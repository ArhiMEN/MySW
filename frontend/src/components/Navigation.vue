<template>
  <header class="p-3 mb-3 border-bottom">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li><a href="#" @click="$router.push({name: 'wall'})" class="nav-link px-2 link-dark">Стена</a></li>
          <li><a href="#" @click="$router.push({name: 'friends'})" class="nav-link px-2 link-dark">Друзья</a></li>
          <li><a href="#" @click="$router.push({name: 'files'})" class="nav-link px-2 link-dark">Ваши файлы</a></li>
        </ul>
        <button v-show="isFriendsView" @click="$router.push({name: 'add_friends'})" class="btn btn-success btn-sm m-1">Добавить друга</button>
        <div class="dropdown text-end">
          <a href="#" class="d-block link-dark text-decoration-none dropdown-toggle" id="dropdownUser1"
             data-bs-toggle="dropdown" aria-expanded="false">
            <img :src="$store.getters.getAvatarUrl" alt="mdo" width="32" height="32" class="rounded-circle">
          </a>
          <ul class="dropdown-menu text-small" aria-labelledby="dropdownUser1" style="">
            <li><a class="dropdown-item" href="#" @click="$router.push({name: 'account'})">Личная информация</a></li>
            <li><a class="dropdown-item" href="#" @click="$router.push({name: 'settings'})">Настройки</a></li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li><a class="dropdown-item" href="#" @click="exit">Выйти</a></li>
          </ul>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import axios from "axios";
import store from "@/store";
import router from "@/router";

export default {
  name: "Navigation",
  methods: {
    exit() {
      axios.post('api/exit/')
          .then((resp) => {
            if (resp.data.success) {
              store.commit('deleteToken')
              store.commit('deleteAvatarUrl')
              router.push({name: 'login'})
            }
          })
    }
  },
  props: {
    isFriendsView: Boolean
  }
}
</script>

<style scoped>

</style>