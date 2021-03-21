<template>
  <div>
    <!-- {{dataInfo}} -->
    <b-form @submit="onSubmit">
      <b-form-group id="input-group" label="New Company ID:" label-for="input1">
        <b-form-input id="input1" v-model="compid" placeholder="Enter the new CompanyID" required></b-form-input>
      </b-form-group>
      <b-button block type="submit" variant="primary">Submit</b-button>
    </b-form>
    <div>
    <b-table striped hover :items="items"></b-table>
    </div>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "home",
  data: function () {
    return {
      dataInfo: {},
      items: [],
      compid: ''
    }
  },
  mounted () {
    this.items = []
    this.getData()
  },
  methods: {
    onSubmit(event){
      var that = this
      event.preventDefault()
      alert(this.compid)
      const path = "http://127.0.0.1:5000/addDataByID";
      axios
        .get(path, {
          params: {
            'rssd_id': this.compid
          },
          withCredentials: true,
          headers: {
            'secret-key': 'super secret key',
            'Access-Control-Allow-Origin': '*'
          }
        })
        .then(function (response) {
          let data = response.data;
          console.log(data);
          that.getData();
        });
    },
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
          for (let key in that.dataInfo["institutions"]){
            let temp = {"ID":key, "Name":that.dataInfo["institutions"][key]["Name"], "Nickname":that.dataInfo["institutions"][key]["Nick"]}
            that.items.push(temp)
          }
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
