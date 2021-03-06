import { nextTick } from '@vue/runtime-core'
import { createRouter, createWebHashHistory } from 'vue-router'
import store from '../store'

import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta:{
      roles: ["admin", "caadmin" ]
    }
  },
  {
    path: '/init',
    name: 'Init',
    component: function () {
      return import('../views/Init.vue')
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: function () {
      return import('../views/Login.vue')
    }
  },
  {
    path: '/authorities',
    name: 'Authorities',
    component: function () {
      return import('../views/Authorities.vue')
    },
    meta:{
      roles: ["admin", "caadmin"]
    }
  },
  {
    path: '/requests',
    name: 'Requests',
    component: function () {
      return import('../views/Requests.vue')
    },
    meta:{
      roles: ["admin", "caadmin"]
    }
  },
  {
    path: '/requests/:caname',
    name: 'RequestsCa',
    component: function () {
      return import('../views/Requests.vue')
    },
    meta:{
      roles: ["admin", "caadmin"]
    }
  },
  {
    path: '/certificates',
    name: 'Certificates',
    component: function () {
      return import('../views/Certificates.vue')
    },
    meta:{
      roles: ["admin", "caadmin" ]
    }
  },
  {
    path: '/certificates/:caname',
    name: 'CertificatesCa',
    component: function () {
      return import('../views/Certificates.vue')
    },
    meta:{
      roles: ["admin", "caadmin" ]
    }
  },
  {
    path: '/users',
    name: 'Users',
    component: function () {
      return import('../views/Users.vue')
    },
    meta:{
      roles: ["admin"]
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: function () {
      return import('../views/Settings.vue')
    },
    meta:{
      roles: ["admin"]
    }
  },
  {
    path: '/invitation/:inviHash',
    name: 'Invitation',
    component: function () {
      return import('../views/Invitation.vue')
    },
    meta:{
      roles: ["admin", "caadmin" ]
    }
  },

]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

var noRouteChk = ["Init", "Login", "Invitation"]
router.beforeEach(async(to, from, next) =>{
  if(to.name == undefined){
    next({ name: 'Home' })
  }
  if(!store.state.role){
    await store.dispatch("check_user_state")
    //console.log(store.state.role)
  }
  //if(to.name != "Login" && to.meta.roles!=undefined && !to.meta.roles.includes(store.state.role)){
  if( !noRouteChk.includes(to.name) && !store.state.role){
    next({ name: 'Login' })
  }
  else{
    next()
  }
})

export default router
