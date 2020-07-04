import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
def change(str):
    num_change={1:'一',2:'二',3:'三',4:'四',5:'五',6:'六',7:'七',8:'八',9:'九',0:''}
    num=int(str)
    if num <0:
        str='零下'
        num=-num
    else:
        str=''
    if num>=20 and num<=100:
        s=num%10
        t=(num-s)/10
        str=str+"%s十%s" % (num_change[t],num_change[s])
    if num>=10 and num<20:
        s=num%10
        str=str+"十%s" % (num_change[s])
    if num>0 and num<10:
        s=num
        str=str+"%s" % (num_change[s])
    return str
def getText():
    states=['hb','db','hd','hz','hn','xb','xn','gat']
    with open('city.txt') as file:
        lines=file.readlines()
    file.close()
    location=lines[0]
    cityname=lines[1]
    while True:
        choose=input('1,更换地区.\n2,直接播报\n3,退出\n')
        if choose=='1':
            select=int(input('0,华北\n1,东北\n2,华东\n3,华中\n4,华南\n5,西北\n6,西南\n7,港澳台\n:'))
            if select>7 or select<0:
                print('输入格式错误!\n')
            cityname=input('请输入城市名：')
            location=states[select]
            url="http://www.weather.com.cn/textFC/"+location.rstrip()+".shtml"
            headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux i686 (x86_64)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'charset':'utf-8',
            'Referer':url
            }
            check=0
            response=requests.get(url=url,headers=headers)
            response.encoding='utf-8'
            soup=BeautifulSoup(response.text,"html.parser")
            for div in soup.select('div.conMidtab2'):
                for tr in div.select('tr'):
                    if tr.find('td',width='83'):
                        if tr.find('td',width='83').a:
                            if cityname.strip() == tr.find('td',width='83').a.string.strip():
                                with open('city.txt','w') as file:
                                    file.write(location+"\n")
                                    file.write(cityname)
                                check=1
                                file.close()
                                break
                else:
                    continue
                break
            if check==0:
                location=lines[0]
                cityname=lines[1]
                print("输入的城市名有误\n")
        elif choose=='2':
            url="http://www.weather.com.cn/textFC/"+location.rstrip()+".shtml"
            headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux i686 (x86_64)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'charset':'utf-8',
            'Referer':url
            }
            check=0
            response=requests.get(url=url,headers=headers)
            response.encoding='utf-8'
            soup=BeautifulSoup(response.text,"html.parser")
            date=soup.find('ul',attrs={'class': 'day_tabs'}).li.string
            nums=re.findall(r'\d+',date)
            for num in nums:
                num_new=change(num)
                date=date.replace(num,num_new)
            descripe='现在是您所在城市'+cityname+'的天气预报，'+date+'，'
            for div in soup.select('div.conMidtab2'):
                for tr in div.select('tr'):
                    if tr.find('td',width='83'):
                        if tr.find('td',width='83').a:
                            if cityname.strip() == tr.find('td',width='83').a.string.strip():
                                check+=1
                                day='今天'
                                if check==2:
                                    day='明天'
                                elif check==3:
                                    day='后天'
                                if tr.find('td',width='89').string.strip() != '-':
                                    weatherD=tr.find('td',width='89').string
                                    windfromD=tr.find('td',width='162').span.string
                                    winddegreeD=tr.find('td',width='162').span.find_next_sibling().string
                                    degreeD_num=re.search(r'\d+',winddegreeD).group()
                                    degreeD_zh=change(degreeD_num)
                                    winddegreeD=winddegreeD.replace(degreeD_num,degreeD_zh)
                                    winddegreeD=winddegreeD.replace('<','小于')
                                    winddegreeD=winddegreeD.replace('-','到')
                                    winddegreeD=winddegreeD.replace('>','大于')
                                    temD=tr.find('td',width='92').string
                                    temD=change(temD)
                                    descripe=descripe+day+'白天天气预计为'+weatherD+'，'+windfromD+'，风力等级'+winddegreeD+'，最高气温为'+temD+'摄氏度。'
                                    #白天的预报
                                weatherN=tr.find('td',width='98').string
                                windfromN=tr.find('td',width='177').span.string
                                winddegreeN=tr.find('td',width='177').span.find_next_sibling().string
                                degreeN_num=re.search(r'\d+',winddegreeN).group()
                                degreeN_zh=change(degreeN_num)
                                winddegreeN=winddegreeN.replace(degreeN_num,degreeN_zh)
                                winddegreeN=winddegreeN.replace('<','小于')
                                winddegreeN=winddegreeN.replace('-','到')
                                winddegreeN=winddegreeN.replace('>','大于')
                                temN=tr.find('td',width='86').string
                                temN=change(temN)
                                descripe=descripe+day+'晚上天气预计为'+weatherN+'，'+windfromN+'，风力等级'+winddegreeN+'，最低气温为'+temN+'摄氏度。'
                                if check==3:
                                    break
                                #晚上的预报
                else:
                    continue
                break
            print(descripe)
        elif choose=='3':
            return descripe
def main():
    text=getText()
    return
if __name__=='__main__':
    main()