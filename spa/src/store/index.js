import { createStore } from 'vuex'

const axios = require('axios');

export default createStore({
  state: {
    username: null,
    role: null,
    sysMsg: null,
  },
  mutations: {
    set_username_role(state, obj){
      //console.log(obj)
      state.username = obj.username;
      state.role = obj.role;
    },
    reset_username_role(state){
      state.username = null;
      state.role = null;
    },
    reset_sys_msg(state){
      state.sysMsg = null;
    }
  },
  actions: {
    check_user_state({ commit }){
      return axios.get('/api/userstate')
      .then((response)=> {
        //console.log(response.data);
        let obj = {
          username: response.data.username,
          role: response.data.role
        }
        commit("set_username_role", obj)
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
      })
    },

    trigger_reset_sys_msg({ commit }, tm=2000){
      var fwFunc = ()=>{ commit("reset_sys_msg") }
      setTimeout(function(){
        fwFunc();
      }, tm)
    }

  },
  modules: {
  }
})
