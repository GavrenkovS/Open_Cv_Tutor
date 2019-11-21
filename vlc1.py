import getpass
import time
import subprocess
import requests
import serial
import sys
import lxml.etree as etree
import time


class vlc_remote_contol:
    def __init__(self, hst, blist, pname):
        self.host = hst

        self.btn_list = blist

        self.pname = pname
        # self.port = serial.Serial(pname, 9600, timeout=0)
        self.__sess = requests.Session()
        print("init")
        # self.__sess.auth = ('', getpass.getpass())
        self.__sess.auth = ('', '')
        print("init")
        self.old_vol = self.__get_param(self.__sess.get(self.host + '/requests/status.xml').text, 'volume')
        self.curr_vol = 0

    def __get_param(self, info, param):
        beg = info.find('<' + param + '>') + len('<' + param + '>')
        end = info.find('</' + param + '>')
        return int(info[beg:end])

    def __command(self, host, comm, val):
        if (val == ''):
            req = self.__sess.get(host + '/requests/status.xml' + '?' + 'command=' + comm)
        else:
            req = self.__sess.get(host + '/requests/status.xml' + '?' + 'command=' + comm + '&val=' + val)
        req.close()

    def __switch_button(self, btn_code):
        if (btn_code == 'FFC23D'):  ## play/pause
            self.__command(self.host, 'pl_pause', '')
        elif (btn_code == 'FF906F'):  ## fullscreen
            self.__command(self.host, 'fullscreen', '')
        elif (btn_code == 'FFE01F'):  ## volume down
            self.__command(self.host, 'volume', '-10')
        elif (btn_code == 'FFA857'):  ## volume up
            self.__command(self.host, 'volume', '+10')
        elif (btn_code == 'FF22DD'):  ## rewind back
            self.__command(self.host, 'seek', '-0.5%')
        elif (btn_code == 'FF02FD'):  ## rewind forward
            self.__command(self.host, 'seek', '+0.5%')
        elif (btn_code == 'FFA25D'):  ## previous track
            self.__command(self.host, 'pl_previous', '')
        elif (btn_code == 'FFE21D'):  ## previous next
            self.__command(self.host, 'pl_next', '')
        elif (btn_code == 'FF6897'):  ## mute
            self.cur_vol = self.__get_param(self.__sess.get(self.host + '/requests/status.xml').text, 'volume')
            if (self.cur_vol == 0):
                self.__command(self.host, 'volume', str(self.old_vol))
            else:
                self.old_vol = self.cur_vol
                self.__command(self.host, 'volume', '0')
        else:
            pass

    def control(self):
        print('Success')
        # while True:
        # res = self.port.readline().strip().decode("UTF-8")
        # if (res in self.btn_list):
        #    self.__switch_button(res)
        #self.__command(self.host, 'volume', '+10')
        #self.__command(self.host, 'fullscreen', '')
        self.__command(self.host, 'pl_next', '')
        #print("1234")
        #time.sleep(1)
    # pass


def main1():
    conf = etree.parse('conf.xml')
    vpath = conf.xpath('/document/vpath/text()')[0]
    vhost = conf.xpath('/document/vhost/text()')[0]
    try:
        subprocess.Popen([vpath])
    except:
        input('VLC player not found')
        return
    try:
        buttons0 = ['FFA25D', 'FF629D', 'FFE21D', 'FF22DD', 'FF02FD', 'FFC23D', 'FFE01F', 'FFA857', 'FF906F', 'FF6897',
                    'FF9867', 'FFB04F', 'FF30CF', 'FF18E7', 'FF7A85', 'FF10EF', 'FF38C7', 'FF5AA5', 'FF42BD', 'FF4AB5',
                    'FF52AD']
        vrc = vlc_remote_contol(vhost, buttons0, "COM3")
        print("123333333")
        vrc.control()
    except:
        input("Connection or authorization error.")
        return


if __name__ == "__main__":
    main1()
