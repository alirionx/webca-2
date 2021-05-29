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
          <button @click="()=>{addShow = true}">add</button>
        </td>
      </tr>
    </table>

  </div>
</template>

<script>
//import store from '../store'
const axios = require('axios');
import ActMenu from '@/components/ActMenu.vue'
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Users',
  components: {
    ActMenu
  },
  data(){
    return{
      title: "App User Management",
      data: [],

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
          func: (idx)=>{ this.editShow = idx; }
        },
        {
          txt: "show domains",
          func: (idx)=>{ this.domainsShow = idx; }
        },
        {
          txt: "reset pwd",
          func: (idx)=>{ this.resetPwdShow = idx; }
        },
        {
          txt: "delete",
          func: (idx)=>{ this.call_delete(idx); }
        }
      ],
      activeMenu: null,
      addShow: null,
      editShow: null,
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
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to call users from API: '/api/users'";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      })
    },

    call_delete(idx){
      console.log("selete: "+idx)
    }

  },
  created: function(){
    this.call_users();
  },
  mounted: function(){
    
  }

}
</script>
