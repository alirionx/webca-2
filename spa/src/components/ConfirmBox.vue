<template>
  <div v-if="$store.state.sysConfirmFw" class="blocker">

    <div class="stdForm" style="margin-top:16vh">
      <div class="hl">System Confirmation</div>
      <div class="msgBox">{{$store.state.sysConfirmMsg}}</div>
      <div class="btnFrame">
        <button @click="submit">Ok</button>
        <button @click="cancel">Cancel</button>
      </div>
    </div>

  </div>
</template>

<script>
import store from '../store'

export default {
  name: 'ConfirmBox',
  data(){
    return{
      msgHl: {
        msg: "System Message",
        confirm: "System Confirmation",
      } 
    }
  },
  props:{
  },
  methods:{
    submit(){
      this.$store.state.sysConfirmFw()
      this.$store.commit('reset_confirm_msg')
    },
    cancel(){
      this.$store.commit('reset_confirm_msg')
    }
  },
  created: function(){
  
  },
  mounted: function(){
   
  }

}
</script>
