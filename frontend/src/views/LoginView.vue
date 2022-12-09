<template>
  <body class="text-center">
  <main class="form-signin w-100 m-auto">
    <h1 class="h3 mb-3 fw-normal">Пожалуйста, войдите в аккаунт</h1>

    <div class="form-group">
      <label for="floatingInput">Ваша почта</label>
      <input id="floatingInput" type="email" class="form-control" name="email" v-model="form.email"
             placeholder="name@example.com"
             required>
      <span class="text-danger">{{ validate_errors.email }}</span>
    </div>

    <div class="form-group">
      <label for="floatingPassword">Пароль</label>
      <input type="password" class="form-control" name="password" v-model="form.password" placeholder="Пароль" required>
      <span class="text-danger">{{ validate_errors.password }}</span>
    </div>

    <span class="text-danger">{{ validate_errors.__all__ }}</span>

    <button form="f_auth" class="w-100 btn btn-lg btn-primary" @click="login" type="submit">Войти</button>

    <p>Ещё не
      <router-link to="/registration">зарегистрированы</router-link>
      ?
    </p>
  </main>
  </body>
</template>

<script>
import axios from "axios";
import qs from "qs";
import router from "@/router";
import store from "@/store";
import {mapGetters} from "vuex";

export default {
  name: "LoginView",
  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      validate_errors: {
        email: '',
        password: '',
      }
    }
  },
  methods: {
    login() {
      axios.post('/api/login/', qs.stringify(this.form))
          .then((resp) => {
            if (resp.data.success) {
              store.commit('setToken', resp.data.token)
              store.commit('setAvatarUrl', resp.data.avatar_url)
              router.push({name: 'account'})
            } else {
              this.validate_errors = resp.data.validate_errors
            }
          })
    }
  },
  computed: {
    ...mapGetters([
      'getToken'
    ])
  }
}
</script>

<style scoped>

</style>