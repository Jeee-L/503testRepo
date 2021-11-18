<template>
  <div id="add_post">
    <h1>Add Post</h1>
    <input type="text" v-model = "form.add_post_title"  placeholder="add_post_title" />
    <br>
    <input type="radio" v-model = "form.picked_tag"  id="open_world_role_play" value = "open_world_role_play" checked />
    <label for = "open_world_role_play">open_world_role_play</label>
    <br>
    <input type="radio" v-model = "form.picked_tag" id="board_game" value = "board_game" />
    <label for = "board_game">board_game</label>
    <br>
    <input type="radio" v-model = "form.picked_tag" id="side_scrolling" value = "side_scrolling" />
    <label for = "side_scrolling">side_scrolling</label>
    <br>
    <strong>{{ picked_tag }}</strong>
    <br>
    <textarea id = "add_post_content" v-model = "form.add_post_content" placeholder="post content"></textarea>
    <br>
    <input type="button" id = "add_post_button" @click= "add_post" value = "add_post">
    <br>
    <strong>{{ message_add_post }}</strong>
    <br>
  </div>


</template>

<script>
import axios from "axios";

export default {
  name: "add_post",
  data() {
    return {
      form: {
        add_post_title: "",
        picked_tag: "",
        add_post_content: "",
        creator: ""
      },
      message_add_post: ""
    }
  },
  methods: {
    add_post() {
      this.form.creator = sessionStorage.getItem("current_username");
      axios
          .post('http://127.0.0.1:5000/add_post', this.form)
          .then(res => {
            this.message_add_post = res.data.message;
            this.$bus.emit('update_after_add_post');
          })
          .catch(error => {
            console.log(error)
          })
    }
  }
}
</script>

<style scoped>

</style>