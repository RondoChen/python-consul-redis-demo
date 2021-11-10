import sys
import time
import configparser
import redis

from flask import Flask

cf=configparser.ConfigParser()
try:
    cf.read('config/app.ini', encoding='UTF-8')
except:
    print('missing configuration file: app.ini')
    exit()

app = Flask(__name__)
cache = redis.Redis(host=cf.get('redis','redis_host'), port=cf.get('redis','redis_port'), db=cf.get('redis','redis_db'), password=cf.get('redis','redis_password'))

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run()