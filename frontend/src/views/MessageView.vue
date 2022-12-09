<template>
  <div class="container text-center">
    <navigation></navigation>
    <h3 class="text-center">Ваша переписка с пользователем: </h3>
    <div v-for="date in messages">
      <p>{{ date.date }}</p>
      <div v-for="item in date.messages">
        <div class="row" :class="{'justify-content-end': user_id!==item.sender_id}">
          <div class="col-3">
            <div class="border text-break rounded-4 my-2">
              <p class="mx-2 my-1">{{ item.text }}</p>
              <div class="text-end mx-2 my-1">
                <small class="text-muted">{{ getTime(item.date) }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <textarea class="form-control" placeholder="Введите текс" v-model="form.text" name="text" required></textarea>
    <span class="text-danger">{{ validate_errors.text }}</span>
    <button @click="sendMessage" class="w-100 btn btn-lg btn-primary">Отправить</button>
  </div>
</template>

<script>
import Navigation from "@/components/Navigation";
import axios from "axios";
import qs from "qs";
import store from "@/store";

export default {
  name: "MessageView",
  components: {Navigation},
  data() {
    return {
      user_id: null,
      messages: {
        message: []
      },
      form: {
        text: ''
      },
      validate_errors: {
        text: ''
      }
    }
  },
  methods: {
    getMessages() {
      axios.post('api/friends/get_messages/', qs.stringify({user_id: this.user_id}), {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.messages = resp.data.messages
            } else {

            }
          })
    },
    sendMessage() {
      axios.post('api/friends/send_message/', qs.stringify({user_id: this.user_id, ...this.form}), {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.getMessages()
              this.form.text = ''
            } else {
              this.validate_errors = resp.data.validate_errors
            }
          })
    },
    getTime(date) {
      let time = new Date(date.toString())
      return time.getHours().toString() + ":" + time.getMinutes().toString()
    }
  },
  mounted() {
    this.user_id = this.$route.params.id
    this.getMessages()
  }
}
</script>

<style scoped>

</style>