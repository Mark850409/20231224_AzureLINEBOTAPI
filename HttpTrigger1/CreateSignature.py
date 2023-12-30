import base64
import hashlib
import hmac
body=''
channel_secret = 'vcUT+MUgS9+htF4dqMyQ+/iNrkcvjFrRth5iJIyv2TPPYR4QX9ng9F6Z9b8MElsXPcRslLj0Ge6KSu3dJeP8vkQLF9ASP3XTOuJF8agct8t3tmyeS8RFb76HiD8GOmtGh8gMde+Yj8CuPwBP8ZiUTQdB04t89/1O/w1cDnyilFU=' # Channel secret string
hash = hmac.new(channel_secret.encode('utf-8'),body.encode('utf-8'), hashlib.sha256).digest()
signature = base64.b64encode(hash)
print(signature)