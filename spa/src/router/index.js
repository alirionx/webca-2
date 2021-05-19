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
      roles: ["admin", "caadmin", "requester"]
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
    path: '/cas',
    name: 'Cas',
    component: function () {
      return import('../views/Cas.vue')
    },
    meta:{
      roles: ["admin"]
    }
  },

]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

router.beforeEach(async(to, from, next) =>{
  if(to.name == undefined){
    next({ name: 'Home' })
  }
  if(!store.state.role){
    await store.dispatch("check_user_state")
    //console.log(store.state.role)
  }
  if(to.name != "Login" && to.meta.roles!=undefined && !to.meta.roles.includes(store.state.role)){
    next({ name: 'Login' })
  }
  else{
    next()
  }
})

export default router
