<template>
  <div class="container">
    <navigation></navigation>
    <div v-show="!empty" v-for="item in files" class="my-4">
      Имя файла: <span class="text-warning">{{ item.name }}</span><br>
      <div v-if="item.is_image">Файл: <img :src="item.url" alt="mdo" width="32" height="32"><br></div>
      <a :download="item.pure_name" :href="'api/files/download/' + item.id + '/'" class="btn btn-success btn-sm">Скачать файл</a>
      <button @click="deleteFile(item.id)" class="btn btn-danger btn-sm m-1">
        Удалить
      </button>
    </div>

    <label for="name" class="form-label">Введите имя файла</label>
    <input type="text" class="form-control" name="name" v-model="form.name" required>
    <span class="text-danger">{{ validate_errors.name }}</span><br>
    <input type="file" name="new_file" ref="file" required><br>
    <span class="text-danger">{{ validate_errors.new_file }}</span>
    <button @click="uploadFile" class="w-100 btn btn-lg btn-primary">Сохранить файл</button>
  </div>
</template>

<script>
import Navigation from "@/components/Navigation";
import axios from "axios";
import store from "@/store";
import qs from "qs";

export default {
  name: "FilesView",
  components: {Navigation},
  data() {
    return {
      empty: null,
      files: {
        file: []
      },
      form: {
        name: '',
      },
      validate_errors: {
        name: '',
        new_file: '',
      }
    }
  },
  methods: {
    getFiles() {
      axios.get('/api/files/get/', {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.files = resp.data.files
              this.empty = false
            } else if (resp.data.empty) {
              this.empty = true
            }
          })
    },
    uploadFile() {
      const formData = new FormData()
      formData.append('new_file', this.$refs.file.files[0])
      formData.append('name', this.form.name)
      formData.append('user_id', this.$store.getters.getToken)
      axios.post('api/files/upload/', formData, {
        headers: {
          'Authorisation': store.getters.getToken,
          'Content-Type': 'multipart/form-data'
        }
      })
          .then((resp) => {
            if (resp.data.success) {
              this.form.name = ''
              this.$refs.file.value = null
              this.getFiles()
            } else {
              this.validate_errors = resp.data.validate_errors
            }
          })
    },
    deleteFile(file_id) {
      axios.post('/api/files/delete/', qs.stringify({file_id}), {headers: {'Authorisation': store.getters.getToken}})
          .then((resp) => {
            if (resp.data.success) {
              this.getFiles()
            } else {
              // send error
            }
          })
    },
  },
  mounted() {
    this.getFiles()
  }
}
</script>

<style scoped>

</style>