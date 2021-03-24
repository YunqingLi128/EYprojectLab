<template>
  <div>
    <b-form inline>
      <b-form-group id="input-group-1" label="Start Quarter: " label-for="input-quarter-1">
        <b-form-input id="input-quarter-1" name="input-quarter" v-model.trim="quarter1"
                      placeholder="example: 2016Q3" required>
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-2" label="End Quarter: " label-for="input-quarter-2">
        <b-form-input id="input-quarter-2" name="input-quarter" v-model.trim="quarter2"
                      placeholder="example: 2020Q3" required>
        </b-form-input>
      </b-form-group>
    </b-form>
    <b-form-group label="Select Company:">
      <b-form-checkbox-group
        id="checkbox-group-1"
        v-model="selected"
        :options="options"
        name="Company-Select"
      ></b-form-checkbox-group>
    </b-form-group>
    <b-button @click="getData()" variant="primary">Search</b-button>
    <line-chart ref="lineChart"></line-chart>
    <over-time-bar-chart ref="overTimeBarChart"></over-time-bar-chart>
  </div>
</template>

<script>
import LineChart from '@/components/Cards/LineChart'
import OverTimeBarChart from '@/components/Cards/OverTimeBarChart'
import DataSetting from '../../../../../backend/data_setting.json'

export default {
  created () {
    let keylist = []
    let optionCatcher = DataSetting['institutions'];
    for (let instituions in optionCatcher) {
      if (optionCatcher.hasOwnProperty(instituions)){
        keylist.push(instituions)
      }
    }
    let options = []
    for (let key in keylist) {
      if (keylist.hasOwnProperty(key)) {
        let option = {}
        option.text = optionCatcher[keylist[key]]['Nick']
        option.value = optionCatcher[keylist[key]]['Nick']
        options.push(option)
      }
    }
    this.options = options
  },
  name: 'overtime-charts',
  components: {LineChart,OverTimeBarChart},
  data: function () {
    return {
      selected: [],
      options: [],
      quarter1: '',
      quarter2: ''
    }
  },
  methods: {
    getData () {
      console.log(this.selected)
      this.$refs.lineChart.getData('Change In VaR Measure Overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.lineChart.getData('Market Risk-Weighted Assets Overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.lineChart.getData('sVaR-VaR Ratio Overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.lineChart.getData('Diversification Overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.overTimeBarChart.getData('Num of VaR Breach', this.quarter1, this.quarter2, this.selected)
    }
  }
}
</script>
