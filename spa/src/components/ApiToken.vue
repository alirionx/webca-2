<template>
  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>

      <div v-if="data.token">
        <div class="iptHl">Token</div>
        <div class="tokenBox">
          {{data.token}}
          <div class="blender"></div>
          <img src="@/assets/icon_copy.svg" />
        </div>
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
    }
  },
  methods:{

    call_token_state(){
      axios.get('/api/cert/token/'+this.caname+'/'+this.crtObj.commonname)
      .then((response)=> {
        console.log(response.data);
        this.data = response.data.data;
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to call token state for: "+this.crtObj.commonname;
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
