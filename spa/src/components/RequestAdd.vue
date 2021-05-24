<template>
  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>
      
      <div class="innerBox" style="padding-bottom:14px;">

        <div class="iptHl">Full Qualified Domain Name</div>
        <input type="text" required pattern="[a-z/.-]+[a-z]{2}$" v-model="data.fqdn" />
        
        <div class="iptHl">Country</div>
        <select required v-model="data.country" >
          <option v-for="(val, idx) in $store.state.countryCodes" :key="idx" :value="val">{{val}}</option>
        </select>

        <div class="iptHl">State / Region</div>
        <input type="text" required v-model="data.state" />

        <div class="iptHl">City</div>
        <input type="text" v-model="data.city" />

        <div class="iptHl">Organization</div>
        <input type="text" required v-model="data.organization" />

        <div class="iptHl">Organization Unit</div>
        <input type="text" v-model="data.unit" />

        <div class="iptHl">Email of responsible person</div>
        <input type="email" required v-model="data.email" />

        <div class="iptHl">Subject Alternative Names</div>
        <table class="keyValTbl"><tr>
            <th>
              <select v-model="newSanKey">
                <option v-for="(key, idx) in sanKeys" :key="idx">{{key}}</option>
              </select>
            </th>
            <td>
              <input type="text" v-model="newSanVal" />
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
    caname: String,
    cb: Function,
    fw: Function
  },
  data(){
    return{
      title: "Add new Certificate Request",
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
          console.log("already exists...");
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
      axios.post('/api/req/'+this.caname, this.data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.fw();
        this.cb();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error);
        this.$store.state.sysMsg = "Failed to create Certificate Request";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
    }
  },
  created: function(){

  },
  mounted: function(){
    
  }

}
</script>

<style scoped>

</style>
