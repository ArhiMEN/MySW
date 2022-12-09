<template>
  <div class="container">
    <navigation></navigation>
    <h3 v-show="!empty">Стена пользователя: {{ entries[0].name }}</h3>
    <p v-show="!empty" v-for="item in entries" class="border text-break">
      <small class="text-muted">Название записи: </small>
      <span class="fst-italic fw-bold">{{ item.title }}</span><br>
      <small class="text-muted">Дата записи: </small>
      <u>{{ item.date }}</u><br>
      <small class="text-muted">Текст записи: </small>
      {{ item.text }}
    </p>
    <p v-show="empty">Этот пользователь не оставил ни одной записи на стене.</p>
  </div>
</template>

<script>
import axios from "axios";
import qs from "qs";
import store from "@/store";
import Navigation from "@/components/Navigation";

export default {
  name: "FriendWallView",
  components: {Navigation},
  data() {
    return {
      empty: null,
      user_id: null,
      entries: {
        entry: []
      },
    }
  },
  methods: {
    getEntry() {
      axios.post('/api/wall/entries/', qs.stringify({user_id: this.user_id}), {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.entries = resp.data.entries
              this.empty = false
            } else if (resp.data.empty) {
              this.empty = true
              this.entries = [{name: ''}]
            }
          })
    }
  },
  mounted() {
    this.user_id = this.$route.params.id
    this.getEntry()
  }
}
</script>

<style scoped>

</style>