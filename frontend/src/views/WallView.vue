<template>
  <div class="container">
    <navigation></navigation>
    <p  v-show="!empty" v-for="item in entries" class="border text-break">
      <small class="text-muted">Название записи: </small>
      <span class="fst-italic fw-bold">{{ item.title }}</span><br>
      <small class="text-muted">Дата записи: </small>
      <u>{{ item.date }}</u><br>
      <small class="text-muted">Текст записи: </small>
      {{ item.text }}
    </p>
    <p v-show="empty">Вы ещё не оставили ни одной записи на стене.</p>

    <input type="text" placeholder="Введите название" class="form-control" name="title" v-model="form.title" required>
    <div class="invalid-feedback">Введите название.</div>
    <span class="text-danger">{{ validate_errors.title }}</span>
    <textarea placeholder="Введите текст" class="form-control" name="text" rows="5" v-model="form.text"
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
      axios.post('/api/wall/entries/', qs.stringify({user_id: store.getters.getToken}),{headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.entries = resp.data.entries
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
    }
  },
  mounted() {
    this.getEntry()
  }
}
</script>

<style scoped>

</style>