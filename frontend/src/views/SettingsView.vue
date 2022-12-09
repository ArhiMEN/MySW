<template>
  <div class="container">
    <navigation></navigation>
    <input class="form-control" type="file" name="new_avatar" ref="file" required>
    <span class="text-danger">{{ validate_errors.new_avatar }}</span>
    <button @click="changeAvatar" class="w-100 btn btn-lg btn-primary">Сменить аватарку</button>
  </div>
</template>

<script>
import Navigation from "@/components/Navigation";
import axios from "axios";
import store from "@/store";

export default {
  name: "SettingsView",
  components: {Navigation},
  data() {
    return {
      validate_errors: {
        new_avatar: '',
      }
    }
  },
  methods: {
    changeAvatar() {
      const formData = new FormData()
      formData.append('new_avatar', this.$refs.file.files[0])
      axios.post('api/settings/change_avatar/', formData, {
        headers: {
          'Authorisation': store.getters.getToken,
          'Content-Type': 'multipart/form-data'
        }
      })
          .then((resp) => {
            if (resp.data.success) {
              this.$refs.file.value = null
              this.validate_errors.new_avatar = ''
            } else {
              this.validate_errors = resp.data.validate_errors
            }
          })
    },
  },
}
</script>

<style scoped>

</style>