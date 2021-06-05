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
  name: 'Invitation',
  components: {
    //HelloWorld
  },
  data(){
    return{
      title: "Invitation for User Activation",
      data:{
        invitationHash:null,
        username: null,
        email: null,
        newPwd: null,
        repPwd: null,
      }
    }
  },
  methods:{
    call_invitation(){
      axios.get('/api/invitation/'+this.data.invitationHash)
      .then((response)=> {
        console.log(response.data);
        this.data.username = response.data.data.username;
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Invalid invitation hash";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
        this.go_login();
      })
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
      
      axios.post('/api/invitation', this.data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.$store.state.sysMsg = "Activation successfull! you can now login.";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
        this.go_login();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error);
        this.$store.state.sysMsg = "Failed activate user: "+error.response.data.msg;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
        this.data.email = null;
        this.data.newPwd = null;
        this.data.repPwd = null;
      });
    }

  },

  created: function(){
    this.data.invitationHash = this.$route.params.inviHash;
    this.call_invitation();
  }
}
</script>
