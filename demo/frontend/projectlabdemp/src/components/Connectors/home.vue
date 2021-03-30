<template>
  <div id="home">
    <!-- {{dataInfo}} -->
    <div v-if="loading">
      <b-spinner small label="Loading..."></b-spinner> <strong>Data In Loading</strong>
    </div>
    <b-form id = 'homeBForm' inline @submit="onSubmit">
      <b-form-group id="id-input-group" label="New Company ID:" label-for="id-input">
        <b-form-input id="id-input" v-model="compId" placeholder="Enter the new company RSSD ID" required></b-form-input>
      </b-form-group>
      <b-form-group id="name-input-group" label="New Company Name:" label-for="name-input">
        <b-form-input id="name-input" v-model="compName" placeholder="Enter the new company Name" required></b-form-input>
      </b-form-group>
      <b-form-group id="nick-input-group" label="New Company Nick Name:" label-for="nick-input">
        <b-form-input id="nick-input" v-model="compNickName" placeholder="Enter the new company Nick Name" required></b-form-input>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
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
      compId: '',
      compName: '',
      compNickName: '',
      loading: false
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
      // alert(this.compId)
      const path = "http://127.0.0.1:5000/addDataByID";
      axios
        .get(path, {
          params: {
            'rssd_id': this.compId,
            'name': this.compName,
            'nickName': this.compNickName
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
          that.items = []
          that.getData();
        });
    },
    getData () {
      var that = this;
      that.loading = true
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
        })
        .finally(()=>(that.loading = false));
    }
  }
}
</script>

<style scoped>
#id-input-group {
  margin: 5px;
}
#id-input{
  margin: 10px;
  width: 280px;
}

#name-input-group {
  margin: 5px;
}
#name-input{
  margin: 10px;
  width: 280px;
}

#nick-input-group {
  margin: 5px;
}
#nick-input{
  margin: 10px;
  width: 280px;
}

</style>
