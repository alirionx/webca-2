<template>
  <div class="Users">
    <h4>{{title}}</h4>

    <table class="stdTable">
      <tr>
        <th v-for="(col, idx) in defi" :key="idx" :style="{textAlign: col.align}">{{col.hl}}</th>
        <th>act</th>
      </tr>
      <tr v-for="(row, idx) in data" :key="idx">
        <td v-for="(col, idx2) in defi" :key="idx2" :style="{textAlign: col.align}" >{{row[col.col]}}</td>
        <td>
          <ActMenu 
            v-bind:acts="acts" 
            v-bind:idx="idx" 
            v-bind:active="activeMenu" 
            @click="()=>{this.activeMenu = idx}" />
        </td>
      </tr>
      <tr class="lastLine">
        <td :colspan="defi.length+1" >
          <button @click="()=>{editAddShow = 'new'}">add</button>
        </td>
      </tr>
    </table>

    <EditAddUser v-if="editAddShow!=null" 
      v-bind:domains="cas"
      v-bind:dataIn="data[editAddShow]"
      v-bind:fw="()=>{call_users();}"
      v-bind:cb="()=>{editAddShow = null;}" />

  </div>
</template>

<script>
//import store from '../store'
const axios = require('axios');
import ActMenu from '@/components/ActMenu.vue'
import EditAddUser from '@/components/EditAddUser.vue'

export default {
  name: 'Users',
  components: {
    ActMenu,
    EditAddUser
  },
  data(){
    return{
      title: "App User Management",
      data: [],
      cas: [],

      defi: [
        {
          col: "username",
          hl: "Username",
          align: "left"
        },
        {
          col: "email",
          hl: "Email",
          align: "left"
        },
        {
          col: "role",
          hl: "Role",
          align: "left"
        },
        {
          col: "firstname",
          hl: "Firstname",
          align: "left"
        },
        {
          col: "lastname",
          hl: "Lastname",
          align: "left"
        },
        {
          col: "department",
          hl: "Department",
          align: "left"
        },
      ],
      acts: [
        {
          txt: "edit",
          func: (idx)=>{ this.editAddShow = idx; }
        },
        {
          txt: "set password",
          func: (idx)=>{ this.resetPwdShow = idx; }
        },
        {
          txt: "invite lnk",
          func: (idx)=>{ console.log("invite: " + idx); }
        },
        {
          txt: "delete",
          func: (idx)=>{ this.call_delete(idx); }
        }
      ],
      activeMenu: null,
      editAddShow: null,
      domainsShow: null,
      resetPwdShow: null,

    }
  },
  methods:{
    call_users(){
      axios.get('/api/users')
      .then((response)=> {
        console.log(response.data);
        this.data = response.data.data;
        this.cas = response.data.cas;
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to call users from API: '/api/user'";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      })
    },

    call_delete(idx){
      if(this.data[idx].username == this.$store.state.username){
        this.$store.state.sysMsg = "Delete yourself -> no way ;)";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
        return false;
      }

      this.$store.state.sysConfirmMsg = "Do you really want to delete this user: " + this.data[idx].username;
      this.$store.state.sysConfirmFw = ()=>{this.do_delete(idx)};
    },
    do_delete(idx){
      var uname = this.data[idx].username;
      axios.delete('/api/user/'+uname)
      .then((response)=> {
        console.log(response.data);
        this.call_users();
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to delete user: "+uname;
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    },

    reset_active_menu(){
      this.activeMenu = null;
    },

  },
  created: function(){
    this.call_users();

    var fwFunc = ()=> {this.reset_active_menu();}
    document.addEventListener("click", function(ev){
      let chk = ev.target.getAttribute('tag');
      if(chk != 'menu'){
        fwFunc();
      }
    })

  },
  mounted: function(){
    
  }

}
</script>
