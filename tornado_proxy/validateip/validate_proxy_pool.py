#coding:utf8
import redis,json
import urllib, urllib2
import time

testurl = 'http://106.14.135.47:2233/'
 

def test_proxy(url, ip, port, timeout = 5):
    try:
        proxy_handler = urllib2.ProxyHandler({'http': 'http://%s:%s/' % (ip, port)})
        opener = urllib2.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        ret = opener.open(url, timeout=timeout)
        print ret.code
        resp = opener.open(url, timeout=timeout).read()
        if ret.code == 200 and resp == 'Hello, world':
            print resp
            print ret.url
            return True
        else:
            print ret.code
            return False
    except Exception, e:
        print e
    return False


def validate(proxy, testurl):
    return test_proxy(testurl, proxy.split(':')[0], proxy.split(':')[1], 5)


while True:
    db = redis.StrictRedis(host='210.22.106.178', port=2003)
    for proxy in db.zrange('proxy', 0, -1):
        if not validate(proxy, testurl):
            db.zrem('proxy', proxy)
            print 'remove proxy:%s' % proxy
    print 'end'
    time.sleep(3600)



