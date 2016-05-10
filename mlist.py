import memcache

mc = memcache.Client(['127.0.0.1:11211'])

print(mc.get('aaaa'))
print(mc.get('cccc'))
