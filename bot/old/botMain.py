import json 
import requests
import time
import urllib
from student import Student 

TOKEN = "396513103:AAGL6bgtsy1jnpAxLbTe5HmPLDxCHY1MzxM"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

students={}


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def build_keyboard(keyboard):
    print ("keyboard:", keyboard)
    if keyboard:
        #keyboard = [[item] for item in items]
        reply_markup = {"keyboard":keyboard, "one_time_keyboard": True, "resize_keyboard": True}
        return json.dumps(reply_markup)
    else:
        return None


def echo_all(updates):
    for update in updates["result"]:
        try:

            print("\nnext message:\n", update["message"])
            chat = update["message"]["chat"]["id"]
            studentId = update["message"]["from"]["id"]

            if  not studentId in students.keys():
                students[studentId] = Student (update["message"])
            student=students[studentId]
            
            (answers,items) =student.handle(update["message"])
            
            send_messages(answers, chat, build_keyboard(items))
            
                
        except Exception as e:
            print(e)
def send_messages(answers, chat, reply_markup=None):
    for i in range(len(answers)-1):
        send_message(answers[i], chat, None)
        time.sleep(0.05)
    send_message(answers[-1], chat, reply_markup)    

def send_message(text, chat_id, reply_markup=None):
    #text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    print (url)
    get_url(url)

    
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)
        
if __name__ == '__main__':
    main()