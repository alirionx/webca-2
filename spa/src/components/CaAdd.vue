<template>
  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">Add new Root Certificate Authority</div>
      <div v-for="(field, idx) in defi" :key="idx" >
        <div class="iptHl">{{field.hl}}</div>
        <input v-if="field.typ=='static'" type="text" disabled v-model="data[field.col]" />
        <input v-if="field.typ=='text'" type="text" :required="field.manda" :pattern="field.pattern" v-model="data[field.col]" />
        <select v-if="field.typ=='dropdown'" :required="field.manda" v-model="data[field.col]" >
          <option v-for="(val, idx) in field.dd" :key="idx" :value="val">{{val}}</option>
        </select>
        
      </div>

      <div class="btnFrame">
        <button @click="print_data">Submit</button>
        <button type="button" @click="cb">Cancel</button>
      </div>

    </div>
    </form>
      
  </div>
</template>

<script>
//import store from '../store'
const axios = require('axios');
//import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'CaAdd',
  components: {
    //HelloWorld
  },
  props:{
    cb: Function,
    fw: Function,
    defi: Array
  },
  data(){
    return{
      data: {}
    }
  },
  methods:{
    set_init_keys(){
      for(var idx in this.defi){
        this.data[this.defi[idx].col] = "";
      }
    },

    submit(){
     
      console.log(this.data);
      
      axios.post('/api/ca', this.data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.fw();
        this.cb();
      })
      .catch(error => {
        //this.loader = false;
        //console.log(error);
        this.$store.state.sysMsg = "Login Failed";
        this.$store.dispatch("Failed to create CA", 3000);
        this.set_init_keys();
      });
    }
  },
  created: function(){
    this.set_init_keys();
  },
  mounted: function(){
    
  }

}
</script>
