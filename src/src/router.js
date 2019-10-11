import Vue from 'vue'
import Router from 'vue-router'
import Modeselektor from './views/Modeselektor.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'modeselektor',
      component: Modeselektor
    },
    {
      path: '/modeselektor',
      name: 'modeselektor',
      component: Modeselektor
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    },
    {
      path: '/live',
      name: 'live',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/Live.vue')
    },
    {
      path: '/control',
      name: 'control',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/Control.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/Admin.vue')
    }
  ]
})
