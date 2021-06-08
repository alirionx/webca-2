<template>

  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>
      
      <div class="iptHl">Username</div>
      <input type="text" disabled v-model="data.username" />
      
      <div class="iptHl">Your Email</div>
      <input type="email" required v-model="data.email" />

      <div class="iptHl">New Password</div>
      <input type="password" required placeholder="at least 6 characters" pattern="^.{6,}$" v-model="data.newPwd" />

      <div class="iptHl">Repeate new Password</div>
      <input type="password" required v-model="data.repPwd" />

      <div class="btnFrame">
        <button >Submit</button>
        <button type="button" @click="go_login">Cancel</button>
      </div>

    </div>
    </form>
      
  </div>
</template>

<script>
import store from '../store'
const axios = require('axios');
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Init',
  components: {
    //HelloWorld
  },
  data(){
    return{
      title: "Application Initialization",
      init: false,
      data:{
        username: null,
        email: null,
        newPwd: null,
        repPwd: null,
      }
    }
  },
  methods:{
    call_init_state(){
      axios.get('/api/settings/init')
      .then((response)=> {
        console.log(response.data);
        this.data.init = response.data.data.init;
        if(!this.data.init){
          this.call_inactive();
        }
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.call_inactive();
      })
    },

    call_inactive(){
      this.$store.state.sysMsg = "Initialization not available!";
      this.$store.dispatch("trigger_reset_sys_msg", 3000);
      this.go_login();
    },

    go_login(){
      location.hash = "/login";
    },

    submit(){
      //console.log(this.data);
      if(this.data.newPwd != this.data.repPwd){
        this.$store.state.sysMsg = "Passwords don't match! Try again.";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
        this.data.newPwd = null;
        this.data.repPwd = null;
        return
      }
      
      axios.post('settings/init', this.data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.$store.state.sysMsg = "Initialization successfull! you can now login.";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
        this.go_login();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error);
        this.$store.state.sysMsg = "Failed initialize the app: "+error.response.data.msg;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
        this.data.email = null;
        this.data.newPwd = null;
        this.data.repPwd = null;
      });
    }

  },

  created: function(){
    this.call_init_state();
  }
}
</script>
