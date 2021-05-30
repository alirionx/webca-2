<template>
  <div class="blocker">
    <form @submit.prevent="submit">
    <div class="stdForm">
      
      <div class="hl">{{mode}} {{title}}</div>
      
      <div class="innerBox">

        <div class="iptHl">Username</div>
        <input type="text" required pattern="^[a-zA-Z]{4,10}" placeholder="min 4 max 10 chars and no special chars" v-model="data.username" />
        
        <div class="iptHl">Email Address</div>
        <input type="email" required v-model="data.email" />

        <div class="iptHl">Country</div>
        <select required v-model="data.role" >
          <option v-for="(val, idx) in $store.state.roles" :key="idx" :value="val">{{val}}</option>
        </select>

        <div class="iptHl">Firstname</div>
        <input type="text" v-model="data.firstname" />

        <div class="iptHl">Lastname</div>
        <input type="text" v-model="data.lastname" />

        <div class="iptHl">Department</div>
        <input type="text" v-model="data.department" />

        <div class="iptHl">Domains</div>
        <table class="domTable" cellspacing="6px" v-if="data.role!='admin'">
          <tr v-for="(dom, idx) in domains" :key="idx">
            <td>
              <label class="switch">
                <input type="checkbox" v-model="data.domains[dom]">
                <span class="slider round"></span>
              </label>
            </td>
            <td>
              {{dom}}
            </td>
          </tr>
        </table>

      </div>

      <div class="btnFrame">
        <button >Submit</button>
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
  name: 'EditAddUser',
  components: {
    //HelloWorld
  },
  props:{
    domains: Array,
    dataIn: Object,
    cb: Function,
    fw: Function
  },
  data(){
    return{
      mode: "Add",
      method: axios.post,
      title: "App User",
      data: {
        username: "",
        email: "",
        role: "requester",
        firstname: "",
        lastname: "",
        department: "",
        domains: {}
      },
    
    }
  },
  methods:{
    submit(){
     
      console.log(this.data);
      
      this.method('/api/user', this.data, ).then(response => { 
        //this.loader = false;
        console.log(response.data);
        this.fw();
        this.cb();
      })
      .catch(error => {
        //this.loader = false;
        console.log(error);
        this.$store.state.sysMsg = "Failed to "+this.mode+" User: " + error.response.data.msg;
        this.$store.dispatch("trigger_reset_sys_msg", 3000);
      });
    },

  },
  created: function(){
    if(this.dataIn != undefined){
      this.mode = "Edit";
      this.method = axios.put;
      for(var prop in this.dataIn){
        if(this.dataIn[prop] != undefined){
          this.data[prop] = JSON.parse(JSON.stringify(this.dataIn[prop]));
        }
      }
     
    }    

  },
  mounted: function(){
    
  }

}
</script>


<style scoped>
.domTable{
  margin:1px 0 6px 0;
  min-width: 550px;
  text-align: left;
}
.domTable td{
  padding:6px;
  background: #fff;
  *border: 0.5px solid #bbb;
  box-shadow: 0px 1px 2px #666;
}
.domTable td:first-child{
  width:40px;
  text-align: center;
}


.switch {
  position: relative;
  display: inline-block;
  width: 30px;
  height: 17px;
}

.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 13px;
  width: 13px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(13px);
  -ms-transform: translateX(13px);
  transform: translateX(13px);
}

.slider.round {
  border-radius: 17px;
}

.slider.round:before {
  border-radius: 50%;
}

</style>