<template>
  <div class="blocker">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>

      <div v-if="data.token">
        <div class="iptHl">Token</div>
        <div class="tokenBox">
          {{data.token}}
          <div class="blender"></div>
          <img src="@/assets/icon_copy.svg" @click="copy_text(data.token)" />
          <!--img src="@/assets/icon_gear.svg" @click="generate_token" /-->
        </div>

        
      </div>

      <div class="iptHl">Renewal Period</div>
      <select required v-model="renewal" >
        <option v-for="(val, key) in renewalPeriods" :key="key" :value="val" >{{key}}</option>
      </select>
      
      <div class="btnFrame">
        <button type="button" v-if="data.token && renewal!=data.renewal" @click="generate_token">Re-Generate</button>
        <button type="button" v-if="data.token" @click="delete_token">Delete</button>
        <button type="button" v-else @click="generate_token">Generate</button>
        <button type="button" @click="cb">Close</button>
      </div>

    </div>
      
  </div>
</template>

<script>
const axios = require('axios');

export default {
  name: 'ApiToken',
  components: {

  },
  props:{
    caname: String,
    crtObj: Object,
    cb: Function,
    //fw: Function
  },
  data(){
    return{
      title: "Manage API Token for Certificate: "+this.crtObj.commonname,
      data: {},
      renewal: 30,
      renewalPeriods:{
        "1 month": 30,
        "2 month": 60,
        "3 month": 90,
        "6 month": 180,
        "1 year": 365
      },
    }
  },
  methods:{

    call_token_state(){
      axios.get('/api/cert/token/'+this.caname+'/'+this.crtObj.commonname)
      .then((response)=> {
        console.log(response.data);
        this.data = response.data.data;
        if(this.data.renewal != undefined){
          this.renewal = this.data.renewal;
        }
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to call token state for: "+this.crtObj.commonname;
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    },
    
    generate_token(){
      const data = {
        caname: this.caname,
        commonname: this.crtObj.commonname,
        renewal: this.renewal
      }
      axios.post('/api/cert/token/generate', data)
      .then((response)=> {
        console.log(response.data);
        this.data = response.data.data;
        this.$store.state.sysMsg = "New Token generated!";
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to generate new token";
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    },

    delete_token(){
      axios.delete('/api/cert/token/'+this.caname+'/'+this.crtObj.commonname)
      .then((response)=> {
        console.log(response.data);
        this.call_token_state();
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to delete token";
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
    },

    submit(){
      
      // axios.post('/api/user/pwd', data, ).then(response => { 
      //   //this.loader = false;
      //   console.log(response.data);
      //   //this.fw();
      //   this.cb();
      // })
      // .catch(error => {
      //   //this.loader = false;
      //   console.log(error);
      //   this.$store.state.sysMsg = "Failed to set password for user: " + this.usrObj.username;
      //   this.$store.dispatch("trigger_reset_sys_msg", 3000);
      // });
    },

    copy_text(txt){ //OLD SCHOOL ;)
      //console.log(txt);
      var tmpTextBox = document.createElement("textarea");
      document.body.appendChild(tmpTextBox);
      //tmpTextBox.style.visibility = "hidden";
      tmpTextBox.value = txt;
      tmpTextBox.select();
      document.execCommand("copy");
      tmpTextBox.parentNode.removeChild(tmpTextBox);
      this.$store.state.sysMsg = "content copied to clipboard" ;
      this.$store.dispatch("trigger_reset_sys_msg", 800);
    },

  },
  created: function(){
    this.call_token_state();
  },
  mounted: function(){
    
  }

}
</script>

<style scoped>
.tokenBox{
  position: relative;
  max-width: 535px;
  min-height: 16px;
  line-height: 16px;
  padding: 14px;
  margin: 2px 0 8px 0;
  box-shadow: 0px 1px 2px #666;
  border: none;
  border-radius: 3px;
  background-color:#fff;
  font-size: 15px;
  overflow: hidden;
  white-space: nowrap;
}
.tokenBox .blender{
  position:absolute;
  right:0px;
  top:0px;
  width:100px;
  height: 40px;
  *background-color: #fff;
  background-image: linear-gradient(to right, transparent, #fff, #fff);
}
.tokenBox img{
  position: absolute;
  right:8px;
  top:8px;
  height: 28px;
  cursor: pointer;
}
.tokenBox img:hover{
  border-bottom: 2px solid #333;
}
</style>
