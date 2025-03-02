# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
from config import conf

from tools.joke_days.every_day_joke import get_good_joke

import re
from lib import itchat

@plugins.register(
    name="Hello",
    desire_priority=-1,
    hidden=True,
    desc="A simple plugin that says hello",
    version="0.1",
    author="lanvent",
)


class Hello(Plugin):

    group_welc_prompt = "请你随机使用一种风格说一句问候语来欢迎新用户\"{nickname}\"加入群聊。"
    patpat_prompt = "请你随机使用一种风格介绍你自己，并告诉用户输入#help可以查看帮助信息。"
    group_exit_prompt = "请你随机使用一种风格跟其他群用户说他违反规则\"{nickname}\"退出群聊。"

    def __init__(self):
        super().__init__()
        try:
            self.config = super().load_config()
            if not self.config:
                self.config = self._load_config_template()
            self.group_welc_fixed_msg = self.config.get("group_welc_fixed_msg", {})
            self.group_welc_prompt = self.config.get("group_welc_prompt", self.group_welc_prompt)
            self.group_exit_prompt = self.config.get("group_exit_prompt", self.group_exit_prompt)
            self.patpat_prompt = self.config.get("patpat_prompt", self.patpat_prompt)
            logger.info("[Hello] inited")
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            
        except Exception as e:
            logger.error(f"[Hello]初始化异常：{e}")
            raise "[Hello] init failed, ignore "

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT,
            ContextType.JOIN_GROUP,
            ContextType.PATPAT,
            ContextType.EXIT_GROUP
        ]:
            return
        msg: ChatMessage = e_context["context"]["msg"]
        logger.debug("开始处理hello")
        logger.debug(f"hello插件消息{msg}")
        group_name = msg.other_user_nickname
        if e_context["context"].type == ContextType.JOIN_GROUP:
            #判断全局config.json中是否由配置group_welcome_msg，如果配置了group_welcome_msg，根据group_name
            #选择是否使用全局配置，还是使用hello的config.json.template
            if "group_welcome_msg" in conf() or group_name in self.group_welc_fixed_msg:
                reply = Reply()
                reply.type = ReplyType.TEXT
                if group_name in self.group_welc_fixed_msg:
                    #logger.debug(f"用户群{group_name} 群组 {self.group_welc_fixed_msg}")
                    reply.content = self.group_welc_fixed_msg.get(group_name, "").format(nickname=msg.actual_user_nickname)
                else:
                    logger.debug(f"group_name {group_name} is not in 群组 {self.group_welc_fixed_msg}.")
                    g_wm = conf().get("group_welcome_msg", "")
                    if g_wm != "":
                        g_wm = g_wm.format(nickname=msg.actual_user_nickname)
                    reply.content = g_wm
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
                return
            e_context["context"].type = ContextType.TEXT
            e_context["context"].content = self.group_welc_prompt.format(nickname=msg.actual_user_nickname)
            e_context.action = EventAction.BREAK_PASS  # 事件结束，进入默认处理逻辑
            if not self.config or not self.config.get("use_character_desc"):
                e_context["context"]["generate_breaked_by"] = EventAction.BREAK
            return
        
        if e_context["context"].type == ContextType.EXIT_GROUP:
            if conf().get("group_chat_exit_group"):
                e_context["context"].type = ContextType.TEXT
                from datetime import datetime
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

                reply = Reply()
                reply.type = ReplyType.TEXT
                reply.content = self.group_exit_prompt.format(nickname=msg.actual_user_nickname,exit_time=formatted_time)
                e_context["reply"] = reply
                #e_context["context"].content = self.group_exit_prompt.format(nickname=msg.actual_user_nickname,exit_time=formatted_time)
                e_context.action = EventAction.BREAK_PASS  # 事件结束，进入默认处理逻辑
                return
            e_context.action = EventAction.BREAK_PASS 
            return
            
        if e_context["context"].type == ContextType.PATPAT:
            e_context["context"].type = ContextType.TEXT
            e_context["context"].content = self.patpat_prompt
            e_context.action = EventAction.BREAK_PASS   # 事件结束，进入默认处理逻辑
            if not self.config or not self.config.get("use_character_desc"):
                e_context["context"]["generate_breaked_by"] = EventAction.BREAK
            return

        content = e_context["context"].content
        logger.debug("[Hello] on_handle_context. content: %s" % content)
        if content == "Hello":
            reply = Reply()
            reply.type = ReplyType.TEXT
            if e_context["context"]["isgroup"]:
                reply.content = f"Hello, {msg.actual_user_nickname} from {msg.from_user_nickname}"
            else:
                reply.content = f"Hello, {msg.from_user_nickname}"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

        elif content == "Hi":
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = "Hi"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK  # 事件结束，进入默认处理逻辑，一般会覆写reply

        elif content == "End":
            # 如果是文本消息"End"，将请求转换成"IMAGE_CREATE"，并将content设置为"The World"
            e_context["context"].type = ContextType.IMAGE_CREATE
            content = "The World"
            e_context.action = EventAction.CONTINUE  # 事件继续，交付给下个插件或默认逻辑

    def get_func_help_tips(self,**kwargs):
        func_help_tips = "📚 功能支持关键词获取信息，购物链接匹配，AI对话！"

        # 娱乐和信息类
        func_help_tips += "\n🎉 娱乐与资讯：\n"
        func_help_tips += "  🌅 早报: 发送“早报”获取早报。\n"
        func_help_tips += "  🐟 摸鱼: 发送“摸鱼”获取摸鱼人日历。\n"
        func_help_tips += "  🔥 热榜: 发送“xx热榜”查看支持的热榜。\n"
        func_help_tips += "  🔥 八卦: 发送“八卦”获取明星八卦。\n"
        func_help_tips += "  🔥 笑话: 发送“笑话”获取搞笑段子。\n"

        # 查询类
        func_help_tips += "\n🔍 查询工具：\n"
        func_help_tips += "  🌦️ 天气: 发送“城市+天气”查天气，如“北京天气”。\n"
        func_help_tips += "  📦 快递: 发送“快递+单号”查询快递状态。如“快递112345655”\n"
        func_help_tips += "  🌌 星座: 发送星座名称查看今日运势，如“白羊座”。\n"
        
        #购物类
        func_help_tips += "\n🛒 购物券下单："
        func_help_tips += "\n🛍️ 拼多多app商品分享下单获取返利，超级红包领取。"
        func_help_tips += "\n💳 京东app商品分享下单获取返利。"
        func_help_tips += "\n💰 淘宝天猫app商品链接适配中。"

        #购物类关键词
        func_help_tips += "\n  购物类关键词："
        func_help_tips += "\n  京东订单查询：发送“数字订单号”，获取订单返利信息。"
        func_help_tips += "\n  拼多多超级红包：发送“超级红包”，获取拼多多每日红包信息"

        #AI对话
        func_help_tips += " \n  支持AI聊天，@智能助手 提问聊天 \n"
        return func_help_tips
    def get_help_text(self, **kwargs):
        help_text = "输入Hello，我会回复你的名字\n输入End，我会回复你世界的图片\n"
        return help_text

    def _load_config_template(self):
        logger.debug("No Hello plugin config.json, use plugins/hello/config.json.template")
        try:
            plugin_config_path = os.path.join(self.path, "config.json.template")
            if os.path.exists(plugin_config_path):
                with open(plugin_config_path, "r", encoding="utf-8") as f:
                    plugin_conf = json.load(f)
                    return plugin_conf
        except Exception as e:
            logger.exception(e)