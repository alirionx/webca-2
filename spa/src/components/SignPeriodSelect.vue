<template>
  <div class="blocker">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>
      
      <select required v-model="days" >
        <option v-for="(val, key) in validityPeriods" :key="key" :value="val" >{{key}}</option>
      </select>

      <div class="btnFrame">
        <button @click="do_sign">Sign</button>
        <button @click="cb">Cancel</button>
      </div>

    </div>
  </div>
</template>

<script>
//import store from '../store'
const axios = require('axios');

export default {
  name: 'SignPeriodSelect',
  components: {
    
  },
  props:{
    authority: String,
    data: Object,
    cb: Function,
    fw: Function
  },
  data(){
    return{
      title:"Select a validity period for: "+this.data.commonname,
      days: 30,
      validityPeriods:{
        "1 month": 30,
        "6 month": 180,
        "1 year": 365,
        "2 years": 730,
        "3 years": 1095
      },
    }
  },
  methods:{
    do_sign(){
      const data = {days: this.days}
      var reqCn = this.data.commonname;
      axios.post('/api/cert/'+this.authority+'/'+reqCn, data, )
      .then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.cb();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error);
        this.$store.state.sysMsg = "Failed to sign request: "+reqCn;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
    },
  },
  created: function(){
   
  },
  mounted: function(){

  }

}
</script>
