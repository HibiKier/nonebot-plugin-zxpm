<div align=center>

<img width="250" height="312" src="https://github.com/HibiKier/nonebot-plugin-zxpm/blob/main/docs_image/tt.jpg"/>

</div>

<div align="center">

<p>
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/plugin.svg" alt="NoneBotPluginText">
</p>

# nonebot-plugin-zxpm

_✨ 基于 [NoneBot2](https://github.com/nonebot/nonebot2) 的一个 插件管理插件 ✨_

![python](https://img.shields.io/badge/python-v3.9%2B-blue)
![nonebot](https://img.shields.io/badge/nonebot-v2.1.3-yellow)
![onebot](https://img.shields.io/badge/onebot-v11-black)
[![license](https://img.shields.io/badge/license-AGPL3.0-FE7D37)](https://github.com/HibiKier/zhenxun_bot/blob/main/LICENSE)

</div>

## 📖 介绍

[小真寻](https://github.com/HibiKier/zhenxun_bot) 的插件权限管理系统，提供了

- **细致的插件开关**
- **Ban 群组/用户（消息屏蔽）**
- **插件 Cd，Count，Block 限制**
- 群管监测(权限自动设置)
- 用户权限设置(超级用户设置)
- 一个简单的帮助查看

继承了真寻的优良传统，高贵的**超级用户**不受权限控制，除非插件额外限制

> [!NOTE]
>
> <div align="center"><b>小真寻也很可爱呀，也会很喜欢你！</b></div>
>
> <div align="center"><img width="250" height="250" src="https://github.com/HibiKier/nonebot-plugin-zxpm/blob/main/docs_image/tt3.png"/><img width="250" height="250" src="https://github.com/HibiKier/nonebot-plugin-zxpm/blob/main/docs_image/tt1.png"/><img width="250" height="250" src="https://github.com/HibiKier/nonebot-plugin-zxpm/blob/main/docs_image/tt2.png"/></div>

## 💿 安装

```python
pip install nonebot-plugin-zxpm
```

```python
nb plugin install nonebot-plugin-zxpm
```

## 🎁 使用

> [!IMPORTANT]
> ZXPM 对插件进行了分类  
> `NORMAL`: 普通插件，没有特定标记的情况下都为这个类型  
> `ADMIN`: 管理员权限用户插件  
> `SUPERUSER`: 插件用户插件  
> `SUPER_AND_ADMIN`: 超级用户用于与管理员插件  
> `DEPENDANT`: 依赖插件，一般为没有主动触发命令的插件，受权限控制  
> `HIDDEN`: 隐藏插件，一般为没有主动触发命令的插件，不受权限控制，如消息统计  
> `PARENT`: 父插件，仅仅标记
>
> ZXPM 权限管理严格  
> 普通用户无法查看`ADMIN`，`SUPERUSER`，`SUPER_AND_ADMIN`插件的帮助  
> 权限管理员用户无法查看`SUPERUSER`插件的帮助

## 配置

| 配置                    | 类型 |        默认值        | 说明                                                |
| :---------------------- | :--: | :------------------: | --------------------------------------------------- |
| zxpm_db_url             | str  | data/zxpm/db/zxpm.db | 数据库地址，默认为 sqlite                           |
| zxpm_notice_info_cd     | int  |         300          | 群/用户权限检测等各种检测提示信息 cd，为 0 时不提醒 |
| zxpm_ban_reply          | str  |  才不会给你发消息.   | 用户被 ban 时回复消息，为空时不回复                 |
| zxpm_ban_level          | int  |          5           | 使用 ban 功能的对应权限                             |
| zxpm_switch_level       | int  |          1           | 使用开关功能的对应权限                              |
| zxpm_admin_default_auth | int  |          5           | 群组管理员默认权限                                  |
| zxpm_font               | str  |       msyh.ttc       | 作图时字体                                          |

## 帮助

| 指令 | 格式 | 权限等级 | 参数 | 作用                     | 示例                                                                                                                                                 |
| :--: | :--: | :------: | :--: | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| zxpm | zxpm |    0     |  -s  | 提供一个简单详情帮助图片 | `zxpm Ban`: 查看 Ban 的用户帮助 <br> `zxpm Ban -s`: 查看 Ban 的超级用户帮助<br>`zxpm 40`: 查看 id 为 40 的插件帮助(id 通过给 bot 发送`插件列表`获取) |

> [!NOTE]
> 这里的指令只是写了个大概，功能开关指令比较复杂
> 建议对 bot 发送 `zxpm ZXPM插件管理` 和 `zxpm ZXPM插件管理 -s` 来查看详细帮助
> ZXPM 内部维护了一个插件数据库，收集所有含有`PluginMetaData`的插件
> 对于其他插件，同样也可以使用`zxpm`来获取帮助信息

## 权限设置

|   指令   |         格式          | 权限等级  | 参数 | 作用                     | 示例               |
| :------: | :-------------------: | :-------: | :--: | ------------------------ | ------------------ |
| 添加权限 | 添加权限 [level] [at] | SUPERUSER |      | 为用户提供插件管理等权限 | `添加权限 5 @user` |
| 删除权限 |     删除权限 [at]     | SUPERUSER |      | 为用户提供插件管理等权限 | `删除权限 @user`   |

## Ban/unBan

**群组管理员**

| 指令  |               格式               | 权限等级  | 参数  | 作用                                                | 示例                                                   |
| :---: | :------------------------------: | :-------: | :---: | --------------------------------------------------- | ------------------------------------------------------ |
|  Ban  | ban [At 用户] ?[-t [时长(分钟)]] |     5     | -t -g | 屏蔽用户或群组消息，权限等级低无法 Ban 等级高的用户 | `ban @用户`: 永久 ban<br>`ban @用户 -t 10`: ban 十分钟 |
| unBan |         unban [At 用户]          | SUPERUSER |       | 接触蔽用户或群组消息 @user                          | `unban @用户`: 放出来                                  |

**超级用户**

```
ban [At用户/用户Id] ?[-t [时长]]
unban --id [idx]  : 通过id来进行unban操作
ban列表: 获取所有Ban数据

群组ban列表: 获取群组Ban数据
用户ban列表: 获取用户Ban数据

ban列表 -u [用户Id]: 查找指定用户ban数据
ban列表 -g [群组Id]: 查找指定群组ban数据
示例:
    ban列表 -u 123456789    : 查找用户123456789的ban数据
    ban列表 -g 123456789    : 查找群组123456789的ban数据

私聊下:
    示例:
    ban 123456789          : 永久拉黑用户123456789
    ban 123456789 -t 100   : 拉黑用户123456789 100分钟

    ban -g 999999              : 拉黑群组为999999的群组
    ban -g 999999 -t 100       : 拉黑群组为999999的群组 100分钟

    unban 123456789     : 从小黑屋中拉出来
    unban -g 999999     : 将群组9999999从小黑屋中拉出来
```

## 插件控制

**群组管理员**

```
格式:
开启/关闭[功能名称]   : 开关功能
开启/关闭所有插件     : 开启/关闭当前群组所有插件状态
醒来                 : 结束休眠
休息吧               : 群组休眠, 不会再响应命令

示例:
开启签到              : 开启签到
关闭签到              : 关闭签到
```

**超级用户**

```
插件列表
开启/关闭[功能名称] ?[-t ["private", "p", "group", "g"](关闭类型)] ?[-g 群组Id]

开启/关闭插件df[功能名称]: 开启/关闭指定插件进群默认状态
    = 开启插件echo -df
    = 关闭插件echo -df
开启/关闭所有插件df: 开启/关闭所有插件进群默认状态
开启/关闭所有插件:
    私聊中: 开启/关闭所有插件全局状态
    群组中: 开启/关闭当前群组所有插件状态

私聊下:
    示例:
    开启签到                : 全局开启签到
    关闭签到                : 全局关闭签到
    关闭签到 -t p           : 全局私聊关闭签到
    关闭签到 -g 12345678    : 关闭群组12345678的签到功能(普通管理员无法开启)
```

**可修改配置文件**

在`data/zxpm/configs`路径下有以下 3 个配置文件，且文件中已提供参数解释

- `plugin2block.yaml`: 插件阻塞配置
  例如:

  ```
  zhenxun.builtin_plugins.sign_in:
    status: true
    check_type: ALL
    watch_type: USER
    result: "你签那么快干什么啦"
  ```

- `plugin2cd.yaml`: 插件 CD 配置
  例如:

  ```
  zhenxun.builtin_plugins.sign_in:
    status: true
    check_type: ALL
    watch_type: USER
    result: 告辞
    cd: 12
  ```

- `plugin2count.yaml`: 插件每日次数配置
  例如：

  ```
    zhenxun.builtin_plugins.help:
    status: false
    watch_type: GROUP
    result: 再看就揍死你
    max_count: 2
  ```

## ❤ 感谢

- 可爱的小真寻 Bot [`zhenxun_bot`](https://github.com/HibiKier/zhenxun_bot): 我谢我自己，桀桀桀
