<template>
  
  <div class="blocker">

    <div class="stdForm" style="margin-top:6vh">

      <div class="hl">{{title}}</div>
      <!--div class="innerBox"-->
        <div class="iptHl" style="font-size:14px">Request String (PEM)</div>
        <textarea class="certBox" v-model="reqStr"></textarea>
     
      <!--/div-->
      <div class="btnFrame">
        <button @click="upload">Upload</button>
        <button @click="cb">Cancel</button>
      </div>
    </div>

  </div>

</template>

<script>
const axios = require('axios');

export default {
  name: 'ReqUpload',
  components: {
  },
  props:{
    caname:String,
    cb:Function,
    fw:Function,
  },
  data(){
    return{
      title: "Upload Certificate Request",
      reqStr: ""
    }
  },
  methods:{
    upload(){
      //console.log(this.caname, this.reqStr);
      const data = {"req": this.reqStr}
      axios.post('/api/req/upload/'+this.caname, data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.reqStr = "";
        this.cb();
        this.fw();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error);
        this.$store.state.sysMsg = "Failed to upload cert request";
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