<template>
  <div>
    <div class="ActBtn" tag="menu" v-if="idx!=active">
      <div tag="menu"></div>
      <div tag="menu"></div>
      <div tag="menu"></div>
    </div>
    <div class="ActMenu" v-if="idx==active" tag="menu">
      <div class="box">
        <div v-for="(act, idx) in acts" :key="idx" @click="()=>{act.func(idx)}" class="btn" >{{act.txt}}</div>
      </div>
    </div>
  </div>
</template>

<script>
//import store from '../store'
//const axios = require('axios');
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'ActMenu',
  components: {
    //HelloWorld
  },
  props:{
    acts: Array,
    idx: Number,
    active: Number
  },
  data(){
    return{
      name: "ActMenu"
    }
  },
  methods:{

  },
  created: function(){
    //console.log("created");
  },
  mounted: function(){
    //console.log("mounted");
  }

}
</script>

<style scoped>
.ActBtn{
  display:table;
  margin: -4px auto -4px auto;
  padding:0 2px 0 2px;
  border: 1px #444 solid;
  border-radius: 2px;
  cursor: pointer;
}
.ActBtn:hover{
  background-color: #444;
}
.ActBtn:hover div{
  background-color: #fff;
}
.ActBtn div{
  width: 14px;
  height: 4px;
  border-radius: 3px;
  background-color: #444;
  margin: 2px auto 1.5px auto;
}
.ActMenu{
  position: relative;
}
.ActMenu .box{
  position:absolute;
  left:2px;
  top:-10px;
  box-shadow: 0px 4px 8px #444;
}
.ActMenu .btn{
  padding:3px;
  min-width: 80px;
  background-color: #444;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  border:1px solid #000;
  margin-top: -1px;
}
.ActMenu .btn:hover{
  background-color: #000;
}
</style>
