import cv2
import os,datetime
import xlrd


class ScanCamera():

    def __init__(self, ip, car_num, channel, user, pwd):
        self.ip = ip
        self.car_num = car_num
        self.channel = channel
        self.rstp_url = "rtsp://%s/user=%s&password=%s&channel=%s" % (
            ip, user, pwd, channel)

    def getFileSize(self, path):
        '''
            获取文件大小
        '''
        try:
            size = os.path.getsize(path)
            return size
        except Exception as err:
            print(err)

    def get_frame(self, url):
        '''
            截取摄像头一帧画面
        '''
        cap = cv2.VideoCapture(url)
        ret, frame = cap.read()
        cv2.imwrite("test.png", frame)  # 保存路径
        cap.release()
        cv2.destroyAllWindows()

    def check(self):
        '''
            从截取的画面中，判断是否黑屏
        '''

        self.get_frame(self.rstp_url) 
        size = self.getFileSize("test.png")

        info = "%s | %s 车位 | 通道%s |" % (self.ip, self.car_num, self.channel)

        if size < 62020:
            info = info + ' 黑屏'
            print(info)
            write_log(date, info)
            return True
        else:
            print(info + " 正常")
            return False


def write_log(date,content):
    '''
        写日志
    '''
    name = str(date) + '.log'
    with open(name ,"a+",encoding="utf-8") as f:
        f.writelines(content + '\n')


user = 'admin'  # 摄像头用户名
pwd = '123'  # 摄像头密码

date = datetime.datetime.now().strftime("%Y-%m-%d")


workbook = xlrd.open_workbook("camera.xls")
table = workbook.sheets()[0]
for row in range(1, table.nrows):
    ip = table.cell(row, 0).value  # IP地址
    car_num = table.cell(row, 1).value  # 车位号
    channel = table.cell(row, 2).value  # 通道
    remark = table.cell(row, 3).value  # 备注

    #如果该记录有备注，则跳过检测
    if remark:
        continue

    obj = ScanCamera(ip, car_num, channel, user, pwd)
    obj.check()
