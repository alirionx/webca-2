<template>
  <div class="certificates">
    <h2>This is the Certificates Page</h2>
  </div>
</template>

<script>
import store from '../store'
const axios = require('axios');

export default {
  name: 'Certificates',
  components: {
    //HelloWorld
  },
  data(){
    return{
      name: "Certificates"
    }
  },
  methods:{
    
  },
  created: function(){
    console.log("Certificates created");
  },
  mounted: function(){
    console.log("Settings mounted");
  }

}
</script>