<template>
  <div class="requests">
    <select class="mainSelect" v-model="authority" @change="set_hash">
      <option value="?">select an authority</option>
      <option v-for="(ca,idx) in authorities" :key="idx">{{ca.commonname}}</option>
    </select>

    <table class="stdTable" v-if="authority!='?'">
      <tr>
        <th v-for="(col, idx) in defi" :key="idx" :style="{textAlign: col.align}">{{col.hl}}</th>
        <th>act</th>
      </tr>
      <tr v-for="(row, idx) in requests" :key="idx">
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
          <button @click="()=>{uploadShow = true}">upload</button>
        </td>
      </tr>
    </table>

    <ReqShow v-if="reqShow!=null" 
      v-bind:caname="authority" 
      v-bind:dataIn="requests[reqShow]" 
      v-bind:cb="()=>{reqShow = null;}" />

    <SansShow v-if="sansShow!=null" 
      v-bind:caname="authority" 
      v-bind:data="requests[sansShow]" 
      v-bind:cb="()=>{sansShow = null;}" />

    <RequestAdd v-if="addShow!=null" 
      v-bind:caObj="get_ca_obj_by_caname(authority)" 
      v-bind:fw="()=>{call_requests();}"
      v-bind:cb="()=>{addShow = null;}" />

    <RequestEdit v-if="editShow!=null" 
      v-bind:caObj="get_ca_obj_by_caname(authority)" 
      v-bind:data="requests[editShow]" 
      v-bind:fw="()=>{call_requests();}"
      v-bind:cb="()=>{editShow = null;}" />

    <ReqUpload v-if="uploadShow!=null" 
      v-bind:caname="authority" 
      v-bind:fw="()=>{call_requests();}"
      v-bind:cb="()=>{uploadShow = null;}" />
    
    <SignPeriodSelect v-if="periodSelectShow!=null" 
      v-bind:authority="authority" 
      v-bind:data="requests[periodSelectShow]" 
      v-bind:cb="()=>{periodSelectShow = null; this.call_requests(); }" />

  </div>
</template>

<script>
//import store from '../store'
const axios = require('axios');
import ActMenu from '@/components/ActMenu.vue'
import ReqShow from '@/components/ReqShow.vue'
import RequestAdd from '@/components/RequestAdd.vue'
import RequestEdit from '@/components/RequestEdit.vue'
import ReqUpload from '@/components/ReqUpload.vue'
import SansShow from '@/components/SansShow.vue'
import SignPeriodSelect from '@/components/SignPeriodSelect.vue'

export default {
  name: 'Requests',
  components: {
    ActMenu,
    RequestAdd,
    RequestEdit,
    ReqShow,
    ReqUpload,
    SansShow,
    SignPeriodSelect
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
        }
      ],
      requests:[],

      acts: [
        {
          txt: "show reqest",
          func: (idx)=>{ this.reqShow = idx; }
        },
        {
          txt: "show sans",
          func: (idx)=>{ this.sansShow = idx; }
        },
        {
          txt: "edit",
          func: (idx)=>{ this.editShow = idx; }
        },
        {
          txt: "sign",
          //func: (idx)=>{ this.call_sign(idx); }
          func: (idx)=>{ this.periodSelectShow = idx; }
        },
        {
          txt: "delete",
          func: (idx)=>{ this.call_delete(idx); }
        }
      ],
      activeMenu: null,
      certReq: null,
      addShow: null,
      editShow: null,
      uploadShow: null,
      reqShow: null,
      sansShow: null,
      periodSelectShow: null,
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

    call_requests(){
      axios.get('/api/reqs/'+this.authority)
      .then((response)=> {
        console.log(response.data);
        this.requests = response.data.data;
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to call data from API: /api/reqs/"+this.authority;
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    },

    set_hash(){
      location.hash = "/requests/"+this.authority;
      if(this.authority=="?"){
        this.requests = [];
      }
      else{
        this.call_requests();
      }
    },

    reset_active_menu(){
      this.activeMenu = null;
    },

    call_sign(idx){
      this.$store.state.sysConfirmMsg = "Do you really want to sign this request: " + this.requests[idx].commonname;
      this.$store.state.sysConfirmFw = ()=>{this.do_sign(idx)};
    },
    

    call_delete(idx){
      this.$store.state.sysConfirmMsg = "Do you really want to delete this request: " + this.requests[idx].commonname;
      this.$store.state.sysConfirmFw = ()=>{this.do_delete(idx)};
    },
    do_delete(idx){
      var reqCn = this.requests[idx].commonname;
      axios.delete('/api/req/'+this.authority+'/'+reqCn)
      .then((response)=> {
        console.log(response.data);
        this.call_requests();
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to delete request: "+reqCn;
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
      this.call_requests();
    }
  }

}
</script>