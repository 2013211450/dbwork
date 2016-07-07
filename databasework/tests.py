#!/usr/bin/env python

import django

import socket
import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# sys.path.append('/home/liuwei/air_conditioner/room/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dbwork.settings'
django.setup()
from databasework.models import BaseStation
import threading
import urllib
import urllib2

class httptest(threading.Thread):

    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        with open("query.txt", "r") as res:
            for r in res.readlines():
                self.post_to_url(r.strip(), "http://www.radioreference.com/apps/audio/?ctid=5586")

    def post_to_url(self, test_word, url):
        data = urllib.urlencode({"username": "liuwei", "password":"xxxxx"})
        req = urllib2.Request(url=url)
        resp = urllib2.urlopen(req)
        print resp

if __name__ == '__main__':
    t = httptest(3)
    t.start()
    '''
    for i in range(1, 10):
        user = User.objects.filter(username='test'+str(i)).first()
        if not user:
            user = User.objects.create_user('test'+str(i), 'test@qq.com', '123123')
        room = Room.objects.filter(user_id=user.id).first()
        if room:
            print 'Exist'
            print room.id
            room.speed = 0
            room.mode = 0
            room.save()
        else:
            room = Room.objects.create(user_id=user.id, numbers='40'+str(i), room_temperature=27.9)
            print 'create' 
            print room.id
    '''
    # room = Room.objects.get(user_id=user.id)
    # server = Server.objects.first()
    # for i in range(8, 11):
    #     user = User.objects.create_user('test_0'+str(i), 'test@qq.com','123123')
    #    print user.id
    #    print user.username
    #    print room.host

