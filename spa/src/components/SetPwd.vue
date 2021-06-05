<template>
  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>

      <div class="iptHl">New Password</div>
      <input type="password" required pattern="^.{6,}$" placeholder="at least 6 characters" v-model="newPwd" />

      <div class="iptHl">Repeat Password</div>
      <input type="password" required pattern="^.{6,}$" placeholder="..." v-model="repPwd" />
     
      <div class="btnFrame">
        <button >Submit</button>
        <button type="button" @click="cb">Cancel</button>
      </div>

    </div>
    </form>
      
  </div>
</template>

<script>
const axios = require('axios');

export default {
  name: 'SetPwd',
  components: {

  },
  props:{
    usrObj: Object,
    cb: Function,
    //fw: Function
  },
  data(){
    return{
      title: "Set Password for user: "+this.usrObj.username,
      newPwd: null,
      repPwd: null,
    }
  },
  methods:{
    submit(){
      
      if(this.newPwd != this.repPwd){
        this.$store.state.sysMsg = "Password fields do not match. Try again...";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
        this.newPwd = null;
        this.repPwd = null;
        return false;
      }

      const data = {
        username: this.usrObj.username,
        password: this.newPwd 
      }

      axios.post('/api/user/pwd', data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        //this.fw();
        this.cb();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error);
        this.$store.state.sysMsg = "Failed to set password for user: " + this.usrObj.username;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
    },

  },
  created: function(){

  },
  mounted: function(){
    
  }

}
</script>


