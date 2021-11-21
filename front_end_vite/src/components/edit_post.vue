<template>
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
    <button type="button" @click="edit_post(postId)">Submit Edit Post</button><br>
</template>

<script setup>
    defineProps({
        postId: String
    })
</script>


<script>
    import axios from "axios";
    export default {
        name: "edit_post",
        data() {
            return {
               all_posts: {},
               current_user: "",
                edit_form:{
                    edit_title: "",
                    edit_content: "",
                    creator: "",
                    edit_tag: "",
                },
            }
        },
        methods:{
             edit_post(id){
                this.edit_form.creator = sessionStorage.getItem("current_username");
                axios
                    .post('http://127.0.0.1:5000/edit_post', {"edit_id":id, "edit_form":this.edit_form})
                    .then(res => {
                    // console.log(res.data);
                    location.reload();  // refresh page
                    this.operation_message = res.data.message;
                    })
                    .catch(error => {
                    console.log(error)
                    });
                },
        },
    }
</script>
