import requests,json,smtplib,time
from email.mime.text import MIMEText
from email.utils import formataddr
sender='749832133@qq.com'    # 发件人邮箱账号
password = 'fbzjazzeyracbaih'      # 发件人邮箱密码(注意这个密码不是QQ邮箱的密码，是在QQ邮箱的SMTP中生成的授权码)
reciver = '1481604320@qq.com'      # 收件人邮箱账号，我这边发送给自己
Cookie = 'Secure; JSESSIONID=A4326B652D84B8C0458F94F9E941588A; Secure'
def getInfo():
    url = 'https://jwglxt.fjnu.edu.cn/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
    headers = {
        'Host': 'jwglxt.fjnu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Length': '148',
        'Origin': 'https://jwglxt.fjnu.edu.cn',
        'Connection': 'keep-alive',
        'Referer': 'https://jwglxt.fjnu.edu.cn/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default&su=116072017036',
        'Cookie': Cookie,
        'TE': 'Trailers'
    }
    data = {
        'xnm':"2019",
        'xqm':"12",
        '_search':"false",
        'nd':"1593162087469",
        'queryModel.showCount':"15",
        'queryModel.currentPage':"1",
        'queryModel.sortName':"",
        'queryModel.sortOrder':"asc",
        'time':"1"
    }
    resp = requests.post(url,headers=headers,data=data)
    data = json.loads(resp.text)
    count = data['totalCount']
    items = data['items']
    info = ""
    for item in items:
        Course = item['kcmc']
        Score = item['cj']
        info+=Course+ " " +Score+"\n"
    return count,info

def sendEmail(sender,password,reciver,info):
    state = True
    try:
        msg = MIMEText(info, 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["", sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["", reciver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "成绩自动查询"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(sender, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(sender, [reciver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        state = False
    return state

def setCount(count):
    with open("count.txt" , "w+") as f:
        f.write(str(count))

def getCount():
    try:
        with open("count.txt", "r") as f:
                return int(f.read())
    except:
        return 0

def isSend(num):
    count = getCount()
    if(num > count):
        setCount(num)
        return True
    return False
def main():
    count, info = getInfo()
    print(info)
    state = isSend(count)
    if(state):
        state = sendEmail(sender, password, reciver, info)
        sendEmail(sender, password, "1843264686@qq.com", "成绩已出")
        sendEmail(sender, password, "1164221036@qq.com", "成绩已出")
        sendEmail(sender, password, "1439651427@qq.com", "成绩已出")
        if(state):
            print("发送成功")
        else:
            print("发送失败")

if __name__ == '__main__':
    while(True):
        main()
        time.sleep(60)