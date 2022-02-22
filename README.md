
# **订单处理-Django服务**

## 代码结构
```
LLB_spider/wos_django/
    |wos_django/
        |__pycache__/
        |__init__.py
        |asgi.py
        |nk_get_vertify.py
        |lanzou_get_vertify.py
        |nk_new.py
        |settings.py
        |views.py
        |urls.py
        |wsgi.py
    |db.sqlite3
    |manage.py
```

## 依赖环境
- windows server 2016
- python3.6.4
- selenium【[selenium配置参考，点这里](https://zhuanlan.zhihu.com/p/372590832)】
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
django-admin.py startproject wos_django
```
没有异常报错即为创建成功。会生成以下文件：
```
.../wos_django/
    |wos_django/
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

<br />

### 项目部署

<br />

1. **替换代码** 将项目代码中的nk_get_vertify.py，lanzou_get_vertify.py，nk_new.py，urls.py移动至django目录（urls.py需要覆盖）

当前代码结构为：
```
.../wos_django/
    |wos_django/
        |__pycache__/
        |__init__.py
        |asgi.py
        |nk_get_vertify.py
        |lanzou_get_vertify.py
        |nk_new.py
        |settings.py
        |urls.py
        |wsgi.py
    |db.sqlite3
    |manage.py
```

2. cd进有nk_get_vertify.py的目录下，打开此代码。找到以下代码(约在33行)：
```
driver = webdriver.Chrome(executable_path=r"C:\Users\Administrator\Desktop\chromedriver.exe")
```
将其修改为:
```
driver = webdriver.Chrome(executable_path=r"您的chromedriver绝对路径，参考selenium配置")
```

然后修改lanzou_get_vertify.py的代码，修改内容（约在21行）同上。

3. 另外启动一个进程（可以另外新打开一个命令行窗口），启动nk_get_vertify.py:
```
python nk_get_vertify.py
```
可以看见selenium打开浏览器进入wos获取cookie和sid。待目录下生成vertify.txt后，即为成功。

4. 启动django服务，执行：
```
python manage.py runserver 0.0.0.0:8000
```

<br />

## 使用指南

<br />

调用方式：get

参数：keyword

url：http://你的IP:8000/wos_new?keyword=neurosciences

<br />

> 成功信息实例：

```json 
{
    "data":{
        "keywords":'neurosciences', //检索的关键词
        "published_year":[    //发布年份的统计结果(取最近20年)
            {
                "year":2000,    //年份
                "count":10    //数量
            }...],
            
        "document_type":[    //文献类型（取top10）
            {
                "type":"xxx",
                "count":
            }...],
            
        "wos_category":[    //Web of Science类别（取top20）
            {
                "category":'xxx',
                "count":11
            }...],
            
        "institution":[    //所属机构（取top20）
            {
                "name":'xxx',    //机构名称
                "count":11    //记录数
            }...],
            
        "journal":[    //出版物标题（期刊）（取top20）
            {
                "name":'xxx',    //期刊名称
                "count":11    //记录数
            }...],
            
        "fund_agency":[    //基金资助机构（取top20）
            {
                "name":'xxx',    //资助机构名称
                "count":11    //记录数
            }...],
            
        "researc_area":[    //研究方向（取top20）
            {
                "area":'xxx',    //研究方向名称
                "count":11    //记录数
            }...],
            
        "country":[//（取top20）
            {
                "name":"USA",    //国家名称
                "count":11    //记录数
            }...]
    },

    "succeed":true/false,
    "err_msg":"",//错误信息.succeed=false时填写    
}
```

> 错误信息实例

```json
1. {"data": {}, "succeed": False, "err_msg": "模拟器请求的登录态失效，请检查是否能进入wos"}

2. {"data": {}, "succeed": False, "err_msg": "您提交了空表单，或参数错误"}
```

<br />