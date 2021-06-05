<template>
  <div class="authorities">
    <h3>Root Certificate Authorities</h3>
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

    <CaAdd v-if="addShow"
      v-bind:fw="()=>{ call_authorities(); }" 
      v-bind:cb="()=>{addShow = null}" />

    <CaRenew v-if="renewIdx!=null"
      v-bind:fw="()=>{ call_authorities(); }" 
      v-bind:cb="()=>{renewIdx = null}" 
      v-bind:dataIn="data[renewIdx]" />

    <RootCertShow v-if="certShow"
      v-bind:caname="certShow" 
      v-bind:cb="()=>{certShow = null}" />

  </div>
</template>

<script>
import store from '../store'
const axios = require('axios');

import ActMenu from '@/components/ActMenu.vue'
import CaAdd from '@/components/CaAdd.vue'
import CaRenew from '@/components/CaRenew.vue'
import RootCertShow from '@/components/RootCertShow.vue'

export default {
  name: 'Authorities',
  components: {
    ActMenu,
    CaAdd,
    CaRenew,
    RootCertShow
  },
  data(){
    return{
      addShow: null,
      renewIdx: null,
      certShow: null,
      acts: [
        {
          txt: "show root cert",
          func: (idx)=>{ this.certShow = this.data[idx].commonname; }
        },
        {
          txt: "requests",
          func: (idx)=>{ location.hash = '/requests/'+this.data[idx].commonname; }
        },
        {
          txt: "certificates",
          func: (idx)=>{ location.hash = '/certificates/'+this.data[idx].commonname; }
        },
        {
          txt: "renew",
          func: (idx)=>{ this.renewIdx = idx; }
        },
        {
          txt: "export",
          func: (idx)=>{ console.log("export :"+ idx); }
        },
        {
          txt: "delete",
          func: (idx)=>{ this.call_delete(idx) }
        }
      ],
      activeMenu: null,
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
      data: []
    }
  },
  methods:{
    call_authorities(){
      axios.get('/api/cas')
      .then((response)=> {
        console.log(response.data);
        this.data = response.data.data;

      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to call data from API: /api/cas";
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    },
    reset_active_menu(){
      this.activeMenu = null;
    },

    call_delete(idx){
      this.$store.state.sysConfirmMsg = "Do you really want to delete the root certificate authority: " + this.data[idx].commonname;
      this.$store.state.sysConfirmFw = ()=>{this.do_delete(idx)};
    },
    do_delete(idx){
      var caCn = this.data[idx].commonname;
      axios.delete('/api/ca/'+caCn)
      .then((response)=> {
        console.log(response.data);
        this.call_authorities();
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to delete ca: "+caCn;
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    }

  },
  created: function(){
    //console.log("Authorities created");
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
    //console.log("Authorities mounted");
  }

}
</script>