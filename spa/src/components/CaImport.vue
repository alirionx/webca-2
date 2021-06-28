<template>
  <div class="blocker">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>
      <input type="file" id="fileIpt" accept="application/x-gzip" @change="set_file" />  
      <div id="fileBox" @click="call_file_select">
        <span v-if="!fileName">click to select a file</span>
        {{fileName}}
      </div>


      <div class="btnFrame">
        <button @click="submit" v-if="fileName">Submit</button>
        <button type="button" @click="cb">Cancel</button>
      </div>

    </div>
      
  </div>
</template>

<script>
const axios = require('axios');

export default {
  name: 'CaImport',
  components: {
  },
  props:{
    cb: Function,
    fw: Function
  },
  data(){
    return{
      title: "Import Root Certificate Authority",
      fileName: null,
    }
  },
  methods:{
    submit(){
      var formData = new FormData();
      var fileObj = document.getElementById("fileIpt");
      formData.append("file", fileObj.files[0]);
    
      axios.post('/api/ca/import', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => { 
        console.log(response.data);
        this.fw();
        this.cb();
      })
      .catch(error => {
        //console.log(error.response);
        this.$store.state.sysMsg = error.response.data.msg;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
    },

    call_file_select(){
      var fileIpt = document.getElementById("fileIpt").click();
    },
    set_file(){
      let tmpVal = this.fileName = document.getElementById("fileIpt").value;
      if(tmpVal.includes("\\")){
        var spltChar = "\\";
      }
      else if(tmpVal.includes("/")){
        var spltChar = "/";
      }
      else{
        var spltChar = null;
      }

      if(spltChar){
        let spltAry = tmpVal.split(spltChar);
        this.fileName = spltAry.slice(-1)[0] 
      }
      else{
        this.fileName = tmpVal;
      }
    }
  
  },
  created: function(){

  },
  mounted: function(){
    
  }

}
</script>


<style scoped>
#fileIpt{
  display:none;
}
#fileBox{
  width:95%;
  margin:20px auto 4px auto;
  padding:14px;
  background: #fafafa;
  box-shadow: 0px 1px 2px #666;
  font-size: 16px;
  color:#000;
  text-align: center;
  cursor: pointer;
}
#fileBox:hover{
  background: #eee;
}
</style>