<template>
  <div class="headBlock">
    <div class="headLine">
      Web-based Certificate Authority Administration
    </div>
    <NavMenu />
  </div>
  <h2 v-if="$store.state.sysMsg">{{$store.state.sysMsg}}</h2>
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
