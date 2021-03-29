<template>
  <b-card class="stress-window-table-card" title="Stress Window">
    <b-table class="stress-window-table" id="stress-window-table" striped hover :items="items" :fields="fields"></b-table>
  </b-card>
</template>

<script>
import axios from 'axios';
import helper from '@/helper';

export default {
  name: 'OverTimeTable',
  created () {
    this.getQuarterList = helper.getQuarterList
  },
  data: function () {
    return {
      items: [],
      fields: []
    }
  },
  methods: {
    getData (id, quarterStart, quarterEnd, selected) {
      let that = this;
      const url = 'http://127.0.0.1:5000/getStressWindowOvertime';
      axios
        .get(url, {
          params: {
            'start': quarterStart,
            'end': quarterEnd
          },
          withCredentials: true,
          headers: {
            'secret-key': 'super secret key',
            'Access-Control-Allow-Origin': '*'
          }
        })
        .then(function (response) {
          let data = response.data
          let quarterList = that.getQuarterList(quarterStart, quarterEnd);
          console.log(quarterList)
          let items = []
          for (const quarter of quarterList) {
            items.push({'Quarter': quarter});
          }
          let fields = ['Quarter']
          for (let key of selected) {
            if (data.hasOwnProperty(key)) {
              fields.push(key)
              for (let i = 0; i < data[key].length; ++i) {
                items[i][key] = data[key][i][1];
              }
            }
          }
          items.reverse();
          console.log(fields)
          console.log(items)
          that.fields = fields
          that.items = items
        });
    }
  }
}
</script>

<style scoped>

.stress-window-table-card {
  max-width: 80rem;
  max-height: 40rem;
  margin-bottom: 20px;
}

.stress-window-table {
  width: 100%;
  height: 35rem;
  display: inline-block;
}

</style>
