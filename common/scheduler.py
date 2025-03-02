# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
import threading
from common.log import logger
from tools.news_60s.timer_news import get_60s_news
from tools.joke_days.every_day_joke import get_good_joke
from config import conf
import requests
import io
import time
import json
import os
from pytz import timezone
from lib.gewechat import GewechatClient

class scheduler(object):
    """description of class"""
    #数据变量
    func_type = {}
    channel_object=None
    group_chatroom = []
    goods_push_group_chatroom = []
    goods_pull_push_switch = False
    
    def __init__(self,channel):
        
        self.appid = conf().get("gewechat_app_id")
        self.base_url = conf().get("gewechat_base_url")
        if not self.base_url:
            logger.error("[gewechat] base_url is not set")
            return
        self.token = conf().get("gewechat_token")
        self.client = channel.client

        self.roomid_name_map = []
        #self.client = GewechatClient(self.base_url, self.token)

        #加载linkconvert配置
        self.config = self._load_linkconvert_config_template()

        self.func_type['news'] = {
            'func':self.news_get,
            'timer':{}
            }
        self.func_type['promotion'] = {
            'func':self.promotion_get,
            'timer':{}
            }
        self.func_type['joke'] = {
            'func':self.joke_get,
            'timer':{}
            }
        self.func_type['goods_pull'] = {
            'func':self.goods_pull,
            'timer':{}
            }
        self.func_type['goods_push'] = {
            'func':self.goods_push,
            'timer':{}
            }
        #获取所有群聊的id-name
        self.get_all_chatrooms_id_name_map()
        #获取新闻推送群列表wxids[]
        self.news_chatrooms_id = []
        news_push_group_list = conf().get("news_push_group_list", [])
        for group_name in news_push_group_list:
            find_flag = False
            for item in self.roomid_name_map:
                if item["nickName"] == group_name:
                    self.news_chatrooms_id.append(item["wxids"])
                    logger.info(f"新闻推送群名称：{group_name}, roomid: {item['wxids']}")
                    find_flag = True
            if not find_flag:
                logger.error(f"新闻推送群名称：{group_name}查找id失败")
            #else:
            #    logger.error(f"群聊：{group_name}查找id失败")
            #room_id = self.get_chatroom_id_by_name(group_name)
            #if  room_id is not None:
            #    logger.info(f"新闻推送群名称：{group_name}, roomid: {room_id}")
            #    self.news_chatrooms_id.append(room_id)
            #else:
            #    logger.error(f"群聊：{group_name}查找id失败")
        #获取商品推送群列表wxids[]
        self.goods_chatrooms_id = []
        goods_push_group_list = conf().get("goods_push_group_list", [])
        for group_name in goods_push_group_list:
            find_flag = False
            for item in self.roomid_name_map:
                if item["nickName"] == group_name:
                    self.goods_chatrooms_id.append(item["wxids"])
                    logger.info(f"商品推送群名称：{group_name}, roomid: {item['wxids']}")
                    find_flag = True
            if not find_flag:
                logger.error(f"商品推送群名称：{group_name}查找id失败")

        #for group_name in goods_push_group_list:
        #    room_id = self.get_chatroom_id_by_name(group_name)
        #    if  room_id is not None:
        #        logger.info(f"商品推送群名称：{group_name}, roomid: {room_id}")
        #        self.goods_chatrooms_id.append(room_id)
        #    else:
        #        logger.error(f"群聊：{group_name}查找id失败")
        
    def init_timer(self,task_config):
        for k,v in task_config.items():
             self.func_type[k]['timer'] = v
        logger.debug("[WX] set scheduler task :[%s]"%(json.dumps(task_config)))

    #获取所有的群聊id
    def get_all_chatrooms_id_name_map(self):
        response = self.client.fetch_contacts_list(self.appid)
        #print(response)
        if response["ret"] == 200:
            my_chatrooms = response["data"]["chatrooms"]
            for chatroom in my_chatrooms:
                chatroom_info = self.get_chatroom_info(chatroom)
                if chatroom_info["data"]["nickName"] is not None:
                    self.roomid_name_map.append({"wxids":chatroom,"nickName":chatroom_info["data"]["nickName"]})
        else:
            logger.error("Failed to fetch chatrooms:", response.json()["msg"])
            return []
    def get_all_chatrooms(self):
        response = self.client.fetch_contacts_list(self.appid)
        #print(response)
        if response["ret"] == 200:
            return response["data"]["chatrooms"]
        else:
            logger.error("Failed to fetch chatrooms:", response.json()["msg"])
            return []
    #通过chatroom_id获取群信息
    def get_chatroom_info(self, chatroom_id):

        response =self.client.get_chatroom_info(self.appid, chatroom_id)
        #print(response)
        if response["ret"] == 200:
            return response
        else:
            logger.error("Failed to get chatroom info:", response["msg"])
            return {}

    #通过群名称去匹配对应的群id,此时需要遍历所有的群，耗时
    def get_chatroom_id_by_name(self, chatroom_name):
        chatrooms = self.get_all_chatrooms()
        for chatroom in chatrooms:
            chatroom_info = self.get_chatroom_info(chatroom)
            if chatroom_info["data"]["nickName"] is not None and chatroom_info["data"]["nickName"] == chatroom_name:
                return chatroom_info["data"]["chatroomId"]
        return None

    def news_get(self):
        logger.debug("[WX] scheduler 获取新闻")
        ret,image_url = get_60s_news()
        try:
            logger.info(f"[WX] get image success, img_url={image_url}")
            for chatroom_id in self.news_chatrooms_id:
                logger.info(f"[WX] scheduler  发送新闻到 {chatroom_id}")

                self.client.post_image(self.appid, chatroom_id,image_url)
                time.sleep(5)
                logger.info(f"[WX] scheduler  发送新闻到 {chatroom_id} 结束")
        except Exception as e:
            logger.error("[WX] scheduler 获取新闻,出现异常，%s"% e)

    def promotion_get(self):
        print("获取促销\n")
        content = ""
        content = "-------京东618现金红包--------\n"
        content += "每次最高24618💰元现金大礼\n"
        content += "12点开启，现金红包会场直达👇\nhttps://u.jd.com/kqas9uw \n"
        content += "-----------------------------------\n"
        content += "口令红包,输入框搜如下任意口令👇\n购物红包263\n粉丝领红包354\n粉丝领福利553\n"
        content += "-----------------------------------\n"
        content += "👉Tips:下单即享返现优惠！\n👉 https://dwz.mk/16j03\n"
        content += "-----------------------------------\n"
        content = "京东618红包链接可收藏每天领三次👇\n① https://u.jd.com/kqas9uw\n② https://u.jd.com/kb37Vcu\n③ https://u.jd.com/kiyMz4D\n"
        for chatroom_id in self.goods_chatrooms_id:
            self.client.post_text(self.appid, chatroom_id, content, "")
    def joke_get(self):
        logger.info(f"[WX] get random joke form joke server")
        ret,res_text = get_good_joke()
        for chatroom_id in self.goods_chatrooms_id:
            self.client.post_text(self.appid, chatroom_id, content, "")
            time.sleep(2)
    #商品获取
    def goods_pull(self):
        try:
            import plugins.linkconvert.jingdong.xianbao_switch
            #判断是否推送
            if plugins.linkconvert.jingdong.xianbao_switch.xianbao_pull_push_switch:            
                from plugins.linkconvert.jingdong.good_collections import goods_stack
                from plugins.linkconvert.jingdong.convert_jd_link import convert_jd_link
                from plugins.linkconvert.jingdong.xianbao_control import xianbao_resource_id
                jd_link_instance = convert_jd_link(self.config)
                logger.info(f"[WX] 开始从服务器获取商品线报信息-资源id{xianbao_resource_id}")

                jd_link_instance.get_jd_ztk_xianbao(2,xianbao_resource_id,0,6*60)
                logger.info(f"[WX] 线报栈大小 [{goods_stack.size()}].")
        except Exception as e:
            logger.error(f"[WX] goods_pull 商品线报捕获异常 [%s]."%e)
        logger.info(f"[WX] goods_pull 结束获取商品信息")
    #商品推送
    def goods_push(self):
        try:
            #from plugins.linkconvert.platform import xianbao_switch
            from plugins.linkconvert.jingdong.xianbao_switch import xianbao_pull_push_switch
            #xianbao_switch = True
            #判断是否推送
            if xianbao_pull_push_switch:
                #清空商品队列
                from plugins.linkconvert.jingdong.good_collections import goods_stack
                goods_stack.clear()
                #商品获取
                self.goods_pull()
                
                logger.info(f"[WX] 开始推送商品线报到商品推送群组")
                content = ""
                #一次推送多条
                push_count = 1
                while push_count > 0:
                    push_count = push_count - 1
                    if goods_stack.size() > 0:
                        logger.debug(f"[WX] 线报栈大小 [{goods_stack.size()}].")
                        
                        #线报资源项
                        xianbao_item = goods_stack.pop()
                        content = f"{xianbao_item.content}\n-----------------------------------\n"
                        
                        #发送消息
                        if content != "" and content is not None:
                            #official_account_link = "👉Tips:京东双十一红包领取！\n👉 https://u.jd.com/COruwur\n-----------------------------------\n更多线报，👉微信小程序[社交购物分享]\n-----------------------------------\n"
                            #official_account_link = "年货节🧧: https://u.jd.com/s6cJWPY \n更多查询👉 #小程序://社交购物分享/n7O8sdAGdrM2Idg"
                            official_account_link = "#小程序://社交购物分享/n7O8sdAGdrM2Idg"
                            content = f"------------京东特价购-------------\n{content}{official_account_link}"
                            for chatroom_id in self.goods_chatrooms_id:
                                self.client.post_text(self.appid, chatroom_id, content, "")
                            time.sleep(2);
                            switch_send_pic = True
                            if switch_send_pic:
                                #发送图片
                                img_url = xianbao_item.img_url
                                if img_url != "" and img_url is not None:
                                    for chatroom_id in self.goods_chatrooms_id:
                                        self.client.post_image(self.appid, chatroom_id, img_url)
                                    logger.info(f"[WX] download image success,img_url={img_url}")
                            time.sleep(120);
                    else:
                        logger.debug(f"[WX] 线报栈为空.")
                        break


        except Exception as e:
            logger.error(f"[WX] 商品线报捕获异常 [%s]."%e)

        logger.info(f"[WX] 结束推送商品线报到商品推送群组")
    def start_scheduler(self):
        work_hours = "8-22"
        scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
        for type,func_info in self.func_type.items():
            hour_value = func_info['timer'].get('hour')
            minute_value = func_info['timer'].get('minute')
            #判断是否启用定时器
            switch = func_info['timer'].get('switch')
            if  hour_value is not None and minute_value is not None:
                if switch:
                    scheduler.add_job(func_info['func'], trigger='cron', hour=(func_info['timer']['hour']), minute=(func_info['timer']['minute']))
            elif hour_value is None and minute_value is not None:
                if switch:
                    scheduler.add_job(func_info['func'], trigger='cron', hour=work_hours, minute=func_info['timer']['minute'])               
        scheduler.start()
    def timer_start(self):
        scheduler_thread = threading.Thread(target=self.start_scheduler)
        scheduler_thread.start()

    def _load_linkconvert_config_template(self):
        try:
            plugin_config_path = os.path.join("plugins/linkconvert/", "config.json.template")
            if os.path.exists(plugin_config_path):
                with open(plugin_config_path, "r", encoding="utf-8") as f:
                    plugin_conf = json.load(f)
                    return plugin_conf
        except Exception as e:
            logger.exception(e)




