<template>
  <h1>All_post</h1>
  <strong>{{ message_display_all_post }}</strong>
  <strong> {{ operation_message }} </strong>
  <div id = "all_post_display_block">
    <ul id = "all_post_display_block_list_main">
      <li v-for = "every_post in all_posts">
        <div>
          <strong>{{ "Title: " + every_post["post_title"] + "; Tag: " + every_post["post_tag"] + "; Created Time: " + every_post["time"] }}</strong>
          <p>
            {{  every_post["post_content"] }}
          </p>
          <div v-show="this.current_user === every_post['creator']">
            <button type="button" @click="delete_post(every_post['_id'])">Delete Post</button><br>
            New title: <input type="text" v-model = "edit_form.edit_title"  placeholder="new title" /><br>
            New content: <textarea v-model = "edit_form.edit_content" placeholder="new content"></textarea><br>
            <button type="button" @click="edit_post(every_post['_id'])">Submit Edit Post</button><br>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "display_all_post",
  data() {
    return {
      all_posts: {},
      message_display_all_post: "",
      current_user: "",
      operation_message: "",
      edit_form:{
        edit_title: "",
        edit_content: "",
        creator: "",
      },
    }
  },
  methods: {
    delete_post(id){
      // console.log(time);
          axios
            .post('http://127.0.0.1:5000/delete_post', {"delete_id":id})
            .then(res => {
              console.log(res.data);
              // refresh page, reference: https://www.jb51.net/article/215889.htm
              location.reload();
              this.operation_message = res.data.message;
            })
            .catch(error => {
              console.log(error)
            });
    },
    edit_post(id){
      this.edit_form.creator = this.current_user;
      axios
        .post('http://127.0.0.1:5000/edit_post', {"edit_id":id, "edit_form":this.edit_form})
        .then(res => {
          console.log(res.data);
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
        .post('http://127.0.0.1:5000/display_all_post')
        .then(res => {
          this.all_posts = res.data.all_posts;
          this.message_display_all_post = res.data.message;
          this.current_user = sessionStorage.getItem("current_username");
        })
        .catch(error => {
          console.log(error)
        });


    this.$bus.on('update_after_add_post', () => {
      axios
        .post('http://127.0.0.1:5000/display_all_post')
        .then(res => {
          this.all_posts = res.data.all_posts;
          this.message_display_all_post = res.data.message;
          this.current_user = sessionStorage.getItem("current_username");
        })
        .catch(error => {
          console.log(error)
        })
    });
  }
}
</script>

<style scoped>

</style>