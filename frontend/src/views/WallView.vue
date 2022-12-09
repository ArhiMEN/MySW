<template>
  <div class="container">
    <navigation></navigation>
    <div v-show="!empty" v-for="item in entries" class="border text-break rounded my-3">
      <small class="text-muted m-1">Дата записи:</small>
      <u>{{ item.date }}</u><br>
      <small class="text-muted m-1">Название записи:</small>
      <span class="fst-italic fw-bold m-1">{{ item.title }}</span><br>
      <small class="text-muted m-1">Текст записи: </small>
      <p class="m-1">{{ item.text }}</p>
    </div>
    <p v-show="empty">Вы ещё не оставили ни одной записи на стене.</p>

    <input type="text" placeholder="Введите название" class="form-control my-1" name="title" v-model="form.title" required>
    <div class="invalid-feedback">Введите название.</div>
    <span class="text-danger">{{ validate_errors.title }}</span>
    <textarea placeholder="Введите текст" class="form-control my-1" name="text" rows="5" v-model="form.text"
              required></textarea>
    <span class="text-danger">{{ validate_errors.text }}</span>
    <button class="w-100 btn btn-lg btn-primary" @click="addEntry">Создать запись</button>
  </div>
</template>

<script>
import axios from "axios";
import qs from "qs";
import store from "@/store";
import Navigation from "@/components/Navigation";

export default {
  name: "WallView",
  components: {Navigation},
  data() {
    return {
      empty: null,
      entries: {
        entry: []
      },
      form: {
        title: '',
        text: ''
      },
      validate_errors: {
        title: '',
        text: ''
      }
    }
  },
  methods: {
    getEntry() {
      axios.post('/api/wall/entries/', qs.stringify({user_id: store.getters.getToken}), {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.entries = resp.data.entries
              this.empty = false
            } else if (resp.data.empty) {
              this.empty = true
            }
          })
    },
    addEntry() {
      axios.post('/api/wall/add_entry/', qs.stringify(this.form), {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.form.title = ''
              this.form.text = ''
              this.getEntry()
            } else {
              this.validate_errors = resp.data.validate_errors
            }
          })
    },
    getDate(date) {
      let time = new Date(date)
      return time.getUTCFullYear()
    }
  },
  mounted() {
    this.getEntry()
  }
}
</script>

<style scoped>

</style>