import memcache 

mc = memcache.Client(['127.0.0.1:11211'])

alloffmess = mc.get('cccc')[5]
if mc.get('cccc')[5]:
    print("full") 
    for val in alloffmess:
        uname = val.split(";")[0]
        offmess = val.split(";")[1]
        print ("user:(" + uname + ") leave a offline message to you:" + offmess)