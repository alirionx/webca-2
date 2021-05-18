<template>
  <div class="home">
    <div>{{$store.state.username}}</div>
    <div>{{$store.state.role}}</div>
    
  </div>
</template>

<script>
import store from '../store'
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
    //HelloWorld
  }
}
</script>
