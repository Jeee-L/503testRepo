<template>

  <strong>Register</strong>
  <br>
  <input type="text" v-model = "form.username_register"  placeholder="username_reg">
  <br>
  <input type="password" v-model = "form.password_register" placeholder="password_reg">
  <br>
  <input type="button" id = "register_button" @click= "user_register" value = "register">
  <br>
  <strong>{{ register_message }}</strong>
  <br>
</template>

<script>
import axios from "axios";
export default {
  name: "register",
  // refer to https://5balloons.info/post-form-data-to-api-using-axios-in-vuejs/
  data() {
    return {
      form: {
        username_register: "",
        password_register: ""
      },
      register_message: ""
    }
  },
  methods: {
    user_register() {
      axios
          .post('http://127.0.0.1:5000/register', this.form)
          .then(res => {
            this.register_message = res.data.message;
          })
          .catch(error => {
            console.log(error)
          })
    }
  }
}
</script>
<style scoped>

</style>