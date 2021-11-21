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
              <input type="button" @click=  "share_post(every_post['_id'])" value = "share_post"/>
            </div>

          </div>
          <br>
          <div v-show="this.current_user === every_post['creator']">
            <button type="button" @click="delete_post(every_post['_id'])">Delete Post</button><br>
            New title: <input type="text" v-model = "edit_form.edit_title"  placeholder="new title" /><br>
            New content: <textarea v-model = "edit_form.edit_content" placeholder="new content"></textarea><br>
            New tag:
            <br>
            <input type="radio" v-model = "edit_form.edit_tag"  id="open_world_role_play" value = "open_world_role_play" checked />
            <label for = "open_world_role_play">open_world_role_play</label>
            <br>
            <input type="radio" v-model = "edit_form.edit_tag" id="board_game" value = "board_game" />
            <label for = "board_game">board_game</label>
            <br>
            <input type="radio" v-model = "edit_form.edit_tag" id="side_scrolling" value = "side_scrolling" />
            <label for = "side_scrolling">side_scrolling</label>
            <br>
            <button type="button" @click="edit_post(every_post['_id'])">Submit Edit Post</button><br>
          </div>
        </div>
      </li>
    </ul>
  </div>
  <hr>
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
      selected_friend: "",
      friend_list: "",
      edit_form:{
        edit_title: "",
        edit_content: "",
        creator: "",
        edit_tag: "",
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
              // https://www.w3schools.com/jsref/met_loc_reload.asp
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
    },
    share_post(id) {
      axios
        .post('http://127.0.0.1:5000/share_post', {
          "shared_post_id":id,
          "shared_to_username" : this.selected_friend,
          "shared_from_username" : this.current_user,
        })
        .then(res => {
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