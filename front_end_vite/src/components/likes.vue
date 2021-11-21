<template>
  <div>
    {{ "number_of_likes " + number_of_likes }}
    <input type="button" @click = "add_like(postId)" value = "LIKE" v-show="!this.liked_or_not"/>
     <input type="button" @click = "unlike(postId)" value = "UNLIKE" v-show="this.liked_or_not"/>
  </div>
</template>

<script setup>
    defineProps({
        postId: String
    })
</script>

<script>
import axios from "axios";

export default {
  name: "likes",
  data() {
    return {
      number_of_likes: 0,
      current_user: "",
      liked_or_not: false
    }
  },
  methods :{
    add_like(postId) {
       axios
        .post('http://127.0.0.1:5000/add_like',
            {
              "post_id": this.postId,
              "current_user": sessionStorage.getItem("current_username")
            })
        .then(res => {
          location.reload();
          this.liked_or_not = true
          this.operation_message = res.data.message;
        })
        .catch(error => {
          console.log(error)
        });
    },
    unlike(postId) {
      axios
          .post('http://127.0.0.1:5000/unlike',
              {
                "post_id": this.postId,
                "current_user": sessionStorage.getItem("current_username")
              })
          .then(res => {
            location.reload();
            this.liked_or_not = false
            this.operation_message = res.data.message;
          })
          .catch(error => {
            console.log(error)
          });
    }
  },
  mounted() {
     axios
        .post('http://127.0.0.1:5000/fetch_like',
            {
              "post_id": this.postId,
              "current_user": sessionStorage.getItem("current_username")
            })
        .then(res => {
          this.operation_message = res.data.message;
          this.number_of_likes = res.data.number_of_likes;
          this.current_user = sessionStorage.getItem("current_username")
          this.liked_or_not = res.data.liked_or_not
        })
        .catch(error => {
          console.log(error)
        });

     this.$bus.on('update_after_login', () => {
       axios
          .post('http://127.0.0.1:5000/fetch_like',
              {
                "post_id": this.postId,
                "current_user": sessionStorage.getItem("current_username")
              })
          .then(res => {
            this.operation_message = res.data.message;
            this.number_of_likes = res.data.number_of_likes;
            this.current_user = sessionStorage.getItem("current_username")
            this.liked_or_not = res.data.liked_or_not
          })
          .catch(error => {
            console.log(error)
          });
    });

  }
}
</script>

<style scoped>

</style>