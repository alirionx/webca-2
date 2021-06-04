<template>
  <div class="Invitation">
    <div>{{$route.params.inviHash}}</div>
  </div>
</template>

<script>
import store from '../store'
const axios = require('axios');
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Invitation',
  components: {
    //HelloWorld
  },
  data(){
    return{
      title: "Invitation for User Activation"
    }
  },
  methods:{
    call_invitation(){
      axios.get('/api/invitation/'+this.$route.params.inviHash)
      .then((response)=> {
        console.log(response.data);
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
        this.$store.state.sysMsg = "Invalid invitation hash";
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      })
    },
  },

  created: function(){
    this.call_invitation();
  }
}
</script>
