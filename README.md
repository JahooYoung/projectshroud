# projectshroud

## 说明

- 前端采用vue.js，暂定做单页应用

- 后端采用Django+django rest framework
- 前后端通信使用RESTful api

## 使用

### 环境

1. 建议使用virtualenv
2. `pip install Django djangorestframework`
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

### Entities

- User
  - registered_events[]
  - attended_events[]
  - unattended_events()
  - //friends[]
- Event
  - title
  - description
  - start_time
  - end_time
  - created_time
  - location
  - event_admin[]
  - registered_user[]
  - signed_user[]
- SuperEvent
  - event[]