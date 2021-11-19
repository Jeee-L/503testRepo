<template>
  <div v-show = 'current_login_or_not' >
      <strong>send_friend_request </strong>
      <br>
      <input type="text" v-model = "form.username_to_receive_friend_request"  placeholder="username_to_add_friend">
      <br>
      <input type="button" id = "send_friend_request_button" @click= "send_friend_request" value = "send_friend_request">
      <br>
      <strong>{{ message_send_friend_request }}</strong>
      <hr>
  </div>

</template>

<script>
import axios from 'axios';
export default {
  name: "send_friend_request",
  data() {
    return {
      form:{
        username_to_receive_friend_request: "",
        username_to_send_friend_request: ""
      },
      message_send_friend_request: "",
      current_login_or_not: false
    }
  },
  mounted() {
     this.$bus.on('update_after_login', () => {
          this.current_login_or_not = true;
          this.form.username_to_send_friend_request = sessionStorage.getItem("current_username")
     });
      // console.log(sessionStorage.getItem("current_login_or_not"))
      if (sessionStorage.getItem("current_login_or_not")){
         this.current_login_or_not = true;
         this.form.username_to_send_friend_request = sessionStorage.getItem("current_username");
      }
  },
  methods: {
    send_friend_request() {
      axios
          .post('http://127.0.0.1:5000/send_friend_request', this.form)
          .then(res => {
            this.message_send_friend_request = res.data.message_send_friend_request;
          })
          .catch(error => {
            console.log(error)
          })
    }
  },
}
</script>


<style scoped>

</style>