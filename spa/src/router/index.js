import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    login: true
  },
  {
    path: '/login',
    name: 'Login',
    component: function () {
      return import('../views/Login.vue')
    },
    login: false
  },
  {
    path: '/cas',
    name: 'Cas',
    component: function () {
      return import('../views/Cas.vue')
    },
    login: true
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
