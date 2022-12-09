<template>
  <div class="container">
    <navigation></navigation>
    <div v-for="item in potential_friends" class="my-4">
      <img :src="item.avatar" alt="mdo" width="32" height="32"
           class="rounded-circle">
      Имя: {{ getFullName(item) }}<br>
      Пол: {{ item.sex }}<br>
      <button @click="addFriend(item.id)" class="btn btn-success btn-sm">Добавить</button>
    </div>
  </div>
</template>

<script>
import Navigation from "@/components/Navigation";
import axios from "axios";
import store from "@/store";
import qs from "qs";

export default {
  name: "AddFriendView",
  components: {Navigation},
  data() {
    return {
      potential_friends: {
        users: []
      }
    }
  },
  methods: {
    getUsers() {
      axios.get('/api/friends/potential/', {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.potential_friends = resp.data.users
            }
          })
          .catch((err) => {
            console.log(err)
          })
    },
    getFullName(item) {
      return item.last_name + " " + item.first_name + " " + item.middle_name
    },
    addFriend(user_id) {
      axios.post('/api/friends/add/', qs.stringify({user_id}), {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.getUsers()
            } else {
              // send error
            }
          })
    }
  },
  mounted() {
    this.getUsers()
  }
}
</script>

<style scoped>

</style>