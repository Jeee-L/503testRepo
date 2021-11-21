<template>
<div id = "display_friend_list" v-show = 'current_login_or_not'>
    <strong>display_friend_list</strong>
      <ul>
        <li v-for = "(every_friend, index) in friend_list">
          <div>
            <strong>{{ every_friend }}</strong>
            <br>
            <input type="button" @click="unfriend(every_friend)" value = "unfriend"/>
          </div>
        </li>
      </ul>
  </div>
  <hr>
</template>

<script>
import axios from "axios";

export default {
  name: "display_friend_list",
  data() {
    return {
      friend_list: {},
      current_user: "",
      current_login_or_not: false
    }
  },
  mounted() {
    this.$bus.on('update_after_login', () => {
          this.current_login_or_not = true;
          this.current_user = sessionStorage.getItem("current_username");
          // console.log(sessionStorage.getItem("current_username"))
          axios
            .post('http://127.0.0.1:5000/display_friend_list',
                {current_user : sessionStorage.getItem("current_username")})
            .then(res => {
              this.friend_list = res.data.friend_list;
            })
            .catch(error => {
              console.log(error)
            });
    });

    // console.log(sessionStorage.getItem("current_login_or_not"))
    if (sessionStorage.getItem("current_login_or_not")){
      this.current_login_or_not = true;
      this.current_user = sessionStorage.getItem("current_username");
      // console.log(sessionStorage.getItem("current_username"))
      axios
      .post('http://127.0.0.1:5000/display_friend_list',
          {current_user : sessionStorage.getItem("current_username")})
      .then(res => {
        this.friend_list = res.data.friend_list;
      })
      .catch(error => {
        console.log(error)
      });
    }
  },
  methods: {
    unfriend(every_friend) {
      axios
      .post('http://127.0.0.1:5000/unfriend',
          {
            current_user : sessionStorage.getItem("current_username"),
            username_to_unfriend: every_friend
          })
      .then(res => {
        location.reload();
      })
      .catch(error => {
        console.log(error)
      });
    }
  }
}
</script>

<style scoped>

</style>