
**目录**（点击跳转到对应位置）

- [**订单处理-Django服务**](#订单处理-django服务)
  - [代码结构](#代码结构)
  - [依赖环境](#依赖环境)
  - [部署指南](#部署指南)
    - [环境配置](#环境配置)
    - [项目部署](#项目部署)
  - [使用指南](#使用指南)
    - [接口一：模拟数据源](#接口一模拟数据源)
    - [接口二：通过用户id获取用户订单历史](#接口二通过用户id获取用户订单历史)
    - [接口三：按skuId查询从下单到实际付款概率](#接口三按skuid查询从下单到实际付款概率)
    - [接口四：按时段获得成交量最高的sku top10](#接口四按时段获得成交量最高的sku-top10)

---

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

### 环境配置

> **会django配置或已有django环境可跳过此步骤**

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

### 项目部署

1. 确认服务器安全组**已开放8000端口**（出入站均设置开放）
   
2. **下载代码**，将代码拉取到本地，并在命令行中cd进代码目录中

3. **设置允许外部访问**  打开settings.py，找到以下代码(约在28行)：
```
ALLOWED_HOSTS = '101.35.191.114', 'localhost', '127.0.0.1'
```
将其修改为:
```
ALLOWED_HOSTS = ['你的部署服务器IP', 'localhost', '127.0.0.1']
```

4. 启动django服务，执行：
```
python manage.py runserver 0.0.0.0:8000
```

## 使用指南

### 接口一：模拟数据源

调用方式：post

参数：无

url：http://部署的服务器IP:8000/add

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

```
1. 
{
    "data":{},
    "succeed":true,
    "msg":"新增订单数据成功，当前订单数：12"
}

2.
{
    "data":{},
    "succeed":true,
    "msg":"已存在orderId=1的订单，订单数据修改成功！，当前订单数：12"
}
```

> 错误信息实例

```
{
    "data":{},
    "succeed":false,
    "msg":"您的请求提交不正确或提交格式错误，请检查！"
}
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
![Image text](https://github.com/FTLIKON/OrderProcess/blob/main/imgs/QQ%E5%9B%BE%E7%89%8720220223001842.png)

---

### 接口二：通过用户id获取用户订单历史

调用方式：get

参数：userId

说明：返回对应用户的所有完整订单信息

url：http://部署的服务器IP:8000/user_orders?userId=1

> 成功信息实例：

```
{
    "data":{
        "user_orders":[
            {
                "orderId":2,
                "orderTime":111,
                "skuId":4566,
                "userId":1,
                "status":0,
                "price":45.23,
                "pay":45.12
            }
        ]
    },
    "succeed":true,
    "msg":"已成功查询到用户订单数量：1"
}
```

> 错误信息实例

```
{
    "data":{},
    "succeed":false,
    "msg":"您的请求提交不正确或提交格式错误，请检查！"
}
```

get接口可以直接在浏览器输入url请求。

---

### 接口三：按skuId查询从下单到实际付款概率

调用方式：get

参数：skuId

说明：返回对应商品的skuId，订单量，成交订单量，付款率

url：http://部署的服务器IP:8000/pay_rate?skuId=4566

> 成功信息实例：

```
{
    "data":{
        "skuId":"4566",
        "order_num":9,
        "pay_num":5,
        "pay_rate":0.5555555555555556
    },
    "succeed":true,
    "msg":"已成功查询到skuId=4566的订单共有9个，其中已付款5个，实际付款率为0.5555555555555556（付款数/订单总数）"
}
```

> 错误信息实例

```
1.
{
    "data":{},
    "succeed":false,
    "msg":"您的请求提交不正确或提交格式错误，请检查！"
}

2.
{
    "data":{},
    "succeed":false,
    "msg":"未查询到该skuId"
}
```

---

### 接口四：按时段获得成交量最高的sku top10

调用方式：get

参数：时间区间。starttime：开始时间，endtime：结束时间

说明：提取时间区间内的所有订单，判断每个商品对应的成交订单，进行排序取TOP10

url：http://部署的服务器IP:8000/get_top?starttime=0&endtime=9999

> 成功信息实例：

```
{
    "data":{
        "top10_skuId":[
            "123",
            "4566"
        ]
    },
    "succeed":true,
    "msg":"已成功获取并分析从0到9999的共12个订单，共2个成交的skuId，已按正序已列出成交额top10的skuId."
}
```

> 错误信息实例

```
{
    "data":{},
    "succeed":false,
    "msg":"您的请求提交不正确或提交格式错误，请检查！"
}
```

