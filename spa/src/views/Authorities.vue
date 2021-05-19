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
          <button @click="()=>{addIdx = true}">add</button>
        </td>
      </tr>
    </table>

    <CaAdd v-if="addIdx"
      v-bind:defi="defi"
      v-bind:fw="()=>{ call_authorities(); }" 
      v-bind:cb="()=>{addIdx = null}" 
      />

  </div>
</template>

<script>
import store from '../store'
const axios = require('axios');

import ActMenu from '@/components/ActMenu.vue'
import CaAdd from '@/components/CaAdd.vue'

export default {
  name: 'Authorities',
  components: {
    ActMenu,
    CaAdd
  },
  data(){
    return{
      addIdx: null,
      acts: [
        {
          txt: "renew",
          func: (idx)=>{ console.log(idx, 'renew')}
        },
        {
          txt: "delete",
          func: (idx)=>{ console.log(idx, 'delete')}
        }
      ],
      activeMenu: null,
      defi: [
        {
          col: "commonname",
          hl: "Common Name",
          typ: "text",
          manda: true,
          pattern: "[a-z/.-]+[a-z]{2}$",
          align: "left"
        },
        {
          col: "country",
          hl: "Country",
          typ: "dropdown",
          dd:["DE", "AU", "US", "UK"],
          manda: true,
          align: "left"
        },
        {
          col: "state",
          hl: "State",
          typ: "text",
          manda: true,
          align: "left"
        },
        {
          col: "city",
          hl: "City",
          typ: "text",
          manda: true,
          align: "left"
        },
        {
          col: "organization",
          hl: "Organization",
          typ: "text",
          manda: true,
          align: "left"
        },
        {
          col: "unit",
          hl: "Unit",
          typ: "text",
          manda: false,
          align: "left"
        },
        {
          col: "email",
          hl: "Responsible Email",
          typ: "text",
          manda: true,
          pattern: "[a-z1-9.\-]+[@][a-z1-9]+[.][a-z]{2,4}$",
          align: "left"
        },
        {
          col: "validity",
          hl: "Validity",
          typ: "date",
          manda: true,
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