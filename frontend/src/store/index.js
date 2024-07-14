import { createStore } from 'vuex'
import {showModal, toast} from "../utils/popup"
import api from "@/api";
import router from "@/router";

export default createStore({
  state: {
      user: {
        isLoggedIn: false,
        username: "",
        nickname: "",
        role: "",
        token: "",
        email: "",
        phone: "",
        gender: "女",
        avatar: ""
      }
  },
  getters: {
    getUserInfo(use){
      return this.state.user;
    },
    // 获取用户头像
    getUserAvatar(state) {
      return state.user.avatar;
    },
    isLoggedIn: state => state.user.isLoggedIn,
    getUsername: state => state.user.username,
    avatar: state => state.user.avatar,
    getUserRole(state) {
      return state.user.role;
    },
  },
  mutations: {

    SET_LOGGED_IN(state, status) {
      state.user.isLoggedIn = status;
    },
    SET_USERINFO(state, userData) {
      state.user.username = userData.username;
      state.user.role = userData.role;
      state.user.token = userData.token;
      state.user.email = userData.email;
      state.user.phone = userData.phone;
      state.user.nickname = userData.nickname;
      state.user.avatar = userData.avatar;
      if(userData.gender){
        state.user.gender = "男"
      }
        },
    SET_UPDATE_USERINFO(state, userData) {
        state.user.username = userData.username;
        state.user.email = userData.email;
        state.user.phone = userData.phone;
        state.user.nickname = userData.nickname;

      // console.log(name)
    },
    // 更新用户头像
    UPDATE_USER_AVATAR(state, avatarUrl) {
      state.user.avatar = avatarUrl;
    },
  },
  actions: {
    updateUserInStore({ commit }, userData) {
      // 这个action用于接收用户数据并提交到mutation
      commit('SET_UPDATE_USERINFO', userData);
    },
    //获取用户信息
    getInfo({commit}){
      return new Promise((resolve, reject)=>{
        getInfoByToken().then(res=>{
          //如果无法获取用户信息，那么说明token失效，需要重新登录。
          if(res.data === null){
            this.dispatch('Logout').then(()=>{
              router.push("/")
            })
          }
          commit("SET_USERINFO", res.data)
          resolve(res)
        }).catch(err=>reject(err))
      })
    },
    login({ commit }, userData) {
      // 假设你在这里调用API登录，然后根据响应更新状态
      commit('SET_LOGGED_IN', true);
      commit('SET_USERINFO', userData);
    },
    async logout({commit}) {
      try {
        const shouldLogout = await showModal("确认退出吗");
        if (shouldLogout) {
          commit('SET_LOGGED_IN', false);
          commit('SET_USERINFO', '');
          api.logout()
          router.push("/courseCenter")
          toast("退出成功", "success");
        }
      }catch (err){
      }
    },
    // 更新用户头像
    updateAvatarLocal({ commit }, avatarUrl) {
      commit('UPDATE_USER_AVATAR', avatarUrl);
    },
    },
  modules: {
  }
})
