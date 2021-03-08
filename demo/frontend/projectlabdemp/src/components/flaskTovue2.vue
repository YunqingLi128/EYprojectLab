<template>
  <div>
    <bar-chart></bar-chart>
    <stack-bar-chart></stack-bar-chart>
  </div>
</template>

<script>
import axios from 'axios';
import BarChart from "./BarChart";
import StackBarChart from "./StackBarChart";

export default {
  name: "my-first-vue",
  components: {BarChart, StackBarChart},
  data: function() {
    return {
      serverResponse: "Waiting for server response"
    };
  },
  methods: {
    getData() {
      var that = this;
      const path = "http://127.0.0.1:5000/getMsg";
      axios
        .get(path)
        .then(function(response) {
          var msg = response.data.msg;
          that.serverResponse = msg;

          alert(
            "Success " + response.status + ", " + response.data + ", " + msg
          );
        })
        .catch(function(error) {
          alert("Error " + error);
        });
    }
  }
};
</script>
