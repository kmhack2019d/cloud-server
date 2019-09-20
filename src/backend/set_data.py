from dotenv import load_dotenv
import os
import pycca as cca
import json

load_dotenv()

fileName = "dummy.json"
filePath = "dummy.json"

cred = cca.AdminStaff(os.environ['CPS_USER_ID'], os.environ['CPS_USER_PASSWORD'])
files = cca.File(os.environ['CPS_APP_ID'], os.environ['CPS_GROUP_ID'], "sample_file", fileName)
try:
    d = files.update_file(cred, filePath)
except:
    d = files.upload_file(cred, filePath, fileName)
