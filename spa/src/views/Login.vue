<template>
  <form @submit.prevent="submit">
  <div class="stdForm">
    
    <div class="hl">WebUI Login</div>
    
    <input 
      type="text" class="txtCenter" 
      placeholder="Username" 
      v-model="username" 
      required />
    <input 
      type="password" class="txtCenter" 
      placeholder="Password" 
      v-model="password" 
      v-on:keyup.enter="submit" 
      required />

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
