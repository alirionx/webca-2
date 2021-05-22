<template>
  <div class="certificates">
    <select class="mainSelect" v-model="authority" @change="set_hash">
      <option value="?">select an authority</option>
      <option v-for="(ca,idx) in authorities" :key="idx">{{ca.commonname}}</option>
    </select>

    <table class="stdTable">
      <tr>
        <th v-for="(col, idx) in defi" :key="idx" :style="{textAlign: col.align}">{{col.hl}}</th>
        <th>act</th>
      </tr>
      <tr v-for="(row, idx) in certificates" :key="idx">
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
import store from '../store'
const axios = require('axios');
import ActMenu from '@/components/ActMenu.vue'

export default {
  name: 'Certificates',
  components: {
    ActMenu
  },
  data(){
    return{
      authorities: [],
      authority: "?",

      defi: [
        {
          col: "commonname",
          hl: "Common Name",
          align: "left"
        },
        {
          col: "country",
          hl: "Country",
          align: "left"
        },
        {
          col: "state",
          hl: "State",
          align: "left"
        },
        {
          col: "city",
          hl: "City",
          align: "left"
        },
        {
          col: "organization",
          hl: "Organization",
          align: "left"
        },
        {
          col: "unit",
          hl: "Unit",
          align: "left"
        },
        {
          col: "email",
          hl: "Responsible Email",
          align: "left"
        },
        {
          col: "validity",
          hl: "Validity",
          align: "center"
        }
      ],
      certificates:[],

      acts: [
        {
          txt: "show cert",
          func: (idx)=>{ console.log("SHOW: "+idx) }
        },
        {
          txt: "renew",
          func: (idx)=>{ console.log("RENEW: "+idx) }
        },
        {
          txt: "delete",
          func: (idx)=>{ console.log("DELETE: "+idx) }
        }
      ],

      activeMenu: null,
      certShow: null,
      addShow: null,
    }
  },
  methods:{
    call_authorities(){
      axios.get('/api/cas')
      .then((response)=> {
        console.log(response.data);
        this.authorities = response.data.data;

      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to call data from API: /api/cas";
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    },

    call_certificates(){
      axios.get('/api/certs/'+this.authority)
      .then((response)=> {
        console.log(response.data);
        this.certificates = response.data.data;
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to call data from API: /api/certs/"+this.authority;
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    },

    set_hash(){
      location.hash = "/certificates/"+this.authority;
      if(this.authority=="?"){
        this.certificates = [];
      }
      else{
        this.call_certificates();
      }
    },

    reset_active_menu(){
      this.activeMenu = null;
    },
  },
  created: function(){
    this.call_authorities();

    var fwFunc = ()=> {this.reset_active_menu();}
    document.addEventListener("click", function(ev){
      let chk = ev.target.getAttribute('tag');
      if(chk != 'menu'){
        fwFunc();
      }
    })

  },
  mounted: function(){
    if(this.$route.params.caname){
      this.authority = this.$route.params.caname;
    }
    if(this.authority!="?"){
      this.call_certificates();
    }
  }

}
</script>