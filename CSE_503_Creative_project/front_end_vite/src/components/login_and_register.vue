<template>
  <h1>{{ msg }}</h1>

    <h2>
      {{ info }}
    </h2>

  <input type="button" id = "login_button" @click= "user_login" value = "log in">
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

defineProps({
  msg: String
})

const count = ref(0)

const info = ref(null)

axios.
  get('http://localhost:5000/test').
  then(res=>{
    info.value = res.data;
	})


</script>