import random
import time
import json

raspi = 0
items = [0 for i in range(60)]

while True:
    items.append(random.randint(0, 100))
    items.pop(0)

    fp = open("temp/data"+str(raspi)+".json",'w')
    json.dump([{
      "micid": 0,
      "data": list(map(lambda x: {
        "time": 0,
        "value": x
      }, items))
    }], fp)

    time.sleep(1)
