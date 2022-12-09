<template>
  <div class="container">
    <navigation></navigation>
    <table class="table table-striped table-dark">
      <tbody>
      <tr>
        <td>Имя:</td>
        <td>{{ user.first_name }}</td>
      </tr>
      <tr>
        <td>Фамилия:</td>
        <td>{{ user.last_name }}</td>
      </tr>
      <tr>
        <td>Отчество:</td>
        <td>{{ user.middle_name }}</td>
      </tr>
      <tr>
        <td>Дата рождения:</td>
        <td>{{ user.birthday }}</td>
      </tr>
      <tr>
        <td>Пол:</td>
        <td>{{ user.sex }}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import store from "@/store";
import axios from "axios";
import Navigation from "@/components/Navigation";

export default {
  name: "AccountView",
  components: {Navigation},
  data() {
    return {
      user: {
        first_name: '',
        last_name: '',
        middle_name: '',
        birthday: '',
        sex: '',
      }
    }
  },
  methods: {
    getUserData() {
      axios.get('/api/account/', {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.user = resp.data.user
            }
          })
    }
  },
  computed: {},
  mounted() {
    this.getUserData()
  }
}
</script>

<style scoped>

</style>