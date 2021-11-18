<template>
  <div v-show = '!current_login_or_not' >
      <strong>Log In</strong>
      <br>
      <input type="text" v-model = "form.username_login"  placeholder="username_login">
      <br>
      <input type="password" v-model = "form.password_login" placeholder="password_login">
      <br>
      <input type="button" id = "register_button" @click= "user_login" value = "login">
      <br>
      <strong>{{ message_login }}</strong>
      <br>
  </div>

</template>

<script>
import axios from 'axios';
export default {
  // refer to https://5balloons.info/post-form-data-to-api-using-axios-in-vuejs/
  name: "login",
  data() {
    return {
      form: {
        username_login: "",
        password_login: ""
      },
      message_login: "",
      current_username: "",
      current_login_or_not: false
    }
  },
  methods: {
    user_login() {
      axios
          .post('http://127.0.0.1:5000/login', this.form)
          .then(res => {
            this.message_login = res.data.message;
            if (res.data.success) {
              sessionStorage.setItem("current_username", res.data.current_username);
              sessionStorage.setItem("current_login_or_not", "true");
              this.current_login_or_not = true;
              this.$bus.emit('update_after_login')
            }
          })
          .catch(error => {
            console.log(error)
          })
    }
  },
  mounted() {
    this.current_login_or_not = sessionStorage.getItem("current_login_or_not");
    console.log(this.current_login_or_not)
  }
}
</script>


<style scoped>

</style>