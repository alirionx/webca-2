<template>
  <form @submit.prevent="submit" >
  <div class="stdForm">
    
    <div class="hl">WebUI Login</div>
    
    <input 
      type="text" class="txtCenter" 
      placeholder="Username" 
      v-model="username" 
      required />
    <input 
      type="password" class="txtCenter" 
      placeholder="Password" 
      v-model="password" 
      v-on:keyup.enter="submit" 
      required />

    <div class="btnFrame">
      <button>Submit</button>
    </div>

    <div id="initBtn" v-if="$store.state.init" @click="go_init">
      inititialize App
    </div>


  </div>
  </form>
</template>

<script>
import store from '../store'
const axios = require('axios');
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Login',
  components: {
    //HelloWorld
  },
  data(){
    return{
      username: "",
      password: "",
    }
  },
  methods:{
    submit(){
      //console.log(this.username, this.password);
      let data = {
        username: this.username,
        password: this.password
      }
      axios.post('/api/login/json', data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        location.hash = "/"
      })
      .catch(error => {
        //this.loader = false;
        //console.log(error);
        this.$store.state.sysMsg = "Login Failed";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
        this.username = "";
        this.password = "";
      });
    },

    go_init(){
      location.hash = '/init'
    }
  },
  created: function(){
    
  },
  mounted: function(){
    
  }

}
</script>


<style scoped>
#initBtn{
  position: fixed;
  bottom: 20px;
  right: 14px;
  padding:5px;
  margin: 0px 10px 0px 10px ;
  min-width: 140px;
  background-color: #eee;
  color:#000;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 14px;
  text-align: center;
  box-shadow: 0px 1px 2px #666;
}
#initBtn:hover{
  text-decoration: underline;
}
</style>

