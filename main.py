import ftplib
import datetime
from win10toast import ToastNotifier
from time import sleep
import requests

arr = []
url = "https://teamroom.nate.com/api/webhook/" #네이트온 팀룸 오픈API 주소
f = ftplib.FTP()
f.encoding = 'euc-kr'
f.connect('ftp.yes24library.com', 2121)
f.login('yes24ftp', 'dPtm24ftp@tjqj')
welcomeMessage = f.getwelcome()
print(welcomeMessage)
f.cwd('납품사이트/홍지씨앤에스')
toaster = ToastNotifier()


def list_line_callback(line):
    line = line.split()
    if len(line[-2]) != 4:
        arr.append(line[-4:])
    return ""

def web_request(url, dict_data):
    response = requests.post(url=url, data=dict_data,
                             headers={'Content-Type': 'application/x-www-form-urlencoded'})

    dict_meta = {'status_code': response.status_code, 'ok': response.ok, 'encoding': response.encoding,
                 'Content-Type': response.headers['Content-Type']}
    if 'json' in str(response.headers['Content-Type']):
        return {**dict_meta, **response.json()}
    else:  # 문자열 형태인 경우
        return {**dict_meta, **{'text': response.text}}

while True:
    a = f.retrlines("LIST", list_line_callback)
    for i in arr:
        year = datetime.datetime.now().date().strftime("%Y")
        str_datetime = year + " " + i[0] + " " + i[1] + " " + i[2]
        formt = '%Y %b %d %H:%M'
        file_date = datetime.datetime.strptime(str_datetime, formt)
        date_diff = datetime.datetime.now() - file_date
        if date_diff.days == 0 and date_diff.seconds // 60 <= 1:
            print("업로드 발생 : " + i[3])
            web_request(url, {'content': i[3] + " 업로드 발생"})
            toaster.show_toast("FTP 업로드 발생",
                               i[3],
                               duration=10)
    sleep(60)
    arr = []
    print("---1분 경과---")




