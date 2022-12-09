<template>
  <div class="container">
    <div class="form-signin w-50 m-auto">
      <div class="form-group">
        <label for="firstName" class="form-label">Имя</label>
        <input type="text" class="form-control" v-model="form.first_name" name="first_name" required>
        <span class="text-danger">{{ validate_errors.first_name }}</span>
      </div>

      <div class="form-group">
        <label for="lastName" class="form-label">Фамилия</label>
        <input type="text" class="form-control" v-model="form.last_name" name="last_name" required>
        <span class="text-danger">{{ validate_errors.last_name }}</span>
      </div>

      <div class="form-group">
        <label for="middleName" class="form-label">Отчество <span class="text-muted">(опционально)</span></label>
        <input type="text" class="form-control" v-model="form.middle_name" name="middle_name">
        <span class="text-danger">{{ validate_errors.middle_name }}</span>
      </div>

      <div class="form-group">
        <label for="birthday" class="form-label">Дата рождения</label>
        <input type="date" class="form-control" v-model="form.birthday" name="birthday" required>
        <span class="text-danger">{{ validate_errors.birthday }}</span>
        <span class="text-danger">{{ errors.birthday }}</span>
      </div>

      <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" v-model="form.email" name="email" required>
        <span class="text-danger">{{ validate_errors.email }}</span>
        <span class="text-danger">{{ errors.email }}</span>
      </div>

      <div class="form-group">
        <label for="password" class="form-label">Пароль</label>
        <input type="password" class="form-control" v-model="form.password" name="password" required>
        <span class="text-danger">{{ validate_errors.password }}</span>
      </div>

      <div class="form-group">
        <label for="password2" class="form-label">Повторите пароль</label>
        <input type="password" class="form-control" v-model="form.password2" name="password2" required>
        <span class="text-danger">{{ validate_errors.password2 }}</span>
      </div>

      <div class="form-group">
        <label class="form-label">Пол:</label>
        <div class="form-check col">
          <input name="sex" type="radio" class="form-check-input" value="мужской" v-model="form.sex" required>
          <label class="form-check-label" for="sex_m">Мужской</label>
        </div>
        <div class="form-check col">
          <input name="sex" type="radio" class="form-check-input" value="женский" v-model="form.sex" required>
          <label class="form-check-label" for="sex_w">Женский</label>
        </div>
        <span class="text-danger">{{ validate_errors.sex }}</span>
      </div>

      <div class="form-group">
        <button class="w-100 btn btn-lg btn-primary" @click="registration">Зарегистрироваться
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import qs from "qs";
import router from "@/router";
import store from "@/store";

export default {
  name: "RegistrationView",
  data() {
    return {
      form: {
        first_name: '',
        last_name: '',
        middle_name: '',
        birthday: '',
        email: '',
        password: '',
        password2: '',
        sex: '',
      },
      validate_errors: {
        first_name: '',
        last_name: '',
        middle_name: '',
        birthday: '',
        email: '',
        password: '',
        password2: '',
        sex: '',
      },
      errors: {
        birthday: '',
        email: '',
      }
    }
  },
  mounted() {
  },
  methods: {
    registration() {
      axios.post('/api/registration/', qs.stringify(this.form))
          .then((resp) => {
            if (resp.data.success) {
              store.commit('setToken', resp.data.token)
              store.commit('setAvatarUrl', resp.data.avatar_url)
              router.push({name: 'account'})
            } else {
              this.validate_errors = resp.data.validate_errors
              if (resp.data.errors.hasOwnProperty('birthday')) {
                this.errors.birthday = resp.data.errors.birthday
              } else {
                this.errors.birthday = ''
              }
              if (resp.data.errors.hasOwnProperty('email')) {
                this.errors.email = resp.data.errors.email
              } else {
                this.errors.email = ''
              }
            }
          }).catch((err) => {
        console.log(err)
      })
    }
  },
  computed: {},
  watch: {}
}
</script>

<style scoped>

</style>