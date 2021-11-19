<template>
  <div id = "notification" v-show = 'current_login_or_not'>
    <strong>All notification</strong>
      <ul>
        <li v-for = "(every_notification, index) in notification_list">
          <div>
            <strong>{{"friend request: " +  every_notification }}</strong>
            <br>
            <input type="button" @click="refuse(every_notification)" value = "refuse"/>
            <input type="button" @click="accept(every_notification)" value = "accept"/>
          </div>
        </li>
      </ul>
  </div>
  <hr>
</template>

<script>
import axios from 'axios';
export default {
  name: "notification",
  data() {
    return {
      notification_list: [],
      current_login_or_not: false,
      form: {
        current_user: ""
      }
    }
  },
  mounted() {
    this.$bus.on('update_after_login', () => {
          this.current_login_or_not = true;
          this.form.current_user = sessionStorage.getItem("current_username");
          // console.log(sessionStorage.getItem("current_username"))
          axios
            .post('http://127.0.0.1:5000/notification', this.form)
            .then(res => {
              this.notification_list = res.data.notification_list;
            })
            .catch(error => {
              console.log(error)
            });
    });

    // console.log(sessionStorage.getItem("current_login_or_not"))
    if (sessionStorage.getItem("current_login_or_not")){
      this.current_login_or_not = true;
      this.form.current_user = sessionStorage.getItem("current_username");
      // console.log(sessionStorage.getItem("current_username"))
      axios
      .post('http://127.0.0.1:5000/notification', this.form)
      .then(res => {
        this.notification_list = res.data.notification_list;
      })
      .catch(error => {
        console.log(error)
      });
    }
  },
  methods: {
    refuse(every_notification) {
       axios
          .post('http://127.0.0.1:5000/refuse',
              {"refuse_username":every_notification,
                "current_user": this.form.current_user
              })
          .then(res => {
            // console.log(res.data);
            location.reload();
            this.operation_message = res.data.message;
          })
          .catch(error => {
            console.log(error)
          });
    },
    accept(every_notification) {
        axios
          .post('http://127.0.0.1:5000/accept',
              {"accept_username":every_notification,
                "current_user": this.form.current_user
              })
          .then(res => {
            // console.log(res.data);
            location.reload();
            this.operation_message = res.data.message;
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