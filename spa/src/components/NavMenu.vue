<template>
  <div class="menuBar">
    <div v-for="(opt, idx) in defi" :key="idx" >
      <div class="btn" 
        v-if="chk_show(idx)"
        @click="opt.func"
        v-bind:class="{ isActive: opt.lnk==$route.path || (opt.lnk!='/' && $route.path.includes(opt.lnk)), fst:idx==0 }" 
        >{{opt.txt}}
      </div>
    </div>
  </div>
</template>

<script>
//import store from '../store'
const axios = require('axios');

export default {
  name: 'NavMenu',
  props: {

  },
  data(){
    return{
      isActive: null,
      defi: [
        {
          txt: "Home",
          lnk: "/",
          roles: ["admin", "caadmin", "requester"],
          func: ()=>{ this.goto("/") },
        },
        {
          txt: "Authorities",
          lnk: "/authorities",
          roles: ["admin", "caadmin" ],
          func: ()=>{ this.goto("/authorities") },
        },
        {
          txt: "Requests",
          lnk: "/requests",
          roles: ["admin", "caadmin", "requester" ],
          func: ()=>{ this.goto("/requests/?") },
        },
        {
          txt: "Certificates",
          lnk: "/certificates",
          roles: ["admin", "caadmin", "requester" ],
          func: ()=>{ this.goto("/certificates/?") },
        },
        {
          txt: "Users",
          lnk: "/users",
          roles: ["admin"],
          func: ()=>{ this.goto("/users") },
        },
        {
          txt: "Settings",
          lnk: "/settings",
          roles: ["admin"],
          func: ()=>{ this.goto("/settings") },
        },
        {
          txt: "Logout",
          lnk: "logout",
          roles: ["admin", "caadmin", "requester"],
          func: this.call_logout,
        },

      ]
    }
  },
  methods:{
    goto(lnk){
      location.hash = lnk;
    },
    // chk_active(){
    //   let lnk = location.hash.substring(1);
    //   console.log(lnk);
    //   return lnk;
    // },
    chk_show(idx){
      let roles = this.defi[idx].roles;
      if(roles.includes(this.$store.state.role)){
        return true;
      }
      else{
        return false;
      }
    },

    call_logout(){
      this.$store.state.sysConfirmMsg = "Do you really want to logout?";
      this.$store.state.sysConfirmFw = ()=>{this.do_logout()};
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
  mounted: function(){
  
  },

}
</script>

<style scoped>
.menuBar{
  position: absolute;
  bottom: 4px;
  right: 24px;
}
.menuBar div{
  display: inline-block;
}
.menuBar .btn{
  font-size: 14px;
  *font-weight: bold;
  color: #fff;
  text-align: center;
  min-width: 100px;
  cursor: pointer;
  border-right: 2px solid #fff;
}
.menuBar .fst{
  border-left: 2px solid #fff;
}
.menuBar .btn:hover{
  text-decoration: underline;
}

.isActive{
  text-decoration: underline;
}
</style>
