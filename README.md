# projectshroud

## TODOs and Pages
见[github projects](https://github.com/JahooYoung/projectshroud/projects/1)

## 说明

- 前端采用[Vue.js](https://cn.vuejs.org)，暂定做SPA(单页应用)。目前涉及的东西如下：
  - [Vue Router](https://router.vuejs.org/zh/) for SPA router
  - [Vuex](https://vuex.vuejs.org/zh/) for SPA global storage
  - [axios](https://github.com/axios/axios) for http request
  - [Font Awesome](http://fontawesome.dashgame.com) for icons
  - [algoliasearch](https://www.algolia.com) for search
  - [bootstrap-vue](https://bootstrap-vue.js.org) and [bootstrap](https://getbootstrap.com) for out-of-the-box components
  - [bootswatch](https://bootswatch.com) for bootstrap theming
  - [vue-amap](https://github.com/ElemeFE/vue-amap/) for location autocomplete
  - [vue-i18n](https://kazupon.github.io/vue-i18n/zh/) for internationalization
  - [vuelidate](https://vuelidate.netlify.com) for form validation
  - [husky](https://github.com/typicode/husky) and [lint-staged](https://github.com/okonet/lint-staged) for githooks
- 后端采用[Django](https://djangoproject.com) and [Django rest framework](https://www.django-rest-framework.org)。 目前涉及的东西有：
  - [algoliasearch](https://www.algolia.com) for search indexing
  - [MyQR](https://github.com/sylnsfar/qrcode) for QRcode generation
  - [Django Channels](https://channels.readthedocs.io/en/latest/index.html) for websocket
  - [Openpyxl](https://openpyxl.readthedocs.io/en/stable/) for Excel import/export
- 前后端通信使用[RESTful API](https://www.runoob.com/w3cnote/restful-architecture.html)，文档见[API_doc.md](./backend/API_doc.md)
- 服务器采用[Nginx](http://nginx.org/en/)

## 开发准备

### 环境

1. `git clone https://github.com/JahooYoung/projectshroud.git`
2. 安装[python(3.6或以上)](https://www.python.org/), [nodejs(LTS版)](https://nodejs.org), [yarn](https://yarnpkg.com/zh-Hant/), [redis](https://redis.io/)
3. 建议使用[Virtualenv](https://virtualenv.pypa.io/en/stable/)
4. `pip install -r requirements.txt`
5. 将`settings.py`（出于安全原因没有存放于git仓库中）移至`projectshroud/`子目录下，设置`DEBUG = True`
6. `(cd frontend; yarn install)`（前端依赖改了就要做一次）

### 数据库配置

1. 如果使用默认的SQLite，则直接下一步；如果使用MySQL，设置环境变量`DJANGO_DB=mysql`，`MYSQL_USER`和`MYSQL_PSW`为MySQL的用户名和密码，并创建一个名为`shrouddb`的数据库
2. `python manage.py makemigrations backend && python manage.py makemigrations && python manage.py migrate`

### 启动后端开发服务器

1. `python manage.py migrate` (数据模式变了就要做一次)
2. `cd frontend && yarn build && cd ..`（前端改了就要做一次）
3. `python manage.py runserver`
4. 浏览器访问`http://localhost:8000`

### 启动前端开发服务器

1. `cd frontend`
2. `yarn serve`
3. 浏览器访问`http://localhost:8080`

## 生产环境部署

1. 准备环境，见[环境](#环境)，并安装[Nginx](http://nginx.org/en/)
2. 构建前端文件：`(cd frontend; yarn build)`
3. 将`settings.py`（出于安全原因没有存放于git仓库中）移至`projectshroud/`子目录下，在其中设置`DEBUG = False`
4. 配置数据库
   1. 如果使用默认的SQLite，则直接下一步；如果使用MySQL，设置环境变量`DJANGO_DB=mysql`，`MYSQL_USER`和`MYSQL_PSW`为MySQL的用户名和密码，并创建一个名为`shrouddb`的数据库
   2. `python manage.py makemigrations backend && python manage.py makemigrations && python manage.py migrate`
5. 配置nginx：可参考[nginx.conf](deploy/nginx.conf)，注意修改
   1. 用户为当前登录的用户（第1行）
   2. `/path-to-projectshroud/`为你的`projectshroud`路径
   3. `/path-to-virtualenv/`为你的virtualenv的路径
   4. `ssl/`为你的https证书路径
6. 创建日志文件夹：`mkdir -p log deploy/daphne` 
7. 配置后端ASGI应用守护进程：修改`deploy/supervisord.conf`中的`/home/projectshroud/`你的`projectshroud`路径
8. 运行nginx：`sudo nginx`
9. 运行redis：`redis-server `（可通过修改redis配置文件来daemonize）
10. 运行ASGI应用：`supervisord -c ./deploy/supervisord.conf`

## 数据模式
见[models.py](./backend/models.py)

### 关于自定义UserProfile
使用非Django自带的User Model，必须作为整个项目的第一次migrations
若报错需删除数据库及`migrations`文件夹，然后`python manage.py makemigrations && python manage.py migrate`
