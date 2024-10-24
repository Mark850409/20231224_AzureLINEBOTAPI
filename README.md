# 20231224_AzureLINEBOTAPI

### 簡介

建立AZURE FUNCTION並部署LINE BOT應用

### 目錄
- [20231224\_AzureLINEBOTAPI](#20231224_azurelinebotapi)
    - [簡介](#簡介)
    - [目錄](#目錄)
  - [專案架構](#專案架構)
  - [請協助驗證程式內容](#請協助驗證程式內容)
  - [完成畫面預覽](#完成畫面預覽)
  - [GitHub使用方式](#github使用方式)
  - [測試方式](#測試方式)
    - [使用azure function tools測試](#使用azure-function-tools測試)
    - [使用postman測試回傳訊息](#使用postman測試回傳訊息)
    - [使用postman打API並推播訊息給LINE](#使用postman打api並推播訊息給line)
    - [本機測試才需要執行此步驟(產生LINE簽章)](#本機測試才需要執行此步驟產生line簽章)
    - [注意事項](#注意事項)
    - [一、事前準備](#一事前準備)
    - [二、開始撰寫程式](#二開始撰寫程式)
    - [三、開始部署到AZURE FUNCTION](#三開始部署到azure-function)
    - [四、參考連結](#四參考連結)



---

## 專案架構
```
20231224_AzureLINEBOTAPI
├─ .funcignore
├─ .git
│  ├─ config
│  ├─ description
│  ├─ FETCH_HEAD
│  ├─ HEAD
│  ├─ hooks
│  │  ├─ applypatch-msg.sample
│  │  ├─ commit-msg.sample
│  │  ├─ fsmonitor-watchman.sample
│  │  ├─ post-update.sample
│  │  ├─ pre-applypatch.sample
│  │  ├─ pre-commit.sample
│  │  ├─ pre-merge-commit.sample
│  │  ├─ pre-push.sample
│  │  ├─ pre-rebase.sample
│  │  ├─ pre-receive.sample
│  │  ├─ prepare-commit-msg.sample
│  │  ├─ push-to-checkout.sample
│  │  ├─ sendemail-validate.sample
│  │  └─ update.sample
│  ├─ index
│  ├─ info
│  │  └─ exclude
│  ├─ logs
│  │  ├─ HEAD
│  │  └─ refs
│  │     └─ heads
│  │        └─ master
│  └─ refs
│     ├─ heads
│     │  └─ master
│     └─ tags
├─ .gitignore
├─ .vscode
│  ├─ extensions.json
│  ├─ launch.json
│  ├─ settings.json
│  └─ tasks.json
├─ host.json
├─ HttpTrigger1
│  ├─ function.json
│  ├─ sample.dat
│  └─ __init__.py
├─ README.md
└─ setting
   └─ setting.py

```


## 請協助驗證程式內容
> 1. 我抓的是即時資料，因此每天的股價數值應與Yahoo相符，請協助進入此網址確認https://tw.stock.yahoo.com/
> 2. 請驗證LINEBOT輸入正確台股代號是否會回傳訊息，因為API要資料不會即時回傳，等待個1分鐘才收到回覆都算正常，超過時間可能代表程式有誤，請協助提出(問題已解)
> 3. 請驗證LINEBOT輸入錯誤代號是否會出現"您的股票代號查不到呢，換個股票代號試試!!!"的訊息

---

## 完成畫面預覽

輸入正確台股代碼，回傳對應訊息
![image-20231230151901499](https://markweb.idv.tw/uploads/image-20231230151901499.png)

隨意輸入錯誤代碼，回傳對應訊息
![image-20231230151916489](https://markweb.idv.tw/uploads/image-20231230151916489.png)

---

## GitHub使用方式
1. 請先進入以下網址，https://github.com/Mark850409/20231224_AzureLINEBOTAPI
2. 點選code按鈕，下方有個download ZIP
3. 使用git的同學可以點選code按鈕，複製https網址，開啟CMD，輸入以下指令，將專案複製到自己本機進行使用

```bash
git clone https://github.com/Mark850409/20231224_AzureLINEBOTAPI.git
```

---

## 測試方式

### 使用azure function tools測試
```
使用ngrok短暫將網站變成https

ngrok config add-authtoken [自己的token]
ngrok http 7071 
```
首先執行ngrok.exe
![image-20231230140304179](https://markweb.idv.tw/uploads/image-20231230140304179.png)


輸入指令ngrok http 7071 
![image-20231230140424320](https://markweb.idv.tw/uploads/image-20231230140424320.png)


等待測試環境建立完成
![image-20231230140555359](https://markweb.idv.tw/uploads/image-20231230140555359.png)


網站回傳結果如下
![image-20231230140751402](https://markweb.idv.tw/uploads/image-20231230140751402.png)


完成畫面如下
![image-20231230140837949](https://markweb.idv.tw/uploads/image-20231230140837949.png)

--- 

### 使用postman測試回傳訊息

選擇GET，輸入測試網址，點選send
![image-20231230003205989](https://markweb.idv.tw/uploads/image-20231230003205989.png)

回傳正確訊息
![image-20231230003230516](https://markweb.idv.tw/uploads/image-20231230003230516.png)


### 使用postman打API並推播訊息給LINE

方法選擇post，貼上API網址，並在authorization的地方點選Bearer Token，貼上自己的token
![image-20231230005620845](https://markweb.idv.tw/uploads/image-20231230005620845.png)


在header增加json表頭
![image-20231230005447046](https://markweb.idv.tw/uploads/image-20231230005447046.png)


BODY增加要傳送的訊息
![image-20231230005523375](https://markweb.idv.tw/uploads/image-20231230005523375.png)


![image-20231230005655597](https://markweb.idv.tw/uploads/image-20231230005655597.png)


成功畫面如附圖
![image-20231230005739028](https://markweb.idv.tw/uploads/image-20231230005739028.png)


### 本機測試才需要執行此步驟(產生LINE簽章)
```python
import base64
import hashlib
import hmac
body=''
channel_secret = '填上自己的token' # Channel secret string
hash = hmac.new(channel_secret.encode('utf-8'),body.encode('utf-8'), hashlib.sha256).digest()
signature = base64.b64encode(hash)
print(signature)
```

### 注意事項
```
1. LINE的webhook網址必須是https，而且要是publicIP

2. CHANNEL_ACCESS_TOKEN、CHANNEL_SECRET、USER_ID可在LINE官方後台查詢

3. CHANNEL_ACCESS_TOKEN、CHANNEL_SECRET請保存好，不要擅自給別人做使用
```


---

### 一、事前準備

先到LINE developers，首次請先進行登入
https://developers.line.biz/zh-hant/

在provider選項點擊Create，輸入名稱後按下確定
![image-20231224212703551](https://markweb.idv.tw/uploads/image-20231224212703551.png)

點選Create a Messaging API Channel
![image-20231224212726942](https://markweb.idv.tw/uploads/image-20231224212726942.png)

這邊選擇Taiwan
![image-20231224212804756](https://markweb.idv.tw/uploads/image-20231224212804756.png)


輸入頻道名稱、敘述&選擇分類、子分類
![image-20231224212957679](https://markweb.idv.tw/uploads/image-20231224212957679.png)



畫面移至最底下，最後兩個選項打勾，點選Create
![image-20231224212926974](https://markweb.idv.tw/uploads/image-20231224212926974.png)


點選OK
![image-20231224213019775](https://markweb.idv.tw/uploads/image-20231224213019775.png)

點選Agree
![image-20231224213039145](https://markweb.idv.tw/uploads/image-20231224213039145.png)

請事先建立好AZURE FUNCTION，並複製URL
![image-20231224213216240](https://markweb.idv.tw/uploads/image-20231224213216240.png)

進入到Messaging API的Webhooksettings，將網址貼上，最後點選update
![image-20231224213317780](https://markweb.idv.tw/uploads/image-20231224213317780.png)

記得選擇Use webhook
![image-20231224213350767](https://markweb.idv.tw/uploads/image-20231224213350767.png)

點選Verify，此步驟用於驗證AZURE FUNCTION和LINE BOT是否串接成功，如出現錯誤請先排查問題
![image-20231224213407468](https://markweb.idv.tw/uploads/image-20231224213407468.png)

---

### 二、開始撰寫程式

開啟__init__.py檔，撰寫以下程式碼

```python
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
# # 台股API
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

    #本機測試，這段請調整
    
    #取得LINE簽章表頭
    #signature = "b'zClv8I9kaPxJg7xlQhQxmIFzilPOVnGvh9F54dUFRmQ='"
    
    #上線測試，請使用這段
    signature = req.headers['x-line-signature']
       
    logging.info("signature: " + signature)

    #取得LINE body內容
    body = req.get_body().decode("utf-8")

    logging.info("Request body: " + body)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        func.HttpResponse(status_code=400)
    
    #本機測試拿到資料，上線測試請註解
    # msg=''
    # data=getYahooAPI('2330')
    # data_info=getTWstockInfo('2330')
    # dt_obj = datetime.fromtimestamp(int(data[0]['Date']/1000))
    # msg+="當日即時股價資訊如下：\n"
    # msg+="====================\n"
    # msg+=f"開盤價:{data[0]['Open']}\n"
    # msg+=f"最高價:{data[0]['High']}\n"
    # msg+=f"最低價:{data[0]['Low']}\n"
    # msg+=f"收盤價:{data[0]['Close']}\n"
    # msg+=f"最後更新時間:{dt_obj}"
    # line_bot_api.push_message(USER_ID, TextSendMessage(text=msg))
    # return func.HttpResponse(
    #         f'{json.dumps(data)}\n\n{msg}\n\n{data_info}',
    #         mimetype="application/json",
    #     )
    #上線測試請使用這段
    return func.HttpResponse("OK",status_code=200)

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
    msg+=f"最後更新時間:{dt_obj}"
    return data

def getTWstockInfo(stock):
    #透過twstock API取得產業資訊
    msg=""
    msg+="您查詢的資訊如下：\n"
    msg+="====================\n"
    msg+=f"公司名稱:{twstock.codes[stock].name}\n"
    msg+=f"ISIN:{twstock.codes[stock].ISIN}\n"
    msg+=f"成立時間:{twstock.codes[stock].start}\n"
    msg+=f"是否上市:{twstock.codes[stock].market}\n"
    msg+=f"產業別:{twstock.codes[stock].group}"
    return msg

#文字訊息觸發點
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
   #取得文字內容
    text=event.message.text
    #用twstock判斷台股代號是否存在，存在則抓取資料，並回傳訊息，否則回傳查無資料
    if text in twstock.twse:
        stock_detail=getTWstockInfo(text)
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
```
開啟setting.py檔，更改以下設定

```powershell
#LINEBOT
CHANNEL_ACCESS_TOKEN='[這邊請填寫自己的CHANNEL_ACCESS_TOKEN]'
CHANNEL_SECRET='[這邊請填寫自己的CHANNEL_SECRET]'
USER_ID='[這邊請填寫自己的USER_ID]'
```

開啟requirements.txt，寫上以下內容

```
azure-functions
requests
line-bot-sdk
yfinance
pandas
BeautifulSoup4
twstock
```

---

### 三、開始部署到AZURE FUNCTION

點選Deploy to Function APP，直到部署完成
![image-20231224220227376](https://markweb.idv.tw/uploads/image-20231224220227376.png)

--- 

### 四、參考連結

1. LINEBOT自動回覆訊息 
https://steam.oxxostudio.tw/category/python/example/line-reply-message.html
   
2. LINEBOT 官方API
https://developers.line.biz/en/reference/messaging-api/#send-reply-message

3. 下載ngrok
https://ngrok.com/download

4. ngrok教學
https://ithelp.ithome.com.tw/articles/10197345

5. LINE signature-validation
https://developers.line.biz/en/reference/messaging-api/#signature-validation

---