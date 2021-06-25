<template>
  <div class="home">
    <table class="usrStateTable">
      <tr>
        <th>Logged in as:</th>
        <td>{{$store.state.username}}</td>
      </tr>
      <tr>
        <th>User Role:</th>
        <td>{{$store.state.role}}</td>
      </tr>
    </table>
    
    <img src="@/assets/logo_tools.png" class="opensslLogo" />

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


<style scoped>
.opensslLogo{
  margin: 18vh auto auto auto;
  width:22%;
  margin-left: 2%;
  min-width: 300px;
  max-width: 800px;

}
.usrStateTable{
  position: fixed;
  left:10px;
  bottom: 10px;
  font-size:13px;
  text-align: left;
}
.usrStateTable th, td{
  text-align: left;
  border: 1px solid #ccc;
  padding:2px 10px 2px 10px;
}

</style>