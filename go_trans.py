# -*- coding: utf-8 -*-
#!/usr/bin/env python

import re

import json
import requests
import urllib.request

from pprint import pprint
 
client_id = "--"
client_secret = "--"


url = "https://openapi.naver.com/v1/papago/n2mt"
sess = requests.Session()
headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret}

with open('---.srt', 'r', encoding='UTF8') as rf:
    eng_subs = rf.readlines()

index = 1
with open('translated.srt', 'w', encoding='UTF8') as wf:
    wf.write(eng_subs[0])
    for line in eng_subs[1:]:
        if line == '{}\n'.format(index + 1):
            index = index + 1
            wf.write(line)
            continue
        if re.search(r'^[\d]{2}:[\d]{2}:[\d]{2},[\d]{3} --> [\d]{2}:[\d]{2}:[\d]{2},[\d]{3}\n$', line):
            wf.write(line)
            continue
        if len(line) <= 3:
            wf.write(line)
            continue
        text = line.rstrip()
        tr_text = text[:]

        data = {'source': 'en', 'target': 'ko', 'text': text}

        try:
            if index >= 0:
                r = sess.post(url, data=data, headers=headers)
                tr_text = r.json()['message']['result']['translatedText']
        except Exception as err:
            pass

        wf.write('{}\n'.format(tr_text))
        print('{} -> {}'.format(text, tr_text))
