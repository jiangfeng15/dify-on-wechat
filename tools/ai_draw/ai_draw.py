import requests
import json
import time

class ai_draw:
    res_picture_url = None
    header = {}
    post_body = {}
    task_id = ""
    def __init__(self,promot):
        self.set_promotion(promot)
        self.set_header()
    def add_task():
        PASS
    def set_header(self):
        self.header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,und;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Cookie": "__huid=11/xpi1SrFXobyKkXuxbnIdQX0084qaf+VBQkWuxd8bUc=; __guid=156009789.3685170545574759000.1693382486105.9124; __gid=156009789.36613679.1693382486105.1693382550820.7; webp=1; Q=u%3D360H3155002958%26n%3D%26le%3D%26m%3DZGH5WGWOWGWOWGWOWGWOWGWOAwZ0%26qid%3D3155002958%26im%3D1_t0105d6cf9b508f72c8%26src%3Dpcw_hongtu%26t%3D1; __NS_Q=u%3D360H3155002958%26n%3D%26le%3D%26m%3DZGH5WGWOWGWOWGWOWGWOWGWOAwZ0%26qid%3D3155002958%26im%3D1_t0105d6cf9b508f72c8%26src%3Dpcw_hongtu%26t%3D1; T=s%3Daacab85f522ac4ae72d739a3ef24a225%26t%3D1713403572%26lm%3D0-1%26lf%3D2%26sk%3D3fc5b6ff0379b2431ffd6fe26f4dd426%26mt%3D1713403572%26rc%3D%26v%3D2.0%26a%3D1; __NS_T=s%3Daacab85f522ac4ae72d739a3ef24a225%26t%3D1713403572%26lm%3D0-1%26lf%3D2%26sk%3D3fc5b6ff0379b2431ffd6fe26f4dd426%26mt%3D1713403572%26rc%3D%26v%3D2.0%26a%3D1; test_cookie_enable=null",
            "Host": "tu.360.cn",
            "Origin": "https://tu.360.cn",
            "Q": "u=360H3155002958&n=&le=&m=ZGH5WGWOWGWOWGWOWGWOWGWOAwZ0&qid=3155002958&im=1_t0105d6cf9b508f72c8&src=pcw_hongtu&t=1",
            "Referer": "https://tu.360.cn/editor?srcg=default",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "T": "s=aacab85f522ac4ae72d739a3ef24a225&t=1713403572&lm=0-1&lf=2&sk=3fc5b6ff0379b2431ffd6fe26f4dd426&mt=1713403572&rc=&v=2.0&a=1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-QID": "3155002958",
            "m2d": "",
            "sec-ch-ua-platform": "Windows",
            }
        #body_length = len(self.post_body)
        #if body_length > 0:
        #    self.header['Content-Length'] = str(body_length)
    def set_promotion(self,promotion:str):
        self.post_body={
        "guidance_scale":15,
        "height":2048,
        "inference_steps":50,
        "m2": "",
        "n_prompt":"",
        "nums":1,
        "object_name":"",
        "private_image_size":"2048x2048",
        "private_upload_image_preview_url":"",
        "prompt":promotion,
        "prompt_angle":"",
        "prompt_artist":"",
        "prompt_decorator":"",
        "prompt_render_methods":"",
        "prompt_style": "",
        "prompten": "",
        "qid":"3155002958",
        "ratio": "16:9",
        "seed": -1,
        "size":"",
        "sk": "",
        "sk_sn": "",
        "src_type": "hongtu",
        "strength":0.75,
        "style": 2,
        "title": "AI创作",
        "width": 2048
        }
    def create_ai_task(self):
        try:
            post_url = "https://tu.360.cn/api-tu/aiwork/text2image?platform=21&device=21&ver=6.0&src_type=hongtu"    
            response = requests.post(post_url, headers = self.header, json = self.post_body)
            """
            {
                "errno": 0,
                "errmsg": "success",
                "data": {
                    "task_id": "ati3155002958-92552401251424303e49717c517aa305"
                }
             }
            """
            #print(response.text)
            time.sleep(1)
            resp_json = json.loads(response.text)
            if resp_json.get('errno') == 0:
                if resp_json.get('data'):
                    res_data = resp_json['data']
                    self.task_id = res_data['task_id']
            else:
                print(resp_json['errmsg'])
        except Exception as e:
            print({e})
    def get_ai_res_url(self):
        res_url = ""
        if self.task_id != "":
            #task_id以获取，开始查询ai生成结果
            get_url = f"https://tu.360.cn/api-tu/aiwork/text2image_result?platform=21&device=21&ver=6.0&src_type=hongtu&sk=&sk_sn=&m2=&qid=3155002958&task_id={self.task_id}"
            try:
                while True:
                    response = requests.get(get_url,headers = self.header)
                    #print(response.text)
                    resp_json = json.loads(response.text)
                    if resp_json.get('errno') == 0:
                        if resp_json.get('data'):
                            res_data = resp_json['data']
                            status = res_data['status']
                            if status == "success":
                                #解析图片资源url
                                pic_list = res_data["list"]
                                for pic_item in pic_list:
                                    res_url = pic_item.get('hires_image')
                                break
                            elif status == "running":
                                time.sleep(1)
                                continue

                    else:
                        print(resp_json['errmsg'])
                        break                
            except Exception as e:
                print({e})
        return res_url



#aiobj = ai_draw("画一直小狗")
#aiobj.create_ai_task()
#print(aiobj.task_id)
#res_url = aiobj.get_ai_res_url()
#print(res_url)
