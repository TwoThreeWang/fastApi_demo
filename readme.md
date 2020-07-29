![](https://camo.githubusercontent.com/86dafd728b94c0e3c8f19a7295e87df678ed6751/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f6c6f676f2d6d617267696e2f6c6f676f2d7465616c2e706e67)

# FastApi_demo 

# 说明

本程序为使用 FastApi 创建的接口 DEMO，集成了用户管理功能和 TODO 示例功能，接口认证方式为 Token 认证，支持根据 token 的接口调用频率控制，默认用户接口调用频率为 600 次/分钟。

# 使用

1、程序默认使用 SQLite 数据库，数据库文件在 data/test.db，数据库配置信息在 sql_app/database.py

2、下载程序后可直接运行，默认管理员用户为 admin/123456

3、启动成功后访问 127.0.0.1:8000 返回以下信息即为成功
```
{
"message": "Hello World"
}
```

具体接口和说明请访问：http://127.0.0.1:8000/docs

# 启动方法

可使用以下任一方法启动：

1、终端执行以下命令

`uvicorn main:app --reload`

2、ide 直接运行 main.py 文件

3、Docker 运行

# 更新记录

v20200729. 增加基于 websocket 聊天室示例

v20200717. 增加接口频率限制，默认用户调用接口最大次数为 600 次/分钟