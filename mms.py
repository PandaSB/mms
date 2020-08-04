#!/usr/bin/python2.7
import requests
from requests.auth import HTTPBasicAuth
from messaging.mms.message import MMSMessage, MMSMessagePage
from cStringIO import StringIO
import socket
import ConfigParser
import os
import sys
from datetime import datetime

url = ''
login = ''
passwd = ''
tmp_image = ''
telephone = ''
MMSC = ''

def get_config():

    global url
    global login
    global passwd
    global tmp_image
    global telephone
    global MMSC
    config = ConfigParser.ConfigParser()
    if os.path.exists(os.environ['HOME']+'/.mmsrc.conf'):
        config.read (os.environ['HOME']+'/.mmsrc.conf')
    else:
        if os.path.exists(os.environ['HOME']+'/.mmsrc.conf'):
            config.read ('/etc/mmsrc.conf')
        else:
            if sys.version_info[0] < 3:
                config.add_section('mms')
                config.set('mms', 'url', 'http://192.168.0.242/tmpfs/auto.jpg')
                config.set('mms', 'login', 'login')
                config.set('mms', 'passwd', 'passwd')
                config.set('mms', 'tmp_image', '/tmp/image.jpg')
                config.set('mms', 'telephone', '+336aabbccdd')
                config.set('mms', 'MMSC', 'mms.free.fr')
                config.set('mms', 'notused', 'true')
            else :
                config['mms'] = {'url': 'http://192.168.0.242/tmpfs/auto.jpg', 'login': 'login', 'passwd': 'passwd', 'tmp_image':'/tmp/image.jpg', 'telephone': '+336aabbccdd','MMSC': 'mms.free.fr', 'notused': 'true'}
            config.write(open(os.environ['HOME']+'/.mmsrc.conf', 'w'))
            print 'Sample default file created in ' + os.environ['HOME']+'/.mmsrc.conf'
            sys.exit()
    url = config.get('mms', 'url')
    login = config.get('mms', 'login')
    passwd = config.get('mms', 'passwd')
    tmp_image = config.get('mms', 'tmp_image')
    telephone = config.get('mms', 'telephone')
    MMSC =  config.get('mms', 'MMSC')

def get_image():
    html=requests.get(url,auth=HTTPBasicAuth(login,passwd))
    file = open(tmp_image, 'wb')
    file.write(html.content)
    file.close()

def send_message():

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    mms = MMSMessage()
    mms.headers['To'] = telephone + '/TYPE=PLMN'
    mms.headers['Message-Type'] = 'm-send-req'
    mms.headers['Subject'] = 'Image Alarm'

    slide1 = MMSMessagePage()
    slide1.add_image(tmp_image)
    slide1.add_text('Image Alarm.' + dt_string)

    mms.add_page(slide1)

    payload = mms.encode()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((MMSC, 80))
    s.send("POST / HTTP/1.0\r\n")
    s.send("Content-Type: application/vnd.wap.mms-message\r\n")
    s.send("Content-Length: %d\r\n\r\n" % len(payload))

    s.sendall(payload)

    buf = StringIO()

    while True:
        data = s.recv(4096)
        if not data:
            break

        buf.write(data)

    s.close()
    data = buf.getvalue()
    buf.close()

if __name__ == '__main__':
    get_config()
    get_image()
    send_message()
