import requests
import json

def get_good_joke():
    #接口地址
    url = "https://v2.alapi.cn/api/joke/random"
    
    payload = "token=Wgj2ouES7XFbbNAG&format=json"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    joke_return = ""
    try:

        response = requests.request("POST", url, data=payload, headers=headers)

        res_json = json.loads(response.text);

        joke_text = ''
        joke_title = ''
        if res_json['code'] == 200:
            joke_title = res_json['data']['title']
            joke_text = res_json['data']['content']
            joke_return = f"[开心一刻]：\n[标  题]：{joke_title}\n[内  容]：{joke_text}"
        else:
            joke_text = res_json['msg']
            joke_return = f"[接口异常]-{joke_text}"
           
    except Exception as e:
        return False,joke_return
    return True,joke_return


