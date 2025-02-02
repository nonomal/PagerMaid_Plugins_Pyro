from pagermaid.enums import AsyncClient, Message
from pagermaid.listener import listener


@listener(command="tel", description="手机号码归属地等信息查询。")
async def tel(message: Message, request: AsyncClient):
    if not (phone := message.arguments.strip()).isnumeric():
        return await message.edit("出错了呜呜呜 ~ 无效的参数。")
    message = await message.edit("获取中 . . .")  # type: ignore
    res = await request.post("https://tenapi.cn/v2/phone", params={"tel": phone})
    data = None
    if res.is_success and (data := res.json())["code"] == 200:
        data = data["data"]
        await message.edit(
            f"查询目标: {phone}\n"
            f"地区: {data['local']}\n"
            f"号段: {data['num']}\n"
            f"卡类型: {data['type']}\n"
            f"运营商: {data['isp']}\n"
            f"通信标准: {data['std']}"
        )
    else:
        await message.edit(
            "出错了呜呜呜 ~ API 服务器返回了错误。" + ("\n" + data.get("msg") if data else "")
        )
