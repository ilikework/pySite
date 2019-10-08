import requests
import re

pattern = '.*="(.*?)".*'
url = 'http://hq.sinajs.cn/list='
FORMAT_GREEN = "<font color=\"green\">{}</font>"
FORMAT_RED = "<font color=\"red\">{}</font>"
class Stock(object):

    def __get_stocks(self):
        stocks = ['s_sh000001',
                  's_sz399001',
                  's_sz399005',
                  's_sz399006',
                  's_sz000100',
                  's_sh601186',
                  's_sh600875',
                  's_sh601688',
                  's_sh600887',
                  's_sh603288',
                  's_sz002340',
                  's_sz000876',
                  's_sz000001',
                  's_sh601718',
                  's_sh600816',
                  's_sh601933',
                  's_sz150182',
                  's_sz000516',
                  's_sz000848',
                  's_sz000599',
                  's_sh601949',
                  's_sz002085']
        return stocks

    def get_stock_info(self):
        stock_info = []
        stocks = self.__get_stocks()
        i = 0
        for stock in stocks:
            response = requests.get(url+stock)
            if response.status_code==200:
                match_result = re.match(pattern, response.text)
                info = match_result.group(1).split(',')
                i +=1
                if float(info[2])>0:
                    stock_info.append({ 'no':FORMAT_RED.format(str(i))
                                        ,'name':FORMAT_RED.format(info[0])
                                        ,'price':FORMAT_RED.format(info[1])
                                        ,'rise':FORMAT_RED.format(info[2])
                                        ,'rise_persent':FORMAT_RED.format(info[3])
                                        ,'amount':FORMAT_RED.format(info[4])
                                        ,'sum':FORMAT_RED.format(info[5])})
                elif float(info[2])<0:
                    stock_info.append({ 'no':FORMAT_GREEN.format(str(i))
                                        ,'name':FORMAT_GREEN.format(info[0])
                                        ,'price':FORMAT_GREEN.format(info[1])
                                        ,'rise':FORMAT_GREEN.format(info[2])
                                        ,'rise_persent':FORMAT_GREEN.format(info[3])
                                        ,'amount':FORMAT_GREEN.format(info[4])
                                        ,'sum':FORMAT_GREEN.format(info[5])})
                else:
                    stock_info.append({ 'no':str(i)
                                        ,'name':info[0]
                                        ,'price':info[1]
                                        ,'rise':info[2]
                                        ,'rise_persent':info[3]
                                        ,'amount':info[4]
                                        ,'sum':info[5]})

        return stock_info;
#print(type(response)) # <class 'requests.models.Response'>
#print(response.status_code) # 200
#print(type(response.text)) # <class 'str'>
#print(response.text)
#print(response.cookies) # <RequestsCookieJar[<Cookie BDORZ=27315 for >]>

