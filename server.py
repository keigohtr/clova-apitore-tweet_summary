import os
import urllib3
import json
import requests
import re
from cek import Clova
from flask import Flask, request, jsonify


application_id = "YOUR EXTENSION ID"
clova = Clova(application_id=application_id, default_language="ja", debug_mode=True)

line_notify_token = 'YOUR LINE NOTIFY TOKEN'
line_notify_api = 'https://notify-api.line.me/api/notify'

apitore_access_token = 'YOUR APITORE ACCESS TOKEN'
apitore_tweet_summarize_api = 'https://api.apitore.com/api/27/twitter-summarize/get'

app = Flask(__name__)

@clova.handle.launch
def launch_request_handler(clova_request):
    print("Launch request")
    return clova.response("はい、なにをしらべますか")

@clova.handle.default
def default_handler(clova_request):
    print("Default request")
    return clova.response("もう一度お願いします")

@clova.handle.intent("targetWordIntent")
def intent_targetword_handler(clova_request):
    try:
        print("targetWordIntent request")
        target = clova_request.slots_dict["target"]
        notify_message, cek_response = make_response_tweet_summarize(target)
        payload = {'message': notify_message}
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        requests.post(line_notify_api, data=payload, headers=headers)
        return cek_response
    except:
        return clova.response("ごめんなさい。知らない単語です。")

@clova.handle.intent("nextIntent")
def intent_next_handler(clova_request):
    try:
        print("nextIntent request")
        target = clova_request.session_attributes["target"]
        num = int(clova_request.session_attributes["num"])+1
        notify_message, cek_response = make_response_tweet_summarize(target, num)
        payload = {'message': notify_message}
        headers = {'Authorization': 'Bearer ' + line_notify_token}
        requests.post(line_notify_api, data=payload, headers=headers)
        return cek_response
    except:
        return clova.response("私に話しかけるときは、なになにについて教えて、と話しかけてください。")

def make_response_tweet_summarize(target:str, num:int=1):
    numofTweet, tweet = get_apitore_tweet_summarize(target, num)
    text = re.sub('https?://[^\s]+', 'リンク', tweet)
    text = re.sub('#[^\s]+', '', text)
    text = re.sub('@[^\s]+', '', text)
    if len(text) > 50:
        text = text[0:50]
    if num == 1:
        notify_message = f'\n{target}について直近のツイートの要約です。↓↓↓\n\n{tweet}'
        cek_message = f'{target}について直近のツイートの要約です。。。{text}。。。以上です。'
    else:
        notify_message = f'\n{num}番目の要約です。↓↓↓\n\n{tweet}'
        cek_message = f'{num}番目の要約です。。。{text}。。。以上です。'
    cek_response = clova.response(cek_message)
    cek_response.session_attributes = {"target": target, "num": str(num)}
    return (notify_message, cek_response)

def get_apitore_tweet_summarize(target:str, num:int):
    http = urllib3.PoolManager()
    r = http.request(
        'GET',
        apitore_tweet_summarize_api,
        fields={'access_token': apitore_access_token,
                'q': f'{target} -RT',
                'num' : num})
    res = json.loads(r.data.decode('utf-8'))
    numofTweets = res["numofTweets"]
    return (numofTweets, res["tweets"][num-1]["text"])

@clova.handle.end
def end_handler(clova_request):
    return clova.response("はい、終了します", end_session=True)

@app.route('/hackathon/', methods=['POST'])
def my_service():
    resp = clova.route(request.data, request.headers)
    resp = jsonify(resp)
    # make sure we have correct Content-Type that CEK expects
    resp.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return resp

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=50000)
