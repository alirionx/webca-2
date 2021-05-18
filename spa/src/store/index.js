import { createStore } from 'vuex'

const axios = require('axios');

export default createStore({
  state: {
    username: null,
    role: null
  },
  mutations: {
    set_username_role(state, username, role){
      state.username = username;
      state.role = role;
    }
  },
  actions: {
    check_user_state({ commit }){
      axios.get('/api/userstate')
      .then((response)=> {
        console.log(response.data);
        let username = response.data.username;
        let role = response.data.role;
        commit("set_username_role", username, role)
      })
      .catch((err)=> {
        // handle error
        console.log(err.response);
      })
    }

  },
  modules: {
  }
})
