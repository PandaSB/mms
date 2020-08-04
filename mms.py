#!/usr/bin/python2.7
import requests
from requests.auth import HTTPBasicAuth
from messaging.mms.message import MMSMessage, MMSMessagePage
from cStringIO import StringIO
import socket

url = 'http://192.168.0.242/tmpfs/auto.jpg'
login = 'login'
passwd = 'passwd'

tmp_image = '/tmp/image.jpg'

telephone = '+336XXXXXXXX'
MMSC = 'mms.free.fr'

def get_image():
    html=requests.get(url,auth=HTTPBasicAuth(login,passwd))
    file = open(tmp_image, 'wb')
    file.write(html.content)
    file.close()

def send_message():
    mms = MMSMessage()
    mms.headers['To'] = telephone + '/TYPE=PLMN'
    mms.headers['Message-Type'] = 'm-send-req'
    mms.headers['Subject'] = 'Image Alarm'

    slide1 = MMSMessagePage()
    slide1.add_image(tmp_image)
    slide1.add_text('Image Alarm.')

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
    get_image()
    send_message()
