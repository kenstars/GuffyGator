import os
import json
import requests
from pandas.io.json import json_normalize
from random import choice
import logging
import urllib
import shutil
import gearman
class IntentParser(object):
    def __init__(self):
        self.header = {"Content-Type":"application/json","apiKey":"F9RpSEoojxWCec6"}
        self.gm_worker = gearman.GearmanWorker(['localhost:4730'])
        self.gm_worker.register_task('Gator',self.run)
    def getUrlList(self,sticker):
        list1 = []
        for dictionary in sticker:
            for imagetype in dictionary:
                for each in dictionary[imagetype]:
                    if str(each) == 'original':
                        if '.png' in dictionary[imagetype][each]['url']:
                            list1.append(dictionary[imagetype][each]['url'])
        return list1

    def run(self,gearman_worker,gearman_job):
        body = {"sentence" : gearman_job.data}
        result = requests.post('http://text2gif.guggy.com/v2/guggify',headers = self.header,json = body)
        content = json.loads(result._content)
        stickers = content['sticker']
        urls = self.getUrlList(stickers)
        if urls:
            ph = str(choice(urls))
            r = requests.get(ph, stream=True)
            if r.status_code == 200:
                with open("img.png", 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        else:
            print "Not Found"
        return json.dumps({'result':'success'})

if __name__ == '__main__':
    intent = IntentParser()
    intent.gm_worker.work()