<template>
  <h1>All_post</h1>
  <strong>{{ message_display_all_post }}</strong>
  <br>
  <strong> {{ operation_message }} </strong>
  <div id = "all_post_display_block">
    <ul id = "all_post_display_block_list_main">
      <li v-for = "every_post in all_posts">
        <div>
          <strong>{{ "Title: " + every_post["post_title"] + "; Tag: " + every_post["post_tag"]   }}</strong>
          <br>
          <strong>{{every_post["time"] }}</strong>
          <br>
          <strong>{{"creator: " + every_post["creator"] }}</strong>
          <p>
            {{  every_post["post_content"] }}
          </p>
          <br>
          <div>
            <div id = "shared_post_node" v-show= "current_user">
              <select v-model = "selected_friend">
                <option v-for = "every_friend in friend_list" :value="every_friend">{{ every_friend }}</option>
              </select>
              <input type="button" @click= "share_post(every_post['_id'])" value = "share_post"/>
            </div>
          </div>
          <br>
          <div v-show="this.current_user === every_post['creator']">
            <button type="button" @click="delete_post(every_post['_id'])">Delete Post</button><br>
            <edit_post :postId="every_post['_id']"/>
          </div>
          <br>
          <div>
            <div id = "comments_and_like_node" v-show= "current_user">
              <comments :postId="every_post['_id']"/>
              <likes :postId="every_post['_id']"/>
            </div>
          </div>
        </div>
      </li>
    </ul>
  </div>
  <hr>
</template>

<script>
import axios from "axios";
import edit_post from "./edit_post.vue";
import comments from "./comments.vue";
import likes from "./likes.vue";
export default {
  components: {
    edit_post,
    comments,
    likes
  },
  name: "display_all_post",
  data() {
    return {
      all_posts: {},
      message_display_all_post: "",
      current_user: "",
      operation_message: "",
      selected_friend: "",
      friend_list: "",
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
              // https://www.w3schools.com/jsref/met_loc_reload.asp
              location.reload();
              this.operation_message = res.data.message;
            })
            .catch(error => {
              console.log(error)
            });
    },
   
    share_post(id) {
      axios
        .post('http://127.0.0.1:5000/share_post', {
          "shared_post_id":id,
          "shared_to_username" : this.selected_friend,
          "shared_from_username" : this.current_user,
        })
        .then(res => {
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
        .post('http://127.0.0.1:5000/display_all_post', {
          "current_user" : sessionStorage.getItem("current_username")
        })
        .then(res => {
          this.all_posts = res.data.all_posts;
          // console.log(res.data.all_posts)
          this.message_display_all_post = res.data.message;
          this.friend_list = res.data.friend_list;
          this.current_user = sessionStorage.getItem("current_username");
        })
        .catch(error => {
          console.log(error)
        });

      this.$bus.on('update_after_login', () => {
         this.current_user = sessionStorage.getItem("current_username");
      })
      // console.log(sessionStorage.getItem("current_login_or_not"))
      if (sessionStorage.getItem("current_login_or_not")){
         this.current_user = sessionStorage.getItem("current_username");
      }

    this.$bus.on('update_after_add_post', () => {
      axios
        .post('http://127.0.0.1:5000/display_all_post', {
          "current_user" : sessionStorage.getItem("current_username")
        })
        .then(res => {
          this.all_posts = res.data.all_posts;
          this.message_display_all_post = res.data.message;
          this.friend_list = res.data.friend_list;
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