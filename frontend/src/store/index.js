import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    'user_token': null,
    'user_avatar_url': null,
  },
  getters: {
    getToken : state => {
      return state.user_token
    },
    getAvatarUrl : state => {
      return state.user_avatar_url
    }
  },
  mutations: {
    setToken (state, token) {
      state.user_token = token
    },
    deleteToken (state) {
      state.user_token = null
    },
    setAvatarUrl (state, url) {
      state.user_avatar_url = url
    },
    deleteAvatarUrl (state) {
      state.user_avatar_url = null
    },
  },
  actions: {
  },
  modules: {
  }
})
