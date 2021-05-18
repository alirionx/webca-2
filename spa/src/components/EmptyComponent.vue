<template>
  <div class="EmptyComponent">
  </div>
</template>

<script>
//import store from '../store'
//const axios = require('axios');
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'EmptyComponent',
  components: {
    //HelloWorld
  },
  data(){
    return{
      name: "EmptyComponent"
    }
  },
  methods:{

  },
  created: function(){
    console.log("created");
  },
  mounted: function(){
    console.log("mounted");
  }

}
</script>
