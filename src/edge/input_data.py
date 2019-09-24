from dotenv import load_dotenv
import os
import random
import pycca as cca
import json
import time

load_dotenv()

raspi = 0
items = [[0 for i in range(60)]]

while True:
    items[raspi].append(random.randint(0, 100))
    items[raspi].pop(0)

    fp = open("temp/data"+str(raspi)+".json",'w')
    reversed_items = list(reversed(list(map(lambda x: {
      "time": 0,
      "value": x
    }, items[raspi]))))
    json.dump([{
      "micid": 0,
      "data": reversed_items
    }], fp)

    fileName = "data"+str(raspi)+".json"
    filePath = "temp/data"+str(raspi)+".json"

    with open(filePath, 'r') as fp:
        print(json.load(fp))

    cred = cca.AdminStaff(os.environ['CPS_USER_ID'], os.environ['CPS_USER_PASSWORD'])
    files = cca.File(os.environ['CPS_APP_ID'], os.environ['CPS_GROUP_ID'], "sample_file", fileName)
    try:
        d = files.update_file(cred, filePath)
    except:
        print("error")
    time.sleep(1)
    print("Done")
