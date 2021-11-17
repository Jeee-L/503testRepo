<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup

import register from "./components/register.vue";
import login from "./components/login.vue";
import display_all_post from "./components/display_all_post.vue";
import add_post from "./components/add_post.vue";

</script>

<template>
  <register/>
  <login/>
  <display_all_post/>
  <add_post/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
