<template>
  <h1>{{ msg }}</h1>

    <h2>
      {{ info }}
    </h2>

  <button type="button" @click="count++">count is: {{ count }}</button>
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
  get('http://127.0.0.1:5000/test').
  then(res=>{
    info.value = res.data;
	})


</script>