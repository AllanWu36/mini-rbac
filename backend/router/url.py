from typing import Any, Callable, get_type_hints

from fastapi import Depends, routing

from controller.common import about, login
from controller.menu import menu_add, menu_arr, menu_del
from controller.role import (
    assigned_menu,
    role_add,
    role_arr,
    role_del,
    role_has_menu,
    role_put,
    role_query,
)
from controller.user import user_add, user_arr, user_del, user_info, user_list, user_put
from core.security import check_token


class Route(routing.APIRoute):
    """
    https://github.com/tiangolo/fastapi/issues/620
    Django挂载视图方法
    def index() -> User:
        pass
    Route("/", endpoint=index)
    """

    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        tags: list[str],
        summary: str,
        **kwargs: Any
    ):
        if kwargs.get("response_model") is None:
            kwargs["response_model"] = get_type_hints(endpoint).get("return")
        super(Route, self).__init__(
            path=path, endpoint=endpoint, tags=tags, summary=summary, **kwargs
        )

    @classmethod
    def post(
        cls,
        path: str,
        endpoint: Callable[..., Any],
        tags: list[str],
        summary: str,
        **kwargs: Any
    ):
        return Route(
            path=path,
            endpoint=endpoint,
            methods=["POST"],
            tags=tags,
            summary=summary,
            **kwargs
        )

    @classmethod
    def get(
        cls,
        path: str,
        endpoint: Callable[..., Any],
        tags: list[str],
        summary: str,
        **kwargs: Any
    ):
        return Route(
            path=path,
            endpoint=endpoint,
            methods=["GET"],
            tags=tags,
            summary=summary,
            **kwargs
        )

    @classmethod
    def delete(
        cls,
        path: str,
        endpoint: Callable[..., Any],
        tags: list[str],
        summary: str,
        **kwargs: Any
    ):
        return Route(
            path=path,
            endpoint=endpoint,
            methods=["DELETE"],
            tags=tags,
            summary=summary,
            **kwargs
        )

    @classmethod
    def put(
        cls,
        path: str,
        endpoint: Callable[..., Any],
        tags: list[str],
        summary: str,
        **kwargs: Any
    ):
        return Route(
            path=path,
            endpoint=endpoint,
            methods=["PUT"],
            tags=tags,
            summary=summary,
            **kwargs
        )


routes = [
    Route.post("/login", endpoint=login, tags=["公共"], summary="登录"),
    Route.get("/about", endpoint=about, tags=["公共"], summary="关于"),
    #  用户管理
    Route.get("/user", endpoint=user_arr, tags=["用户管理"], summary="用户列表"),
    Route.post("/user", endpoint=user_add, tags=["用户管理"], summary="用户新增"),
    Route.delete(
        "/user/{pk}",
        endpoint=user_del,
        tags=["用户管理"],
        summary="用户删除",
    ),
    Route.put("/user/{pk}", endpoint=user_put, tags=["用户管理"], summary="用户更新"),
    Route.get("/user/{pk}", endpoint=user_info, tags=["用户管理"], summary="用户信息"),
    Route.post("/user/query", endpoint=user_list, tags=["用户管理"], summary="用户列表查询"),
    # 角色管理,
    Route.get("/role", endpoint=role_arr, tags=["角色管理"], summary="角色列表"),
    Route.post("/role", endpoint=role_add, tags=["角色管理"], summary="角色新增"),
    Route.delete(
        "/role/{pk}",
        endpoint=role_del,
        tags=["角色管理"],
        summary="角色删除",
        dependencies=[Depends(check_token)],
    ),
    Route.get(
        "/role/{rid}/menu", endpoint=role_has_menu, tags=["角色管理"], summary="查询角色拥有权限"
    ),
    Route.put("/role", endpoint=role_put, tags=["角色管理"], summary="角色更新"),
    Route.post("/role/query", endpoint=role_query, tags=["角色管理"], summary="角色条件查询"),
    Route.post(
        "/role/assigned/menu", endpoint=assigned_menu, tags=["角色管理"], summary="角色分配菜单"
    ),
    # 菜单新增
    Route.get("/menu", endpoint=menu_arr, tags=["菜单管理"], summary="菜单列表"),
    Route.post("/menu", endpoint=menu_add, tags=["菜单管理"], summary="菜单新增"),
    Route.delete(
        "/menu/{pk}",
        endpoint=menu_del,
        tags=["菜单管理"],
        summary="菜单删除",
        dependencies=[Depends(check_token)],
    ),
]

__all__ = [routes]
