<template>
  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>
      
      <div class="innerBox" style="padding-bottom:14px;">

        <div class="iptHl">Full Qualified Domain Name</div>
        <input type="text" required pattern="^([a-zA-Z0-9._-])+$" v-model="data.fqdn" />
        
        <div class="iptHl">Country</div>
        <select required v-model="data.country" >
          <option v-for="(val, idx) in $store.state.countryCodes" :key="idx" :value="val">{{val}}</option>
        </select>

        <div class="iptHl">State / Region</div>
        <input type="text" required v-model="data.state" />

        <div class="iptHl">City</div>
        <input type="text" v-model="data.city" />

        <div class="iptHl">Organization</div>
        <input type="text" required disabled v-model="data.organization" />

        <div class="iptHl">Organization Unit</div>
        <input type="text" v-model="data.unit" />

        <div class="iptHl">Email of responsible person</div>
        <input type="email" required v-model="data.email" />

        <div class="iptHl">Subject Alternative Names</div>
        <table class="keyValTbl"><tr>
            <th>
              <select v-model="newSanKey" style="margin-top:0; margin-bottom:0">
                <option v-for="(key, idx) in sanKeys" :key="idx">{{key}}</option>
              </select>
            </th>
            <td>
              <input type="text" v-model="newSanVal" style="margin-top:0; margin-bottom:0" />
            </td>
            <td>
              <div class="miniBtn" @click="add_san()">add</div>
            </td>
          </tr></table>

        <div v-for="(san, idx) in data.sans" :key="idx">
          <table class="keyValTbl"><tr>
            <th>{{san.key}}</th>
            <td>{{san.val}}</td>
            <td>
              <div class="miniBtn" @click="remove_san(idx)">remove</div>
            </td>
          </tr></table>
        </div>

      </div>

      <div class="btnFrame">
        <button>Submit</button>
        <button type="button" @click="cb">Cancel</button>
      </div>

    </div>
    </form>
      
  </div>
</template>

<script>
//import store from '../store'
const axios = require('axios');

export default {
  name: 'RequestAdd',
  components: {

  },
  props:{
    caObj: Object,
    cb: Function,
    fw: Function
  },
  data(){
    return{
      title: "Add new Certificate Request ("+this.caObj.commonname+")",
      sanKeys: ["IP", "DNS"],
      newSanKey: "DNS",
      newSanVal: "",
      data: {
        fqdn: "",
        country: "",
        state: "",
        city: "",
        organization: "",
        unit: "",
        email: "",
        sans: []
      },
    
    }
  },
  methods:{
    add_san(){
      if(this.newSanVal.length < 1){
        console.log("empty val...");
        return false;
      }

      for(var idx in this.data.sans){
        let curKey = this.data.sans[idx].key;
        let curVal = this.data.sans[idx].val;
        if(curKey == this.newSanKey && curVal == this.newSanVal){
          //console.log("already exists...");
          this.$store.state.sysMsg = "SAN already exists...";
          this.$store.dispatch("trigger_reset_sys_msg", 1500);
          return false;
        }
      }
      
      let newSanObj = {
        key: this.newSanKey,
        val: this.newSanVal
      }

      this.data.sans.push(newSanObj);
      //this.newSanKey = "DNS";
      this.newSanVal = "";
    },

    remove_san(idx){
      this.data.sans.splice(idx, 1);
    },

    submit(){
      console.log(this.data);
      axios.post('/api/req/'+this.caObj.commonname, this.data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.fw();
        this.cb();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error.response);
        this.$store.state.sysMsg = error.response.data.msg;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
    }
  },
  created: function(){
    this.data.organization = this.caObj.organization;
  },
  mounted: function(){
    
  }

}
</script>

<style scoped>

</style>
