import { defineStore } from 'pinia'
import { message } from 'ant-design-vue'
import router from '@/router'
import dayjs from 'dayjs'
import { loadRouter, getPermissions } from '@/utils/loadCpn'
import { getMenus, getUserInfo, login, selectRole } from '@/apis/user'

export const userStore = defineStore('user', {
    state: () => {
        // 初始化加载用户菜单路由：防止刷新404
        // if (localStorage.getItem('userMenus')) {
        //     loadRouter(JSON.parse(localStorage.getItem('userMenus')))
        // }
        return {
            token: localStorage.getItem('token')
                ? localStorage.getItem('token')
                : '',
            userInfo: localStorage.getItem('userInfo')
                ? JSON.parse(localStorage.getItem('userInfo'))
                : {},
            userMenus: localStorage.getItem('userMenus')
                ? JSON.parse(localStorage.getItem('userMenus'))
                : [],
            permissions: localStorage.getItem('permissions')
                ? JSON.parse(localStorage.getItem('permissions'))
                : [],
            selectKey: localStorage.getItem('selectKey')
                ? JSON.parse(localStorage.getItem('selectKey'))
                : [],
            isLoading: localStorage.getItem('isLoading')
                ? JSON.parse(localStorage.getItem('isLoading'))
                : false,
            isPush: localStorage.getItem('isPush')
                ? JSON.parse(localStorage.getItem('isPush'))
                : false,
            callapse: localStorage.getItem('callapse')
                ? JSON.parse(localStorage.getItem('callapse'))
                : false,
        }
    },
    getters: {
        accessToken: (state) => 'Bearer ' + state.token,
    },
    actions: {
        increment() {
            this.count++
        },
        reset() {
            this.token = ''
            this.userInfo = {}
            this.userMenus = []
            this.permissions = []
            this.selectKey = []
            localStorage.clear()
        },
        async getUserData(uid) {
            const info = await getUserInfo(uid)
            this.userInfo = info.data
            // check user limit time is ok
            const limit_start = info.data.limit_start
                ? dayjs(info.data.limit_start)
                : ''
            const limit_end = info.data.limit_end
                ? dayjs(info.data.limit_end)
                : ''
            var currentTime = new Date()
            var hours = currentTime.getHours()
            var minutes = currentTime.getMinutes()
            if (limit_start) {
                if (hours < limit_start.hour()) {
                    localStorage.clear()
                    message.error('用户不在可用时间段内')
                    return
                } else if (hours === limit_start.hour()) {
                    if (hours < limit_start.minute()) {
                        localStorage.clear()
                        message.error('用户不在可用时间段内')
                        return
                    }
                }
            }
            if (limit_end) {
                if (hours > limit_end.hour()) {
                    localStorage.clear()
                    message.error('用户不在可用时间段内')
                    return
                } else if (hours === limit_end.hour()) {
                    if (minutes > limit_end.minute()) {
                        localStorage.clear()
                        message.error('用户不在可用时间段内')
                        return
                    }
                }
            }
            localStorage.setItem('userInfo', JSON.stringify(info.data))
            // 3. 获取权限信息
            const menus = await getMenus(info.data.roles[0].id)
            this.userMenus = menus.data
            localStorage.setItem('userMenus', JSON.stringify(menus.data))

            // 3.1 加载路由权限
            loadRouter(menus.data)

            // 3.2 加载按钮权限
            const [btnPermissions, firstMenu] = getPermissions(menus.data)
            this.permissions = btnPermissions
            localStorage.setItem('permissions', JSON.stringify(btnPermissions))

            // 3.2 默认打开菜单
            this.selectKey = [firstMenu.id]
            localStorage.setItem('selectKey', JSON.stringify([firstMenu.id]))
            // 4. 跳转路由
            if (firstMenu?.path) {
                router.push(firstMenu.path)
            } else {
                router.push('/main')
            }
            return true
        },
        async loginAction(data) {
            // 1. 登录
            const res = await login(data)
            this.token = res.data.token
            localStorage.setItem('token', res.data.token)
            const check = await this.getUserData(res.data.id)
            if (check) {
                // 弹框提示登录成功
                message.success('登录成功')
            }
        },
        loadRoleRouter() {
            loadRouter(this.userMenus)
        },
        async userSelectRole(rid) {
            await selectRole(rid)
            // 重新拿用户信息
            await this.getUserData(this.userInfo.id)
        },
        setCallapse(flag) {
            this.callapse = flag
            localStorage.setItem('callapse', flag)
        },
    },
})
