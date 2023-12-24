# AZURE FUNCTION
import logging
import azure.functions as func
# 設定檔參數
from setting import setting
# LineBotApi
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,JoinEvent,FollowEvent
)
# 台股API
import twstock
# 奇摩API
import yfinance as yf

# 爬蟲相關套件
import requests
import time
import json
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup


#取得LINEBOT的CHANNEL_SECRET&CHANNEL_ACCESS_TOKEN&USER_ID
line_bot_api = LineBotApi(setting.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(setting.CHANNEL_SECRET)
USER_ID=setting.USER_ID

#主程式進入點
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 取得LINE簽章表頭
    signature = req.headers['x-line-signature']

    # 取得LINE body內容
    body = req.get_body().decode("utf-8")

    logging.info("Request body: " + body)

    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        func.HttpResponse(status_code=400)

    return func.HttpResponse("OK")

#取得cmoney API資料，取得公司名稱等相關資訊
def getYahooStockDetail(stock_id):
    msg=""
    url = f"https://www.cmoney.tw/finance/f00026.aspx?s={stock_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/111.25 (KHTML, like Gecko) Chrome/99.0.2345.81 Safari/123.36','Connection':'close'}
    res = requests.get(url,headers=headers)
    time.sleep(5)
    soup = BeautifulSoup(res.text,'html.parser')
    # 取得基本資料的cmkey
    for line in soup.find_all(class_="mobi-finance-subnavi-link"):
        if line.text == '基本資料':
            cmkey = line['cmkey'].replace('=','%3D')

    url = f"https://www.cmoney.tw/finance/ashx/mainpage.ashx?action=GetStockBasicInfo&stockId={stock_id}&cmkey={cmkey}"

    # 特別注意要加入Referer
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/111.25 (KHTML, like Gecko) Chrome/99.0.2345.81 Safari/123.36',
        'Referer': f"https://www.cmoney.tw/finance/f00026.aspx?s={stock_id}",
        'Connection':'close'
    }

    res = requests.get(url,headers=headers)
    time.sleep(5)

    #取得資料
    data = res.json()[0]
    #將資料轉換為DataFrame格式
    df = pd.DataFrame({
        'CompanyName':data['CompanyName'],
        'Industry':data['Industry'],
        'SubIndustry':data['SubIndustry'],
        'Business':data['Business']
    },index=[stock_id])

    #將處理好的資料進行回傳，並轉換為JSON
    df = df.to_json(orient='records')
    df = json.loads(df)

    #將訊息資料打包，回傳訊息內容字串
    msg+="您查詢的資訊如下：\n"
    msg+="====================\n"
    msg+=f"公司名稱:{df[0]['CompanyName']}\n"
    msg+=f"產業別:{df[0]['Industry']}\n"
    msg+=f"產業別細項:{df[0]['SubIndustry']}\n"
    msg+=f"經營項目:{df[0]['Business']}"
    return msg

#取得Yahoo API資料，取得公司名稱等相關資訊
def getYahooAPI(stock):
    msg=""
    # 取得當天日期
    get_current_date = datetime.today().strftime("%Y-%m-%d")
    # 開始下載資料
    # 參數1:股票代號
    # 參數2:開始日期
    # 參數3:結束日期
    df=yf.download(f'{stock}.TW',start='2023-12-01',end=get_current_date)
    df.index = pd.to_datetime(df.index).date
    #開始取得各欄位資料
    data = pd.DataFrame(df.ffill().iloc[[-1]])
    data["Open"]=data["Open"].round(2).apply(float)
    data["High"]=data["High"].round(2).apply(float)
    data["Low"]=data["Low"].round(2).apply(float)
    data["Close"]=data["Close"].round(2).apply(float)
    data["Adj Close"]=data["Adj Close"].round(2).apply(float)
    data["Volume"]=data["Volume"].round(2).apply(float)
    data['Date'] = pd.to_datetime(df.index[-1], format='%Y-%m-%d')
   
    data = data.to_json(orient='records')
    data = json.loads(data)
    #將timestamp轉換為datetime格式
    dt_obj = datetime.fromtimestamp(int(data[0]['Date']/1000))
    msg+="當日即時股價資訊如下：\n"
    msg+="====================\n"
    msg+=f"開盤價:{data[0]['Open']}\n"
    msg+=f"最高價:{data[0]['High']}\n"
    msg+=f"最低價:{data[0]['Low']}\n"
    msg+=f"收盤價:{data[0]['Close']}\n"
    msg+=f"最後更新時間:{dt_obj}\n"
    return msg



#文字訊息觸發點
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
   #取得文字內容
    text=event.message.text
    #用twstock判斷台股代號是否存在，存在則抓取資料，並回傳訊息，否則回傳查無資料
    if text in twstock.twse:
        stock_detail=getYahooStockDetail(text)
        stock_msg=getYahooAPI(text)
        result=stock_detail+"\n\n"+stock_msg
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result)
        )
    else:
       texts='您的股票代號查不到呢，換個股票代號試試!!!'
       line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=texts)
        )
       
#第一次加入好友觸發點
@handler.add(JoinEvent)
def handle_join(event):
    text=''
    text+="您好，以下為初次使用說明\n"
    text+="=======================\n"
    text+="1.目前程式只支援查詢台股資料，請輸入正確台股代號\n"
    text+="2.目前程式只支援輸入股票代號查詢\n"
    text+="3.測試代號使用:2412(中華電)、2498(宏達電)、3045(台灣大)\n"
    text+="4.更多代號使用請到奇摩類股查詢:https://tw.stock.yahoo.com/class"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=text)
        )
    
#封鎖後重新加入好友觸發點
@handler.add(FollowEvent)
def handle_follow(event):
    text=''
    text+="您好，以下為初次使用說明\n"
    text+="=======================\n"
    text+="1.目前程式只支援查詢台股資料，請輸入正確台股代號\n"
    text+="2.目前程式只支援輸入股票代號查詢\n"
    text+="3.測試代號使用:2412(中華電)、2498(宏達電)、3045(台灣大)\n"
    text+="4.更多代號使用請到奇摩類股查詢:https://tw.stock.yahoo.com/class"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=text)
        )