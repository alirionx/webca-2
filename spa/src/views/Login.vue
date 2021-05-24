<template>
  <form @submit.prevent="submit">
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
    }
  },
  created: function(){
    
  },
  mounted: function(){
    
  }

}
</script>
