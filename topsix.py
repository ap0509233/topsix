from threading import Timer
from urllib.request import urlopen
import json
import time
import easytrader
import sqlite3
import requests

user=easytrader.use('ths')
user.connect(r'C:\东北证券同花顺统一认证版\xiadan.exe')

fuurl=''
ful=''
ftqqurl='https://sc.ftqq.com/[server酱SCKEY].send'


class getdata:
    def __init__(self,id,name):
        self.id = id
        self.name = name
        fullurl=fuurl+str(id)+ful
        html = urlopen(fullurl)
        hjson = json.loads(html.read())
        ti=hjson['a'][0]['t']
        self.ti = ti
        self.url = fullurl
    def run (self):
        html2=urlopen(self.url)
        hjson2 = json.loads(html2.read())
        tit = hjson2['a'][0]['t']
        if tit == self.ti:
            t = Timer(60, self.run)
            print('运行中--')
            t.start()
        else :
            le=hjson2['a'][0]['s']
            for i in le :
                dealPrice = i["d"]
                operation = i["o"]
                realWeight = i["r"]
                status = i["s"]
                stockCode = i["st"]
                stockName = i["sto"]
                toWeight = i["to"]
                weight = toWeight - realWeight
                stocknum = 0
                if operation == 0:
                   if weight < 0.05 :
                      dat='买入'+'\n'+ stockCode + stockName+'\n' +'----到' + str(toWeight) + '----成交价：' + str(dealPrice) +'\n' 
                      requests.post(ftqqurl,data={'text':self.name,'desp':dat})
                   else:
                      totalm = user.balance
                      mm = totalm['总资产']
                      priceU = round(dealPrice * 1.01, 2)
                      stocknum = int((mm * weight) / (priceU * 100)) * 100
                      code = stockCode[2:]
                      user.buy(code,price=priceU,amount=stocknum)
                      dat='买入'+'\n'+ code + stockName+'\n'+ str(stocknum) +'股'+'\n'+ '----到' + str(toWeight) + '----成交价：' + str(priceU) +'\n' 
                      requests.post(ftqqurl,data={'text':self.name,'desp':dat})
                      write(code,stocknum)
                elif operation == 1:
                   if weight < 0.05 :
                      dat='加仓'+'\n'+ stockCode + stockName+'\n' +'----到' + str(toWeight) + '----成交价：' + str(dealPrice) +'\n' 
                      requests.post(ftqqurl,data={'text':self.name,'desp':dat})
                   else:
                      totalm = user.balance
                      mm = totalm['总资产']
                      priceU = round(dealPrice * 1.01, 2)
                      stocknum = int((mm * weight) / (priceU * 100)) * 100
                      code = stockCode[2:]
                      user.buy(code,price=priceU,amount=stocknum)
                      dat='加仓'+'\n'+ code + stockName+'\n'+ str(stocknum) +'股'+'\n'+ '----到' + str(toWeight) + '----成交价：' + str(priceU) +'\n' 
                      requests.post(ftqqurl,data={'text':self.name,'desp':dat})
                      p=check(code)
                      znum=p+stocknum
                      update(code,znum)
                elif operation == 3:
                   if toWeight < 0.05 :
                      code = stockCode[2:]
                      priceD = round(dealPrice * 0.99, 2)
                      p=check(code)
                      user.sell(code,price=priceD,amount=p)
                      dat='清仓'+'\n'+ stockCode + stockName+'\n' +'----从'+str(realWeight)+'清到' + str(toWeight) + '----成交价：' + str(dealPrice) +'\n'
                      requests.post(ftqqurl,data={'text':self.name,'desp':dat})
                      delete(code)
                   else:
                      if weight > -0.05 :
                         dat='减仓'+'\n'+ stockCode + stockName +'\n'+'----从'+str(realWeight)+'减到' + str(toWeight) + '----成交价：' + str(dealPrice) +'\n' 
                         requests.post(ftqqurl,data={'text':self.name,'desp':dat})
                      else:
                         totalm = user.balance
                         mm = totalm['总资产']
                         priceD = round(dealPrice * 0.99, 2)
                         stocknum = int((mm * weight) / (priceD * 100)) * 100
                         code = stockCode[2:]
                         user.sell(code,price=priceD,amount=stocknum)
                         dat='减仓'+'\n'+ code + stockName+'\n'+ str(stocknum) +'股'+'\n'+ '----到' + str(toWeight) + '----成交价：' + str(priceU) +'\n' 
                         requests.post(ftqqurl,data={'text':self.name,'desp':dat})
                         p=check(code)
                         znum=p-stocknum
                         update(code,znum)
                elif operation == 4:
                     code = stockCode[2:]
                     priceD = round(dealPrice * 0.99, 2)
                     p=check(code)
                     user.sell(code,price=priceD,amount=p)
                     dat='清仓'+'\n'+ stockCode + stockName+'\n' +'----从'+str(realWeight)+'清到' + str(toWeight) + '----成交价：' + str(dealPrice) +'\n'
                     requests.post(ftqqurl,data={'text':self.name,'desp':dat})
                     delete(code)
            print ('重新执行')
            time.sleep(10)
            print ('等待了10秒')
            getdata(self.id,self.name).run()

def write (code,num):
   conn = sqlite3.connect("test.db")
   c    = conn.cursor()
   c.execute("INSERT INTO stocks VALUES (?,?)",(code,num))
   conn.commit()
   conn.close()
   
def check (code):
   conn = sqlite3.connect("test.db")
   c    = conn.cursor()
   c.execute('SELECT num FROM stocks WHERE stocks.code=?',([code]))
   num = c.fetchone()
   conn.commit()
   conn.close()
   return num[0]
   
def update (code,num):
   conn = sqlite3.connect("test.db")
   c    = conn.cursor()
   c.execute('UPDATE stocks SET num=? WHERE code=?',(num, code))
   conn.commit()
   conn.close()
    
def delete (code):
   conn = sqlite3.connect("test.db")
   c    = conn.cursor()
   c.execute('DELETE FROM stocks WHERE code=?',([code]))
   conn.commit()
   conn.close()



ab=getdata(***,'ttt')
ab.run()
