<template>
  <div id="home">
    <!-- {{dataInfo}} -->
    <div class="home_header_layout">
      <h3 class="home_header">
        <span class="home_header_span">Welcome to FFIEC 102 Forms Dashboard</span>
      </h3>
    </div>
    <div v-if="loading">
      <b-spinner small label="Loading..."></b-spinner> <strong>Data In Loading</strong>
    </div>
    <b-modal id="bv-modal" ref="loadingModal" hide-footer hide-header-close no-close-on-backdrop title="Data is Loading">
      <div class="d-flex justify-content-center mb-3">
        <b-spinner label="Loading..."></b-spinner>
      </div>
      <div class="d-block text-center">
        <strong>It may cost about several seconds...</strong>
      </div>
    </b-modal>
    <b-alert
      variant="danger"
      dismissible
      fade
      :show= "errorCatch_notfound"
      @dismissed="errorCatch_notfound=false"
    >
      Institution not found
    </b-alert>
    <b-alert
      variant="warning"
      dismissible
      fade
      :show= "errorCatch_alreadyhave"
      @dismissed="errorCatch_alreadyhave=false"
    >
      {{ error }}
    </b-alert>
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
      <b-button type="submit" variant="primary" :disabled="loading">Submit</b-button>
    </b-form>
    <div>
    <b-table striped hover :items="items"></b-table>
    </div>
  </div>
</template>

<script>
import myAPI from '../../api'

export default {
  name: 'home',
  data: function () {
    return {
      dataInfo: {},
      items: [],
      compId: '',
      compName: '',
      compNickName: '',
      loading: false,
      error: '',
      errorCatch_notfound: false,
      errorCatch_alreadyhave: false
    }
  },
  mounted () {
    this.items = []
    this.getData()
  },
  methods: {
    onSubmit (event) {
      let that = this
      that.loading = true
      that.$refs['loadingModal'].show()
      event.preventDefault()
      myAPI
        .addData('addDataByID', that.compId, that.compName, that.compNickName)
        .then(function (response) {
          let data = response.data
          console.log(data['message'])
          if (data['message'] === 'The institution does not exist') {
            that.error = data['message']
            that.errorCatch_notfound = true
          } else if (data['message'] === 'The institution ' + that.compId + ' already exists') {
            that.error = data['message']
            that.errorCatch_alreadyhave = true
          } else {
            that.errorCatch = false
          }
          that.items = []
          that.getData()
        })
        .finally(function () {
          that.loading = false
          that.$refs['loadingModal'].hide()
        })
    },
    getData () {
      let that = this
      that.loading = true
      that.$refs['loadingModal'].show()
      myAPI
        .initData('home') // root route to init data
        .then(function (response) {
          that.dataInfo = response.data
          for (let key in that.dataInfo['institutions']) {
            let temp = {
              'ID': key,
              'Name': that.dataInfo['institutions'][key]['Name'],
              'Nickname': that.dataInfo['institutions'][key]['Nick']
            }
            that.items.push(temp)
          }
        })
        .catch(function (error) {
          alert('Error ' + error)
        })
        .finally(function () {
          that.loading = false
          that.$refs['loadingModal'].hide()
        })
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
.home_header_span{
  font-family: 'Poppins', sans-serif;
  font-weight: bold;
  color: #323030;
}
.home_header{
  margin-bottom: 10px;
}
.home_header_layout{
  border-bottom: 1px solid;
  border-bottom-color: #CACACA;
  margin-bottom: 15px;
  margin-top: 5px;
  box-sizing: border-box;
}

</style>
