<template>
  <div class="certificates">
    <select class="mainSelect" v-model="authority" @change="set_hash">
      <option value="?">select an authority</option>
      <option v-for="(ca,idx) in authorities" :key="idx">{{ca.commonname}}</option>
    </select>

    <table class="stdTable" v-if="authority!='?'">
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
    </table>

    <CrtShow v-if="crtShow!=null" 
      v-bind:caname="authority" 
      v-bind:dataIn="certificates[crtShow]" 
      v-bind:cb="()=>{crtShow = null;}" />

    <SansShow v-if="sansShow!=null" 
      v-bind:caname="authority" 
      v-bind:data="certificates[sansShow]" 
      v-bind:cb="()=>{sansShow = null;}" />

    <CrtRenew v-if="renewShow!=null" 
      v-bind:caObj="get_ca_obj_by_caname(authority)" 
      v-bind:data="certificates[renewShow]" 
      v-bind:fw="()=>{call_certificates();}"
      v-bind:cb="()=>{renewShow = null;}" /> 

  </div>
</template>

<script>
import store from '../store'
const axios = require('axios');
import ActMenu from '@/components/ActMenu.vue'
import SansShow from '@/components/SansShow.vue'
import CrtShow from '@/components/CrtShow.vue'
import CrtRenew from '@/components/CrtRenew.vue'

export default {
  name: 'Certificates',
  components: {
    ActMenu,
    SansShow,
    CrtShow,
    CrtRenew
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
          func: (idx)=>{ this.crtShow = idx; }
        },
        {
          txt: "show sans",
          func: (idx)=>{ this.sansShow = idx; }
        },
        {
          txt: "edit / renew",
          func: (idx)=>{ this.renewShow = idx; }
        },
        {
          txt: "delete",
          func: (idx)=>{ this.call_delete(idx); }
        }
      ],

      activeMenu: null,
      crtShow: null,
      renewShow: null,
      sansShow: null,
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

    call_delete(idx){
      this.$store.state.sysConfirmMsg = "Do you really want to delete this certificate: " + this.certificates[idx].commonname;
      this.$store.state.sysConfirmFw = ()=>{this.do_delete(idx)};
    },
    do_delete(idx){
      var crtCn = this.certificates[idx].commonname;
      axios.delete('/api/cert/'+this.authority+'/'+crtCn)
      .then((response)=> {
        console.log(response.data);
        this.call_certificates();
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to delete certificate: "+crtCn;
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    },

    get_ca_obj_by_caname(caname){
      for(var idx in this.authorities){
        if(caname == this.authorities[idx].commonname){
          return this.authorities[idx];
        }
      }
      return false;
    }
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