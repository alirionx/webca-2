<template>
  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">{{title}}: "{{data.commonname}}"</div>

      <div class="innerBox">
      
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

        <div class="iptHl">New Validity Period in years</div>
        <select required v-model="data.days" >
          <option v-for="(val, key) in validityPeriods" :key="key" :value="val" >{{key}}</option>
        </select>

      </div>

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
  name: 'CaRenew',
  components: {
    //HelloWorld
  },
  props:{
    cb: Function,
    fw: Function,
    dataIn: Object
  },
  data(){
    return{
      title: "Renew Root Certificate Authority",
      data: {
        commonname: "",
        country: "",
        state: "",
        city: "",
        organization: "",
        unit: "",
        email: "",
        days: 1825
      },
      validityPeriods:{
        3: 1095,
        4: 1460,
        5: 1825,
        6: 2190,
        7: 2555,
        8: 2920,
        9: 3285,
        10: 3650
      }
    }
  },
  methods:{
    submit(){
      //console.log(this.data);
      axios.put('/api/ca/'+this.data.commonname, this.data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.fw();
        this.cb();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error);
        this.$store.state.sysMsg = "Failed to renew CA";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
    },

    take_data_in(){
      let tmpData =  JSON.parse(JSON.stringify(this.dataIn))
      for(var key in tmpData){
        this.data[key] = tmpData[key]
      }
    },

  
  },
  created: function(){
    this.take_data_in();
  },
  mounted: function(){
    
  }

}
</script>
