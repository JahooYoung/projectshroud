import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/event',
      name: 'event',
      // route level code-splitting
      // this generates a separate chunk (event.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "event" */ './views/Event.vue')
    },
    {
      path: '/event/:id',
      name: 'eventDetail',
      component: () => import(/* webpackChunkName: "event" */ './views/EventDetail.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import(/* webpackChunkName: "login" */ './views/Login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import(/* webpackChunkName: "register" */ './views/Register.vue')
    // },
    // {
    //   path: '*',
    //   component: () => import(/* webpackChunkName: "notfound" */ './views/NotFound.vue')
    }
  ]
})
