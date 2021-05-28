<template>
  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>
      
      <div class="innerBox">

        <div class="iptHl">Common Name</div>
        <input type="text" required pattern="^([a-zA-Z0-9._-])+$" v-model="data.commonname" />
        
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

      </div>

      <div class="btnFrame">
        <button >Submit</button>
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
      title: "Add new Root Certificate Authority",
      data: {
        commonname: "",
        country: "",
        state: "",
        city: "",
        organization: "",
        unit: "",
        email: "",
      },
    
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
