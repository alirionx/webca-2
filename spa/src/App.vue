<template>
  <div class="headBlock">
    <div class="headLine">
      Web-based Certificate Authority Administration
    </div>
    <NavMenu v-if="$store.state.role" />
  </div>
  
  <div class="msgPop" v-if="$store.state.sysMsg">
    <div class="box">
      {{$store.state.sysMsg}}
      <div class="xBtn" @click="$store.commit('reset_sys_msg')">X</div>
    </div>
  </div>

  <router-view />
</template>

<script>
//import axios from 'axios'
import store from './store'
import NavMenu from './components/NavMenu.vue'

export default {
 name: 'App',
  components:{
    NavMenu
  },
  data(){
    return{
      name: "App"
    }
  },
  methods:{

  },
  mounted: function(){
    store.dispatch("check_user_state");
  }
}

</script>

<style>
@import './assets/styles/app.css';
</style>
