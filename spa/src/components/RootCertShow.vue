<template>
  
  <div class="blocker">

    <div class="stdForm" style="margin-top:10vh">
      <div class="hl">{{title}}</div>
      <!--div class="innerBox"-->
        <div class="iptHl" style="font-size:14px">Certificate (PEM)</div>
        <textarea class="certBox" disabled v-model="data.crt"></textarea>
        
        <div class="iptHl" style="font-size:14px">Key (PEM)</div>
        <textarea class="certBox" disabled v-model="data.key"></textarea>
      <!--/div-->
      <div class="btnFrame">
        <button @click="cb">Ok</button>
      </div>
    </div>

  </div>

</template>

<script>
import store from '../store'
const axios = require('axios');


export default {
  name: 'RootCertShow',
  components: {
  },
  props:{
    caname:String,
    cb:Function
  },
  data(){
    return{
      title: this.caname+": certificates",
      data: {}
    }
  },
  methods:{
    call_root_cert(){
      axios.get('/api/rootcert/'+this.caname)
      .then((response)=> {
        console.log(response.data);
        this.data = response.data.data;

      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to load root cert from API: /api/rootcert/"+this.caname ;
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    }
  },
  created: function(){
    this.call_root_cert();
  },
  mounted: function(){
  }

}
</script>
