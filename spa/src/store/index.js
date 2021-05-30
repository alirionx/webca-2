import { createStore } from 'vuex'

const axios = require('axios');

export default createStore({
  state: {
    username: null,
    role: null,
    sysMsg: null,
    sysConfirmFw: null,
    sysConfirmMsg: null,

    countryCodes: [
      "AD","AE","AF","AG","AI","AL","AM","AO","AQ","AR","AS","AT","AU","AW","AX","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BL","BM","BN",
      "BO","BQ","BR","BS","BT","BV","BW","BZ","CA","CC","CD","CF","CG","CH","CK","CL","CM","CN","CO","CR","CU","CV","CW","CX","CY","CZ","DE","DJ",
      "DK","DM","DO","DZ","EC","EE","EG","EH","ER","ES","ET","FI","FJ","FK","FM","FO","FR","GA","GB","GD","GE","GF","GG","GH","GI","GL","GM","GN",
      "GP","GQ","GR","GS","GT","GU","GW","GY","HK","HM","HN","HR","HT","HU","HU","ID","IE","IL","IM","IN","IO","IQ","IR","IS","IT","JE","JM","JO",
      "JP","KE","KG","KH","KI","KM","KN","KP","KR","KW","KY","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MF",
      "MG","MH","MK","ML","MM","MN","MO","MP","MQ","MR","MS","MT","MU","MV","MW","MX","MY","MZ","NA","NC","NE","NF","NG","NI","NL","NO","NP","NR",
      "NU","NZ","OM","PA","PE","PF","PG","PH","PK","PL","PM","PN","PR","PS","PT","PW","PY","QA","RE","RO","RS","RU","RW","SA","SB","SC","SD","SE",
      "SG","SH","SI","SJ","SK","SL","SM","SN","SO","SR","SS","ST","SV","SX","SY","TC","TD","TF","TG","TH","TJ","TK","TM","TN","TO","TR","TT","TV",
      "TW","TZ","UA","UG","UM","US","UY","UZ","VA","VC","VE","VG","VI","VN","VU","WF","WS","YE","YT","ZA","ZM","ZW"
    ],

    roles: ["admin", "caadmin", "requester"]
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
    },
    reset_confirm_msg(state){
      state.sysConfirmFw = null;
      state.sysConfirmMsg = null;
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
