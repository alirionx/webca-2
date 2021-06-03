<template>
  <div class="blocker">
    <div class="stdForm">
      
      <div class="hl">{{title}}</div>

      <div class="tokenBox" v-if="inviHash">
        {{inviUrl}}
        <div class="blender"></div>
        <img src="@/assets/icon_copy.svg" @click="copy_text(inviUrl)" />
      </div>
     
      <div class="btnFrame">
        <button v-if="inviHash" @click="delete_invitation">Delete</button>
        <button v-else @click="create_invitation">Create</button>
        <button type="button" @click="cb">Cancel</button>
      </div>

    </div>
      
  </div>
</template>

<script>
const axios = require('axios');

export default {
  name: 'CreateInvitation',
  components: {

  },
  props:{
    usrObj: Object,
    cb: Function,
    //fw: Function
  },
  data(){
    return{
      title: "Create user invitation link for: "+this.usrObj.username,
      inviHash: null,
      inviUrl: null,
    }
  },
  methods:{

    call_invitation_state(){
      axios.get('/api/user/invitation/'+this.usrObj.username)
      .then((response)=> {
        console.log(response.data);
        this.inviHash = response.data.data.hash;
        this.create_invi_url();
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to call users invitation state";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      })
    },

    create_invitation(){
      const data = {
       username: this.usrObj.username
      }

      axios.post('/api/user/invitation', data, ).then(response => { 
        console.log(response.data);
        //this.cb();
        this.inviHash = response.data.data.hash;
        this.create_invi_url();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error);
        this.$store.state.sysMsg = "Failed to create invitation for user: " + this.usrObj.username;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
    },

    delete_invitation(){
      axios.delete('/api/user/invitation/'+this.usrObj.username)
      .then((response)=> {
        console.log(response.data);
        this.inviHash = null;
        this.create_invi_url();
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to delete users invitation";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      })
    },

    create_invi_url(){
      if(!this.inviHash){
        this.inviUrl = null;
      }
      else{
        let urlStr = location.protocol + '//' + location.hostname;
        if(location.port != "80" && location.port != "443"){
          urlStr += ':' + location.port
        }
        this.inviUrl = urlStr+"/api/invitation/"+this.inviHash; 
      }
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
    this.call_invitation_state();
  },
  mounted: function(){
    
  }

}
</script>


