import memcache

mc = memcache.Client(['127.0.0.1:11211'])
#       mc.key  uname  passwd  alive     friendlist  
mc.set('aaaa',['aaaa','bbbb','offline',[],0,[],0])
mc.set('cccc',['cccc','dddd','offline',[],0,[],0])
mc.set('eeee',['eeee','eeee','offline',['aaaa'],0,[],0])
mc.set('ffff',['ffff','ffff','offline',['aaaa'],0,[],0])

