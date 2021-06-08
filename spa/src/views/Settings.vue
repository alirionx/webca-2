<template>
  <div class="settings">
    <div class="settingsCard" v-bind:class="{ inactive: userEditDisabled }">
      <img src="@/assets/icon_tool.svg" class="editIcon" v-if="userEditDisabled" @click="user_edit_switch" />
      <img src="@/assets/icon_hook.svg" class="editIcon" v-if="!userEditDisabled" @click="user_edit_submit" />
    
    <form @submit.prevent="user_edit_submit">
      <div class="hl">Your Account Settings</div>
      <div class="iptHl">Username</div>
      <input type="text" disabled required v-model="userData.username" />
      
      <div class="iptHl">Email Address</div>
      <input type="email" :disabled="userEditDisabled" required v-model="userData.email" />

      <div class="iptHl">Firstname</div>
      <input type="text" :disabled="userEditDisabled" v-model="userData.firstname" />

      <div class="iptHl">Lastname</div>
      <input type="text" :disabled="userEditDisabled" v-model="userData.lastname" />

      <div class="iptHl">Department</div>
      <input type="text" :disabled="userEditDisabled" v-model="userData.department" />
    </form>
      
    <form  @submit.prevent="pwd_change_submit">
      <table class="pwdTable" v-if="!userEditDisabled&&enablePwdChange"><tr>
        <td>
          <input type="password" required pattern="^.{6,}$" placeholder="current password" v-model="pwdData.curPwd" />
        </td>
          <input type="password" required pattern="^.{6,}$" placeholder="new password" v-model="pwdData.newPwd" />
        <td>
        </td>
          <input type="password" required pattern="^.{6,}$" placeholder="repeate new password" v-model="pwdData.repPwd" />
        <td>
        </td>
      </tr></table>

      <div class="btnFrame">
        <button 
          class="smlBtn" 
          type="submit"
          v-if="!userEditDisabled&&enablePwdChange"
        >submit</button>
        
        <button 
          class="smlBtn"
          type="button"
          v-if="!userEditDisabled&&!enablePwdChange"  
          @click="()=>{this.enablePwdChange=true;}"
        >change password</button>

        <button 
          class="smlBtn"
          type="button"
          v-if="!userEditDisabled&&enablePwdChange"  
          @click="()=>{this.enablePwdChange=false;}"
        >cancel</button>
      
      </div>
    </form>
    <div class="gradianBlender" v-if="userEditDisabled"></div>
    </div>

    <div class="settingsCard">
      <div class="hl">Admin Options</div>

      <table class="mainTbl"><tr>
        <td>
          <img v-if="resetDisabled" src="@/assets/icon_power.svg" class="mainIco" @click="switch_reset" />
          <img v-if="!resetDisabled" src="@/assets/icon_x.svg" class="mainIco" @click="switch_reset" />
        </td>
        <td>
          <span v-if="resetDisabled">Reset the Application</span>
          <div class="optSelector" v-if="!resetDisabled">
            <label class="switch">
              <input type="checkbox" v-model="resetCerts">
              <span class="slider round"></span>
            </label>
            <span>Delete all Certificate files???</span>
          </div>
        </td>
        <td v-if="!resetDisabled">
          <img src="@/assets/icon_hook.svg" class="mainIco" @click="call_reset" />
        </td>
      </tr></table>

    </div>

  </div>
</template>

<script>
import store from '../store'
const axios = require('axios');

export default {
  name: 'Settings',
  components: {
    //HelloWorld
  },
  data(){
    return{
      userEditDisabled: true,
      resetDisabled: true,
      resetCerts:false,
      enablePwdChange: false,
      userData:{
        username: null,
        email: null,
        firstname: null,
        lastname: null,
        department: null,
      },
      pwdData:{
        curPwd: null,
        newPwd: null,
        repPwd: null,
      }
    }
  },
  methods:{
    setting_data_call(){
      axios.get('/api/settings')
      .then((response)=> {
        console.log(response.data);
        this.userData = response.data.data.userData;
        this.tmpUserData = JSON.parse(JSON.stringify(this.userData) );

      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to call settings data from API: " + err.response.data.msg;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      })
    },

    user_edit_switch(){
      if(this.userEditDisabled){
        this.userEditDisabled=false;
      }
      else{
        this.userEditDisabled=true;
      }
    },
    user_edit_submit(){
      // console.log(this.userData);
      // console.log(this.tmpUserData);
      if(JSON.stringify(this.userData) == JSON.stringify(this.tmpUserData)){
        this.userEditDisabled = true;
        this.enablePwdChange = false;
        return;
      }
      axios.put('/api/settings/user', this.userData, ).then(response => { 
        console.log(response.data);
      })
      .catch(error => {
        //this.loader = false;
        this.userData = this.tmpUserData;
        console.log(error);
        this.$store.state.sysMsg = "Failed to change user Account Settings: "+error.response.data.msg;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
      this.userEditDisabled = true;
      this.enablePwdChange = false;
    },

    pwd_change_submit(){
      if(this.pwdData.newPwd != this.pwdData.repPwd){
        this.$store.state.sysMsg = "Passwords don't match! Try again.";
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
        this.pwdData.newPwd = null;
        this.pwdData.repPwd = null;
        return;
      }

      axios.put('/api/settings/pwd', this.pwdData, ).then(response => { 
        console.log(response.data);
        this.enablePwdChange = false;
      })
      .catch(error => {
        console.log(error);
        this.$store.state.sysMsg = "Failed to change password: "+error.response.data.msg;;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
      this.pwdData.curPwd = null;
      this.pwdData.newPwd = null;
      this.pwdData.repPwd = null;
    },

    switch_reset(){
      if(this.resetDisabled){
        this.resetDisabled=false;
      }
      else{
        this.resetDisabled=true;
      }
    },
    call_reset(){
      this.$store.state.sysConfirmMsg = "Do you really want to reset the application";
      this.$store.state.sysConfirmFw = ()=>{this.do_reset()};
    },
    do_reset(){
      const data = {resetCerts: this.resetCerts};
      axios.post('/api/settings/reset', data, ).then(response => { 
        console.log(response.data);
        this.do_logout();
      })
      .catch(error => {
        console.log(error);
        this.$store.state.sysMsg = "Failed to reset the application: "+error.response.data.msg;;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
    },
    do_logout(){
      axios.post('/api/logout', {}, ).then(response => { 
        console.log(response.data);
        this.$store.commit("reset_username_role");
        location.hash = "/login"
      })
      .catch(error => {
        console.log(error);
      });
    }

    
  },
  created: function(){
    this.setting_data_call();
  },
  mounted: function(){
    //console.log("Settings mounted");
  }

}
</script>

<style scoped>
.optSelector span{
  padding-left:12px;
}
</style>