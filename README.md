# projectshroud

## 说明

- 前端采用vue.js，暂定做单页应用
- 后端采用Django+django rest framework
- 前后端通信使用RESTful api

## 使用

### 环境

1. 建议使用virtualenv
2. `pip install -r requirements.pip`
3. 安装[yarn](https://yarnpkg.com/zh-Hant/)
4. `cd frontend && yarn install`

### 启动后端开发服务器

1. `python manage.py migrate` (数据模式变了就要做一次)
2. `cd frontend && yarn build && cd ..`
3. `python manage.py runserver`
4. 访问`http://localhost:8000`

### 启动前端开发服务器

1. `cd frontend`
2. `yarn serve`
3. 访问`http://localhost:8080`

## 数据模式 
See `models.py`

### 关于自定义UserProfile
使用非Django自带的User Model，必须作为整个项目的第一次migrations  
若报错需删除数据库及`migrations`文件夹，然后`python manage.py makemigrations && python manage.py migrate`;
