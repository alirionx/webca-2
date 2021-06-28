<template>
  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>
      
      <div class="innerBox" style="padding-bottom:14px;">

        <div class="iptHl">Full Qualified Domain Name</div>
        <input type="text" required disabled v-model="data.commonname" />
        
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

        <!--Macht hier wirklich keinen Sinn!. Request ist Request, so wie er ist. Bei Bedarf neuen Request erzeugen-->
        <!--div class="iptHl">Subject Alternative Names</div>
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
        </div-->

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
  name: 'RequestEdit',
  components: {

  },
  props:{
    caObj: Object,
    data: Object,
    cb: Function,
    fw: Function
  },
  data(){
    return{
      title: "Edit Certificate Request",
      sanKeys: ["IP", "DNS"],
      newSanKey: "DNS",
      newSanVal: "", 
      tmpData: {},
      // data: {
      //   fqdn: "",
      //   country: "",
      //   state: "",
      //   city: "",
      //   organization: "",
      //   unit: "",
      //   email: "",
      //   sans: []
      // },
    
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
      axios.put('/api/req/'+this.caObj.commonname+'/'+this.data.commonname, this.data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.fw();
        this.cb();
      })
      .catch(error => {
        //this.loader = false;
        this.reset_data();
        console.log(error.response);
        this.$store.state.sysMsg = error.response.data.msg;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
    },

    reset_data(){
      for(var prop in this.tmpData){
        this.data[prop] = this.tmpData[prop];
      }
    }
  },
  created: function(){
    this.tmpData = JSON.parse(JSON.stringify(this.data));
  },
  mounted: function(){
    
  }

}
</script>

<style scoped>

</style>
