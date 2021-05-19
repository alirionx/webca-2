<template>
  <div class="settings">
    <h2>This is the Settings Page</h2>
  </div>
</template>

<script>
import store from '../store'
const axios = require('axios');

export default {
  name: 'Settings',
  components: {
    //HelloWorld
  },
  data(){
    return{
      name: "Settings"
    }
  },
  methods:{
    
  },
  created: function(){
    //console.log("Settings created");
  },
  mounted: function(){
    //console.log("Settings mounted");
  }

}
</script>