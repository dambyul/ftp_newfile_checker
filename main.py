import ftplib
import datetime
from win10toast import ToastNotifier
from time import sleep

arr = []
f = ftplib.FTP()
f.encoding='euc-kr' #경로에 한글 있을 경우
f.connect('도메인',포트)
f.login('아이디', '비밀번호')
welcomeMessage = f.getwelcome();
print(welcomeMessage);
f.cwd('FTP 경로')
toaster = ToastNotifier()

def listLineCallback(line):
    line = line.split()
    if len(line[-2]) != 4 :
        arr.append(line[-4:])
    return ""

while True :
    a = f.retrlines("LIST", listLineCallback);
    for i in arr :
        year = datetime.datetime.now().date().strftime("%Y")
        str_datetime = year + " " + i[0] + " " + i[1] + " " + i[2]
        format = '%Y %b %d %H:%M'
        file_date = datetime.datetime.strptime(str_datetime,format)
        date_diff = datetime.datetime.now() - file_date
        if date_diff.days == 0 and date_diff.seconds // 60 <= 1 :
            print("업로드 발생 : " + i[3])
            toaster.show_toast("FTP 업로드 발생",
                       i[3],
                       duration=10)
    sleep(60)
    arr = []
    print("---1분 경과---")



