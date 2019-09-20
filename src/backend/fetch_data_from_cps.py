from dotenv import load_dotenv
import os
import pycca as cca
import json
import time

load_dotenv()

while (1):
    for raspi in range(2):
        try:
            cred = cca.AdminStaff(os.environ['CPS_USER_ID'], os.environ['CPS_USER_PASSWORD'])
            files = cca.File(os.environ['CPS_APP_ID'], os.environ['CPS_GROUP_ID'], "sample_file", "data"str(raspi)+".json")
            d = files.download(cred, "./temp/data"+str(raspi)+".json")
            print("Done")
        except:
            print("Error")
    time.sleep(1)
