<template>
<div id = "share_post_to_you">
    <strong>All_share_post_to_you</strong>
      <ul>
        <li v-for = "(every_share_post_to_you, index) in all_share_post_to_you_list">
          <div>
            <strong>{{"Shared by "  + every_share_post_to_you["username_this_post_shared_from"] }}</strong>
            <br>
            <strong>{{ "Title: " + every_share_post_to_you["post_title"] + "; Tag: " + every_share_post_to_you["post_tag"]   }}</strong>
            <br>
            <strong>{{every_share_post_to_you["time"] }}</strong>
            <br>
            <strong>{{"creator: " + every_share_post_to_you["creator"] }}</strong>
            <p>
              {{  every_share_post_to_you["post_content"] }}
            </p>
            <br>
            <input
                type="button"
                @click="dismiss_shared_post(every_share_post_to_you['_id'], every_share_post_to_you['username_this_post_shared_from'] )"
                value = "dismiss"/>
          </div>
        </li>
      </ul>
    </div>
    <hr>
</template>

<script>
import axios from "axios";

export default {
  name: "shared_post_to_you",
      data() {
    return {
      all_share_post_to_you_list: [],
      current_user: "",
      operation_message: "",
    }
  },
  methods: {
    dismiss_shared_post(id, username_this_post_shared_from){
          axios
            .post('http://127.0.0.1:5000/dismiss_shared_post', {
              "current_user" : sessionStorage.getItem("current_username"),
              "username_this_post_shared_from" : username_this_post_shared_from,
              "dismiss_shared_post_id": id
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
        .post('http://127.0.0.1:5000/display_all_share_post_to_you', {
          "current_user" : sessionStorage.getItem("current_username")
        })
        .then(res => {
          this.all_share_post_to_you_list = res.data.all_share_post_to_you_list;
          // console.log(res.data.all_share_post_to_others_list)
          this.operation_message = res.data.message;
          this.current_user = sessionStorage.getItem("current_username");
        })
        .catch(error => {
          console.log(error)
        });

    this.$bus.on('update_after_login', () => {
         this.current_user = sessionStorage.getItem("current_username");
      axios
        .post('http://127.0.0.1:5000/display_all_share_post_to_you', {
          "current_user" : sessionStorage.getItem("current_username")
        })
        .then(res => {
          this.all_share_post_to_you_list = res.data.all_share_post_to_you_list;
          // console.log(res.data.all_share_post_to_others_list)
          this.operation_message = res.data.message;
          this.current_user = sessionStorage.getItem("current_username");
        })
        .catch(error => {
          console.log(error)
        });
    })
  }
}
</script>

<style scoped>

</style>