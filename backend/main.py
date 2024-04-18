from fastapi import Depends, FastAPI
import uvicorn
from core.events import close_orm, init_orm
from core.exceptions import exception_handlers
from core.middleware import middlewares
from core.security import check_permissions
from core.utils import load_routers

# [step n]若需要，创建异步定时任务，新建service.schedulers文件，并实现async fun job函数
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from service.schedulers import job1
# # 创建异步调度器
# scheduler = AsyncIOScheduler()
# # 添加异步定时任务，这里每隔 5 秒执行一次 job 函数
# scheduler.add_job(job1, 'interval', seconds=5)
# # 启动调度器
# scheduler.start()


app = FastAPI(
    on_startup=[init_orm],
    on_shutdown=[close_orm],
    middleware=middlewares,
    exception_handlers=exception_handlers,
)
# [step 1]在route下添加一个文件xxx，并添加一个url接口
# [step 2]设定路由xxx是否‘no_depends’
load_routers(app, "router", no_depends=["auth"], depends=[Depends(check_permissions)])

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
