#我們在寫一個伺服器,以下程式碼就是在架設一個伺服器
#我們在做一個web app時通常會把伺服器的主要檔案取為app.py
#python架伺服器(or寫網站)最主流兩種套件:flask, django
#代表這個程式碼是用flask寫的,是用來架設伺服器的
#承上(代表今天就算是一個軟體工程師,只要他不是走網頁領域的話,他不見得懂這個程式碼,即使他很熟python)

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage  #傳貼圖要import"StickerSendMessage"
)

app = Flask(__name__)

line_bot_api = LineBotApi('Q3eo2dA3tXvwQmpzf5jTAYctPp/Vrt5dAWDw+wj8al5JYjTTCVORjIH3jFWb+i0oJK9zdOiafmyMTm+uao+2pLr+meMEj0R+sIaGv6XjMCEwpfSnWQl3XB9ad+bqJYqeJA9mFZ4KT1aLa4uTLuJ2+AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('da7255e8fc5e0f5d19c0d111bc48c999') #secret


@app.route("/callback", methods=['POST'])    #www.line-bot.com"/callback"有人來這個路徑(callboack結尾)敲門的話,就會執行這個觸發事件
def callback():    #返回的觸發事件    #所以我們要在MessagingAPI裡輸入我們程式放在雲端的網址,line就會把訊息轉載到我們給他的網址
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)    #上面那個func會觸發這個handleFunction,顧名思義就是在處理訊息,使用者傳來的訊息有某某某,然後我們就做什麼動作
def handle_message(event):
    msg = event.message.text    #####示範改:使用者tx的訊息,把存成msg
    reply = '很抱歉, 您說什麼'

    ##### 開始改  ############
    if msg in ['hi', 'Hi']:    ####用"=="要完全一樣的hi,改用in清單
        reply = '嗨~'
    elif msg == '你吃飯了嗎':
        reply = '還沒'
    elif msg == '你是誰':
        reply = '我是機器人,我不用打疫苗咧~~~'
    elif '疫苗' in msg:
        reply = '你想打疫苗，是嗎?'
    ##### 結束 ########

    line_bot_api.reply_message(    #回覆訊息
        event.reply_token,
        TextSendMessage(text=reply))    #####示範改:機器回的訊息:改成reply;這行才是真正回覆訊息的




    #####貼圖寫成另個if####
    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(    #line_sdk範例程式碼
            package_id='1',    #貼圖對應什麼代號,這部分要google
            sticker_id='1'
        )
    
    line_bot_api.reply_message(    #回覆訊息
        event.reply_token,
        sticker_message)    #####示範改:機器回的訊息:改成回覆貼圖

    return    #return掉就是這個func就結束了.return是回傳,我們可以return"不寫東西喔"
                  #結果就是"不return東西的return";但是func只要一遇到return,就會自動結束掉.
                  #重要!!!造成我們寫這個return,只是為了讓這個func結束掉
    #####結束######

    #這時回傳貼圖還是失敗,我們要看log了(讀錯誤訊息)
    #cmd打 heroku logs(因為這時候錯誤訊息是"在雲端的",因為這些程式碼在運行,是在heroku的電腦運行的
     #不然錯誤訊息應該是在我的CMD的麻,但現在根本不再local執行,所以要打heroku logs→才可以跟heroku說
     #你的伺服器把那個錯誤訊息傳過來~)
    #會發現"StickerSendMessage is not defined"原因是忘記import!!找到原因了!

    


if __name__ == "__main__": #寫這行是為:程式"被執行"才執行,而不是"被import"就執行,否則才剛寫random,電腦就在產生亂數,CPU就跑很高,這樣不好
    app.run()
