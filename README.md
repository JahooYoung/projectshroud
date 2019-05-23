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
- 前后端通信使用[RESTful API](https://www.runoob.com/w3cnote/restful-architecture.html)，文档见[API_doc.md](./backend/API_doc.md)
- 服务器采用[Nginx](http://nginx.org/en/)

## 开发准备

### 环境

1. 建议使用virtualenv
2. `pip install -r requirements.txt`
3. 安装[yarn](https://yarnpkg.com/zh-Hant/)
4. `cd frontend && yarn install`（前端依赖改了就要做一次）

### 启动后端开发服务器

1. `python manage.py migrate` (数据模式变了就要做一次)
2. `cd frontend && yarn build && cd ..`（前端改了就要做一次）
3. `python manage.py runserver`
4. 浏览器访问`http://localhost:8000`

### 启动前端开发服务器

1. `cd frontend`
2. `yarn serve`
3. 浏览器访问`http://localhost:8080`

## 数据模式
See [models.py](./backend/models.py)

### 关于自定义UserProfile
使用非Django自带的User Model，必须作为整个项目的第一次migrations
若报错需删除数据库及`migrations`文件夹，然后`python manage.py makemigrations && python manage.py migrate`