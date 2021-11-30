import time
import redis
import consul
import json
from flask import Flask

try:
    c = consul.Consul(host='127.0.0.1', port=8500, scheme = 'http' )
    config_json = json.loads(c.kv.get('redis')[1]['Value'].decode('utf-8'))

except:
    exit()

redis_config = config_json['redis_config']
show_message = config_json['show_message']

app = Flask(__name__)
cache = redis.Redis(host=redis_config['redis_host'], port=redis_config['redis_port'], db=redis_config['redis_db'], password=redis_config['redis_password'])

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
    return '{}! I have been seen {} times.\n'.format(show_message,count)

if __name__ == "__main__":
    app.run()
