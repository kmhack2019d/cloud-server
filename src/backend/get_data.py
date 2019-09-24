from dotenv import load_dotenv
import os
import pycca as cca
import json

load_dotenv()

def getData(raspi):
    with open("./temp/data"+raspi+".json", 'r') as fp:
        json_data = json.load(fp)

    return json_data
