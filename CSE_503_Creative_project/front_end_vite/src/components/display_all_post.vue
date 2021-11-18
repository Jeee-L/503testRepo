<template>
  <h1>All_post</h1>
  <strong>{{ message_display_all_post }}</strong>
  <div id = "all_post_display_block">
    <ul id = "all_post_display_block_list_main">
      <li v-for = "every_post in all_posts">
        <div>
          <strong>{{ "Title: " + every_post["post_title"] + "; Tag: " + every_post["post_tag"]}}</strong>
          <p>
            {{  every_post["post_content"] }}
          </p>
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
      message_display_all_post: ""
    }
  },
  mounted() {
    axios
        .post('http://127.0.0.1:5000/display_all_post')
        .then(res => {
          this.all_posts = res.data.all_posts;
          this.message_display_all_post = res.data.message;

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