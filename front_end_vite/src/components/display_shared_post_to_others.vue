<template>
    <div id = "share_post_to_others">
    <strong>All_share_post_to_others</strong>
      <ul>
        <li v-for = "(every_share_post_to_others, index) in all_share_post_to_others_list">
          <div>
            <strong>{{"Shared to "  + every_share_post_to_others["username_this_post_shared_to"] }}</strong>
            <br>
            <strong>{{ "Title: " + every_share_post_to_others["post_title"] + "; Tag: " + every_share_post_to_others["post_tag"]   }}</strong>
            <br>
            <strong>{{every_share_post_to_others["time"] }}</strong>
            <br>
            <strong>{{"creator: " + every_share_post_to_others["creator"] }}</strong>
            <p>
              {{  every_share_post_to_others["post_content"] }}
            </p>
            <br>
            <input
                type="button"
                @click="withdraw_shared_post(every_share_post_to_others['_id'], every_share_post_to_others['username_this_post_shared_to'] )"
                value = "withdraw"/>
          </div>
        </li>
      </ul>
    </div>
    <hr>
</template>

<script>
import axios from "axios";

export default {
  name: "shared_post_to_others",
    data() {
    return {
      all_share_post_to_others_list: {},
      current_user: "",
      operation_message: ""
    }
  },
  methods: {
    withdraw_shared_post(id, username_this_post_shared_to){
          axios
            .post('http://127.0.0.1:5000/withdraw_shared_post', {
              "current_user" : sessionStorage.getItem("current_username"),
              "username_share_this_post_to" : username_this_post_shared_to,
              "withdraw_shared_post_id": id
            })
            .then(res => {
              // refresh page, reference: https://www.jb51.net/article/215889.htm
              // https://www.w3schools.com/jsref/met_loc_reload.asp
              location.reload();
              this.operation_message = res.data.message;
            })
            .catch(error => {
              console.log(error)
            });
    }
  },
  mounted() {
    axios
        .post('http://127.0.0.1:5000/display_all_share_post_to_others', {
          "current_user" : sessionStorage.getItem("current_username")
        })
        .then(res => {
          this.all_share_post_to_others_list = res.data.all_share_post_to_others_list;
          console.log(res.data.all_share_post_to_others_list)
          this.operation_message = res.data.message;
          this.current_user = sessionStorage.getItem("current_username");
        })
        .catch(error => {
          console.log(error)
        });
  }
}
</script>

<style scoped>

</style>