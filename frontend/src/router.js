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
      path: '/event/new',
      name: 'newEvent',
      component: () => import(/* webpackChunkName: "eventadmin" */ './views/EventAdmin/Info.vue'),
      props: { newEvent: true }
    },
    {
      path: '/event/:id',
      name: 'eventDetail',
      component: () => import(/* webpackChunkName: "event" */ './views/EventDetail.vue')
    },
    {
      path: '/event/:id/admin',
      name: 'eventAdmin',
      component: () => import(/* webpackChunkName: "eventadmin" */ './views/EventAdmin/Layout.vue'),
      redirect: to => to.path + '/info',
      children: [
        {
          path: 'info',
          name: 'eventAdminInfo',
          component: () => import(/* webpackChunkName: "eventadmin" */ './views/EventAdmin/Info.vue')
        },
        {
          path: 'administrator',
          name: 'eventAdminAdministrator',
          component: () => import(/* webpackChunkName: "eventadmin" */ './views/EventAdmin/Administrator.vue')
        },
        {
          path: 'attendee',
          name: 'eventAdminAttendee',
          component: () => import(/* webpackChunkName: "eventadmin" */ './views/EventAdmin/Attendee.vue')
        },
        {
          path: 'checkin',
          name: 'eventAdminCheckin',
          component: () => import(/* webpackChunkName: "eventadmin" */ './views/EventAdmin/Checkin.vue')
        }
      ]
    },
    {
      path: '/registered-event',
      name: 'registeredEvent',
      component: () => import(/* webpackChunkName: "user" */ './views/UserRegisterEvent.vue')
    },
    {
      path: '/admin-event',
      name: 'adminEvent',
      component: () => import(/* webpackChunkName: "user" */ './views/UserAdminEvent.vue')
    },
    {
      path: '/checkin/:token',
      name: 'checkin',
      component: () => import(/* webpackChunkName: "checkin" */ './views/CheckIn.vue')
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
