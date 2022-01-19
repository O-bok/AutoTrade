import pyupbit
import numpy as np
import pandas
import telegram as tel
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters

bot = tel.Bot(token="5094812587:AAGQPpvjHcPCJre_E67ExJICMDVWCxWCRSk")
chat_id = -664576700     # autotrade
# chat_id = 1391634332     # private

tickers = pyupbit.get_tickers(fiat="KRW")

def ma_cal(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minutes240')
    df["ma200"] = df["close"].rolling(200).mean()
    ma200 = df['ma200'][-1]
    cur_price = pyupbit.get_current_price(ticker)
    if ma200 < cur_price:
        # print(tickers, 'ma200 :' , ma200 , ', 현재가 :' , cur_price , 'ok')
        bot.sendMessage(chat_id=chat_id, text="{} // 4hma200: {}, 현재가: {}  OK".format(ticker,ma200,cur_price)) # 메세지 보내기

def run(bot,update):
    for ticker in tickers:
        ma_cal(ticker)
    return

# for ticker in tickers:
#     ma_cal(ticker)    

updater = Updater(token="5094812587:AAGQPpvjHcPCJre_E67ExJICMDVWCxWCRSk")
#메세지 핸들러 선언, Filters를 text로 하여 입력되는 텍스트에 반응한다.
message_handler = MessageHandler(Filters.text, run)
#updater에 핸들러를 붙인다.
updater.dispatcher.add_handler(message_handler)
# updater 구동. timeout = polling에 거리는 시간의 최대치, clean = polling 시작전 서버에 보류중인 업데이트를 정리할 것인지 여부.
updater.start_polling(timeout=3)
# updater가 종료되지 않도록 함.
updater.idle()
