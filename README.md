
# **订单处理-Django服务**

## 代码结构
```
README.md
OrderProcess/
    |dbModel/
        |__pycache__/
        |migrations
        |__init__.py
        |admin
        |apps
        |models --> 数据表设置文件
        |tests.py
        |views.py
    |OrderProcess/
        |__pycache__/
        |__init__.py
        |asgi.py
        |settings.py --> django设置文件
        |views.py --> 主后端代码文件
        |urls.py --> 接口设置文件
        |wsgi.py
    |db.sqlite3 --> 数据库文件
    |manage.py
```

## 依赖环境
- windows server 2016
- python 3.6.4
- Django 3.0.6
- jsonpath
- lxml


## 部署指南

<br />

### 环境配置

> **会django配置或已有django环境可跳过此步骤**

<br />

1. 确认服务器安全组**已开放8000端口**（出入站均设置开放）
2. 下载并安装python3【[Python安装环境 下载地址](https://www.python.org/downloads/)】
3. **安装django** 打开命令行，执行: (本项目安装的是django3.0.6,可根据需要使用其他版本)
```
python -m pip install Django==3.0.6 -i https://pypi.tuna.tsinghua.edu.cn/simple
```
4. **创建django初始项目** 命令行中，cd进想要创建django项目的目录，执行:
```
django-admin.py startproject OrderProcess
```
没有异常报错即为创建成功。会生成以下文件：
```
.../OrderProcess/
    |OrderProcess/
        |__init__.py
        |asgi.py
        |settings.py
        |urls.py
        |wsgi.py
    |manage.py
```
5. **设置允许外部访问**  打开settings.py，找到以下代码(约在28行)：
```
ALLOWED_HOSTS = []
```
将其修改为:
```
ALLOWED_HOSTS = ['部署的服务器IP', 'localhost', '127.0.0.1']
```
6. **启动项目** cd进有manage.py的目录下，执行：
```
python manage.py runserver 0.0.0.0:8000
```
命令行出现以下信息时，则为启动成功：
```
Django version 3.0.6, using settings 'wos_django.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.
```
7. 在浏览器访问地址：http://部署的服务器IP:8000/ ，出现django初始页则可正常访问
8. **关闭django服务** 在命令行按下ctrl+c即可
9. python与django运行环境已全部配置完成，可以开始项目部署。

<br />

### 项目部署

<br />

1. **下载代码**，将代码拉取到本地，并在命令行中cd进代码目录中

2. **设置允许外部访问**  打开settings.py，找到以下代码(约在28行)：
```
ALLOWED_HOSTS = []
```
将其修改为:
```
ALLOWED_HOSTS = ['部署的服务器IP', 'localhost', '127.0.0.1']
```

3. 启动django服务，执行：
```
python manage.py runserver 0.0.0.0:8000
```

<br />

## 使用指南

<br />

###　接口一：模拟数据源

调用方式：post

参数：add

url：http://你的IP:8000/wos_new?keyword=neurosciences

表单格式：
```json 
{
    "orderId": int // 订单id
    "orderTime": int // 下单时间
    "skuId": int // 商品id
    "userId": int // 用户id
    "status": int // 订单状态 (0待付款,1已付款,2取消)
    "price": double  // 价格
    "pay": double // 支付金额
}
```

> 成功信息实例：

```json 
1. {"data": {}, "succeed": true, "msg": "新增订单数据成功，当前订单数：12"}

2. {"data": {}, "succeed": true, "msg": "已存在orderId=1的订单，订单数据修改成功！，当前订单数：12"}
```

> 错误信息实例

```json
{"data": {}, "succeed": False, "msg": "您的请求提交不正确或提交格式错误，请检查！"}
```

post接口调用可参考以下python请求代码：
```python
import requests

url = "http://101.35.191.114:8000/add"

payload='{"orderId": 1,"orderTime": 111,"skuId": 4566,"userId": 4,"status": 1,"price": 55.23,"pay": 45.12}'
headers = {
  'Content-Type': 'text/plain'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```
也可使用postman等接口测试工具：
![Image text]()

<br />

