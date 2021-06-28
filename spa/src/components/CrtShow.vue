<template>
  
  <div class="blocker">

    <div class="stdForm" style="margin-top:6vh">

      <div class="hl">{{title}}</div>
      <div class="innerBox">
        <div class="iptHl" style="font-size:14px">Cert (PEM)</div>
        <textarea class="certBox" disabled v-model="data.crt"></textarea>
        <div class="icoBar">
          <img src="@/assets/icon_copy.svg" @click="copy_text(data.crt)" />
          <img src="@/assets/icon_download.svg" @click="dl_text_as_file(dataIn.commonname+'_crt.pem', data.crt)" />
        </div>

        <div class="iptHl" style="font-size:14px">Full Chain (PEM)</div>
        <textarea class="certBox" disabled v-model="data.fullchain"></textarea>
        <div class="icoBar">
          <img src="@/assets/icon_copy.svg" @click="copy_text(data.fullchain)" />
          <img src="@/assets/icon_download.svg" @click="dl_text_as_file(dataIn.commonname+'_fullchain.pem', data.fullchain)" />
        </div>

        <div class="iptHl" style="font-size:14px">Key (PEM)</div>
        <textarea class="certBox" disabled v-model="data.key"></textarea>
        <div class="icoBar">
          <img src="@/assets/icon_copy.svg" @click="copy_text(data.key)" />
          <img src="@/assets/icon_download.svg" @click="dl_text_as_file(dataIn.commonname+'_key.pem', data.key)" />
        </div>

      </div>
      <div class="btnFrame">
        <button @click="cb">Ok</button>
      </div>
    </div>

  </div>

</template>

<script>
const axios = require('axios');

export default {
  name: 'CrtShow',
  components: {
  },
  props:{
    caname:String,
    dataIn:Object,
    cb:Function
  },
  data(){
    return{
      title: "Certificate: " +this.dataIn.commonname+ " ("+this.caname+")",
      data: {}
    }
  },
  methods:{
    call_cert(){
      var url = '/api/crtpem/'+this.caname+'/'+this.dataIn.commonname;
      axios.get(url)
      .then((response)=> {
        console.log(response.data);
        this.data = response.data.data;

      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Failed to load cert from API: "+url ;
        this.$store.dispatch("trigger_reset_sys_msg", 2000);
      })
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

    dl_text_as_file(filename, txt) {
      var tmpAElm = document.createElement('a');
      tmpAElm.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(txt));
      tmpAElm.setAttribute('download', filename);
      tmpAElm.style.display = 'none';
      document.body.appendChild(tmpAElm);
      tmpAElm.click();
      document.body.removeChild(tmpAElm);
    }

  },
  created: function(){
    this.call_cert();
  },
  mounted: function(){
  }

}
</script>


<style scoped>

</style>