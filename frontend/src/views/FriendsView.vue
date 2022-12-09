<template>
  <div class="container">
    <navigation is-friends-view></navigation>
    <div v-for="item in friends" class="my-4">
      {{ getFullName(item) }}<br>
      <button @click="$router.push({name: 'messages', params: {id:item.id}})" class="btn btn-primary btn-sm m-1">
        Отправить сообщение
      </button>
      <button @click="$router.push({name: 'friend_wall', params: {id:item.id}})" class="btn btn-warning btn-sm m-1">Посмотреть стену</button>
      <button @click="deleteFriend(item.id)" class="btn btn-danger btn-sm m-1">Удалить из друзей</button>
    </div>
  </div>
</template>

<script>
import Navigation from "@/components/Navigation";
import axios from "axios";
import store from "@/store";
import qs from "qs";

export default {
  name: "FriendsView",
  components: {Navigation},
  data() {
    return {
      friends: {
        friend: []
      }
    }
  },
  methods: {
    getFriends() {
      axios.get('/api/friends/', {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.friends = resp.data.friends
            }
          })
    },
    deleteFriend(user_id) {
      axios.post('/api/friends/delete/', qs.stringify({user_id}), {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.getFriends()
            } else {
              // send error
            }
          })
    },
    getFullName(item) {
      return item.last_name + " " + item.first_name + " " + item.middle_name
    }
  },
  mounted() {
    this.getFriends()
  }
}
</script>

<style scoped>

</style>