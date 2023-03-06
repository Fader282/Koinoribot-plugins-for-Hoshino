import hashlib
import uuid
import warnings

import time

import requests

true="true"
false="flse"
YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = '68bc2ee7f0c81f01'
APP_SECRET = 'DAR6n72KwlVOHzAkBA5g3tKJggiiaaIX'



def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]



def sconnect(q):
    data = {}
    warnings.simplefilter('ignore',ResourceWarning)
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['from'] = 'auto'
    data['appKey'] = APP_KEY
    data['q']=q
    data['salt'] = salt
    data['sign'] = sign
    data['vocabId'] = "您的用户词表ID"
    data['to'] = 'ja'

    response = do_request(data)
    contentType = response.headers['Content-Type']
    if contentType == "audio/mp3":
        pass
        millis = int(round(time.time() * 1000))
        filePath = "合成的音频存储路径" + str(millis) + ".mp3"
        fo = open(filePath, 'wb')
        fo.write(response.content)
        fo.close()
    else:
        ssr=response.content
        str1=str(ssr, encoding = "utf-8")
        sss=eval(str1)
        print(sss)
        if not 'basic' in sss.keys():
            return sss['translation']

        return sss['basic']['explains']