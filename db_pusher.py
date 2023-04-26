import redis
import time
import json

with open('./generated.json') as f:
    s_json = f.read()

db = redis.StrictRedis(host='localhost', port=6379)

print("setters:")

start = time.time()
db.set('json_string', s_json)
print("string:", time.time() - start)

start = time.time()
db.hset('json_hset', '1', s_json)
print("hset:", time.time() - start)

zset_d = json.loads(s_json)
zset_ds = {}
for i, item in enumerate(zset_d):
    zset_ds[json.dumps(item)] = i

start = time.time()
zset_count = db.zadd('json_zset', zset_ds)
print("zset:", time.time() - start)

list_d = json.loads(s_json)
list_ds = []
for item in list_d:
    list_ds.append(json.dumps(item))

start = time.time()
list_count = db.lpush('json_list', *list_ds)
end = time.time()
print("list:", time.time() - start, '\n')

#getters
print("getters:")

start = time.time()
db.get('json_string')
print("string:", time.time() - start)

start = time.time()
db.hget('json_hset', '1')
print("hset:", time.time() - start)

start = time.time()
db.zrange('json_zset', 0, zset_count)
print("zset:", time.time() - start)

start = time.time()
db.lrange('json_list', 0, list_count)
print("list:", time.time() - start)

db.flushall()
