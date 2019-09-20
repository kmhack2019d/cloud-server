from dotenv import load_dotenv
import os
import pycca as cca
import json

load_dotenv()

def getData():

    cred = cca.AdminStaff(os.environ['CPS_USER_ID'], os.environ['CPS_USER_PASSWORD'])
    files = cca.File(os.environ['CPS_APP_ID'], os.environ['CPS_GROUP_ID'], "sample_file", "json")
    d = files.download(cred, "./temp/data.json")

    json_data = None
    with open("./temp/data.json", 'r') as fp:
        json_data = json.load(fp)

    return json_data
