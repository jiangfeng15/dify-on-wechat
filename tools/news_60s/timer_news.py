import requests
import json
import time
def get_60s_news():
    url = "https://v2.alapi.cn/api/zaobao"

    payload = "token=Wgj2ouES7XFbbNAG&format=json"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)
    time.sleep(1)
    res_json = json.loads(response.text);

    news_text = ''
    image_url = ''
    if res_json['code'] == 200:
        image_url = res_json['data']['image']
        news_text = res_json['data']['news']
    else:
        return False,None
    """
    response = requests.get(image_url)
    time.sleep(1)
    if response.status_code == 200:
        with open('resource/news_pics/temp_image.jpg', 'wb') as file:
            file.write(response.content)
    else:
        #logger.debug("[WX] can not download image file.")
        return False,None
    """
    return True,image_url


