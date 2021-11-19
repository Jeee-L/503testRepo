<template>
  <div v-show = 'current_login_or_not' >
      <input type="button" @click= "user_logout"  value = "logout">
  </div>
  <strong>{{operation_message }}</strong>
</template>

<script>
export default {
  name: "logout",
  data() {
    return {
      current_login_or_not: false,
      operation_message: ""
    }
  },
  methods: {
    user_logout() {
      sessionStorage.clear();
      // refresh page
      location.reload();
    }
  },
  mounted() {
      this.$bus.on('update_after_login', () => {
          this.current_login_or_not = true;
      })

      if (sessionStorage.getItem("current_login_or_not")){
         this.current_login_or_not = true;

      }
  }
}
</script>

<style scoped>

</style>