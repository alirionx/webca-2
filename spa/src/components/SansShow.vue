<template>
  
  <div class="blocker">

    <div class="stdForm" style="margin-top:1vh">
      <div class="hl">{{title}}</div>
      <div v-for="(san, idx) in data.sans" :key="idx">
        <table class="keyValTbl"><tr>
          <th>{{san.key}}</th>
          <td>{{san.val}}</td>
          <td>
          </td>
        </tr></table>
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
  name: 'SansShow',
  components: {
  },
  props:{
    cb:Function,
    data: Object
  },
  data(){
    return{
      title: "Subject Alternative Names: " +this.data.commonname,
    }
  },
  methods:{
  
  },
  created: function(){
  },
  mounted: function(){
  }

}
</script>


<style scoped>

</style>