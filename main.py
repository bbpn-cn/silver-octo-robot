"""简单的 /help 命令插件"""
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register

@register("help插件", "egg", "处理 /help 命令的插件", "9.9.9", "repo url")
class StartPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("help")
    async def help_command(self, event: AstrMessageEvent):
        '''处理 /start 命令'''
        yield event.plain_result
        ("🎉使用说明🎉
可用命令：
🎶/音乐 歌名
🎶/音乐热评 歌名
🐧/q反 qq号
👧/查询学生 xx学校 某某某")

    async def terminate(self):
        '''插件卸载时调用'''
        pass