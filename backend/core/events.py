from tortoise import Tortoise

TORTOISE_ORM = {
    "connections": {"default": "sqlite://mini.db"},
    "apps": {
        "models": {
            "models": ["models","aerich.models"],
            "default_connection": "default",
        },
    },
}
#
#mysql
# TORTOISE_ORM = {
#     #fastgpt%40mysql --> fastgpt@mysql
#     "connections": {"default": "mysql://gpt:fastgpt%40mysql@193.134.211.28:6033/fastgpt"},
#     "apps": {
#         "models": {
#             "models": ["models","aerich.models"],
#             "default_connection": "default",
#             },
#     },
# }
# [step n]添加数据库管理，新增pyproject.toml文件后，可以用以下命令更新同步数据库
# aerich init-db
# aerich migrate --name xxxxxx
# aerich upgrade
async def init_orm():
    """初始化orm"""
    # await Tortoise.init(db_url="sqlite://mini.db", modules={"models": ["models"]})
    await Tortoise.init(config = TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_orm():
    """关闭orm"""
    await Tortoise.close_connections()
