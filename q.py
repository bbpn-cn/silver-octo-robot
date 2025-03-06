"""温馨提示：不得用于非法用途！！！仅用于查询QQ信息"""
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import aiohttp
import asyncio

@register("qq查询", "Your Name", "QQ信息查询插件，仅限合法使用", "1.0.0", "repo url")
class QQQueryPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def fetch_qq_info(self, session, qq_number):
        """调用API查询QQ信息"""
        url = f"https://api.xywlapi.cc/qqcx2023?qq={qq_number}"
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            return {"status": 500, "message": f"查询失败：{str(e)}"}

    @filter.command("q反")
    async def qq_query(self, event: AstrMessageEvent):
        '''QQ信息查询指令，使用格式：/q反 <QQ号>
        示例：/q反 2388489710'''
        raw_message = event.message_str.strip()
        args = raw_message.split()

        # 如果参数不足，显示帮助信息
        if len(args) < 1 or (len(args) == 1 and args[0] == "q反"):
            yield event.plain_result("使用格式：/q反 <QQ号>\n示例：/q反 2388489710")
            return

        # 提取QQ号（移除命令部分）
        if args[0] == "q反":
            if len(args) < 2:
                yield event.plain_result("请提供QQ号！使用格式：/q反 <QQ号>")
                return
            qq_number = args[1].strip()
        else:
            qq_number = args[0].strip()

        # 验证QQ号是否为纯数字
        if not qq_number.isdigit():
            yield event.plain_result("QQ号必须为纯数字，请检查输入！")
            return

        yield event.plain_result(f"正在查询QQ号 {qq_number} 的信息...")

        async with aiohttp.ClientSession() as session:
            result = await self.fetch_qq_info(session, qq_number)

            # 处理返回结果
            if result.get("status") == 200:
                output = [
                    "查询结果：",
                    f"  手机号：{result.get('phone', '未知')}",
                    f"  归属地：{result.get('phonediqu', '未知')}",
                    f"  LOL：{result.get('lol', '未知')}",
                    f"  微博：{result.get('wb', '未知')}"
                ]
                yield event.plain_result("\n".join(output))
            else:
                yield event.plain_result(f"查询失败：{result.get('message', '未知错误')}")

    async def terminate(self):
        '''插件卸载时调用'''
        pass