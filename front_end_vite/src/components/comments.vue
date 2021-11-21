<template>
  <div id="display all comments">
    <ul>
      <li v-for="every_comment in comment_list">
        <div>
          {{ every_comment['comment_content'] + " BY " + every_comment['comment_creator']}}
          <div id="delete_comment" v-show="current_user === every_comment['comment_creator']">
            <input type="button" @click= "delete_comment(postId, every_comment['_id'])" value = "delete comment"/>
          </div>
        </div>
      </li>
    </ul>
    <div id = "add_comments">
      <textarea id = "add_post_content" v-model = "add_comment_content" placeholder="comment content"></textarea>
      <input type="button" id = "add_comment_button" @click= "add_comment(postId)" value = "add_comment">
    </div>
  </div>
  <br>
</template>

<script setup>
    defineProps({
        postId: String
    })
</script>

<script>
import axios from "axios";

export default {
  name: "comments",
  data() {
    return {
      comment_list: [],
      current_user: "",
      operation_message: "",
      add_comment_content:""
    }
  },
  methods: {
    delete_comment(postId, id) {
          axios
            .post('http://127.0.0.1:5000/delete_comment',
                {
                  "post_id": postId,
                  "comment_id_to_delete": id
                })
            .then(res => {
              // console.log(res.data);
              // refresh page, reference: https://www.jb51.net/article/215889.htm
              // https://www.w3schools.com/jsref/met_loc_reload.asp
              location.reload();
              this.operation_message = res.data.message;
            })
            .catch(error => {
              console.log(error)
            });
    },
    add_comment(postId) {
          axios
            .post('http://127.0.0.1:5000/add_comment',
                {
                  "postId":postId,
                  "current_user" : sessionStorage.getItem("current_username"),
                  "add_comment_content" : this.add_comment_content
                })
            .then(res => {
              // console.log(res.data);
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
        .post('http://127.0.0.1:5000/display_all_comment', {
          "current_user" : sessionStorage.getItem("current_username"),
          "postId" : this.postId
        })
        .then(res => {
          // console.log(res.data.all_posts)
          this.operation_message = res.data.message;
          this.comment_list = res.data.all_comments;
          // console.log( this.comment_list)
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