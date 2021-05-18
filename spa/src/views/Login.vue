<template>
  <form @submit.prevent="submit">
  <div class="stdForm">
    <div class="hl">WebUI Login</div>
    <input type="text" v-model="username" />
    <input type="password" v-model="password" />
    <div class="btnFrame">
      <button>Submit</button>
    </div>
  </div>
  </form>
</template>

<script>
import store from '../store'
const axios = require('axios');
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Login',
  components: {
    //HelloWorld
  },
  data(){
    return{
      username: "",
      password: "",
    }
  },
  methods:{
    submit(){
      console.log(this.username, this.password);
    }
  },
  created: function(){
    console.log("created");
  },
  mounted: function(){
    console.log("mounted");
  }

}
</script>
