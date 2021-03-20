<template>
  <div :data="dataInfo">
    test home page
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "home",
  data: function () {
    return {
      dataInfo: {}
    }
  },
  mounted () {
    this.getData();
  },
  methods: {
    getData () {
      var that = this;
      // root route to init data
      const path = "http://127.0.0.1:5000/home";
      axios
        .get(path, {
          withCredentials: true,
          headers: {
            'secret-key': 'super secret key',
            'Access-Control-Allow-Origin': 'http://127.0.0.1:5000'
          }
        })
        .then(function (response) {
          that.dataInfo = response.data;
        })
        .catch(function (error) {
          alert("Error " + error);
        });
    }
  }
}
</script>

<style scoped>

</style>
