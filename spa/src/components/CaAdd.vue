<template>
  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">Add new Root Certificate Authority</div>
      
      <div class="iptHl">Common Name</div>
      <input type="text" required pattern="[a-z/.-]+[a-z]{2}$" v-model="data.commonname" />
      
      <div class="iptHl">Country</div>
      <select required v-model="data.country" >
        <option v-for="(val, idx) in countryCodes" :key="idx" :value="val">{{val}}</option>
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


      <div class="btnFrame">
        <button @click="print_data">Submit</button>
        <button type="button" @click="cb">Cancel</button>
      </div>

    </div>
    </form>
      
  </div>
</template>

<script>
//import store from '../store'
const axios = require('axios');
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'CaAdd',
  components: {
    //HelloWorld
  },
  props:{
    cb: Function,
    fw: Function
  },
  data(){
    return{
      data: {
        commonname: "",
        country: "",
        state: "",
        city: "",
        organization: "",
        unit: "",
        email: "",
      },
      countryCodes: [
        "AD","AE","AF","AG","AI","AL","AM","AO","AQ","AR","AS","AT","AU","AW","AX","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BL","BM","BN",
        "BO","BQ","BR","BS","BT","BV","BW","BZ","CA","CC","CD","CF","CG","CH","CK","CL","CM","CN","CO","CR","CU","CV","CW","CX","CY","CZ","DE","DJ",
        "DK","DM","DO","DZ","EC","EE","EG","EH","ER","ES","ET","FI","FJ","FK","FM","FO","FR","GA","GB","GD","GE","GF","GG","GH","GI","GL","GM","GN",
        "GP","GQ","GR","GS","GT","GU","GW","GY","HK","HM","HN","HR","HT","HU","HU","ID","IE","IL","IM","IN","IO","IQ","IR","IS","IT","JE","JM","JO",
        "JP","KE","KG","KH","KI","KM","KN","KP","KR","KW","KY","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MF",
        "MG","MH","MK","ML","MM","MN","MO","MP","MQ","MR","MS","MT","MU","MV","MW","MX","MY","MZ","NA","NC","NE","NF","NG","NI","NL","NO","NP","NR",
        "NU","NZ","OM","PA","PE","PF","PG","PH","PK","PL","PM","PN","PR","PS","PT","PW","PY","QA","RE","RO","RS","RU","RW","SA","SB","SC","SD","SE",
        "SG","SH","SI","SJ","SK","SL","SM","SN","SO","SR","SS","ST","SV","SX","SY","TC","TD","TF","TG","TH","TJ","TK","TM","TN","TO","TR","TT","TV",
        "TW","TZ","UA","UG","UM","US","UY","UZ","VA","VC","VE","VG","VI","VN","VU","WF","WS","YE","YT","ZA","ZM","ZW"
      ]
    }
  },
  methods:{
    submit(){
     
      console.log(this.data);
      
      axios.post('/api/ca', this.data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.fw();
        this.cb();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error);
        this.$store.state.sysMsg = "Failed to create CA";
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
