"""BloomFilter.tobytes返回一个字典{'header': header, 'data': data}，
其中header是BloomFilter的类信息（如capicity, error_rate等），data保存了具体的hash信息."""
import rediscluster
from pybloom import BloomFilter


if __name__ == "__main__":
    # 创建bf
    bf = BloomFilter(capacity=1000, error_rate=0.0001)
    for i in range(100):
        _ = bf.add(i)
    info = bf.tobytes()
    # 保存至redis
    r = rediscluster.StrictRedisCluster(
        host="tjpt-redis-c1-node001.a.2345inc.com",
        port=9001,
        password='8Mbh8Ykz')
    for key, value in info.items():
        r.hset("test:bloom1:", key, value)
        r.expire("test:bloom1:", 10)
    # 从redis获取info信息
    redis_info = {"header": "", "data": ""}
    for key in redis_info.keys():
        redis_info[key] = r.hget("test:bloom1:", key)
    # 根据从redis获取的info信息创建BloomFilter
    new_bf = BloomFilter.frombytes(redis_info)
    assert bf.bitarray.tobytes() == new_bf.bitarray.tobytes()
