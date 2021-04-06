<template>
  <div>
    <div class="QH_header_layout">
      <h3 class="QH_header">
        <span class="QH_header_span">Quarterly Highlights</span>
      </h3>
    </div>
    <b-form id="main-input" inline>
      <b-form-group inline id="input-group" label="Please input the quarter:" label-for="input-quarter">
        <b-form-input id="input-quarter" name="input-quarter" v-model.trim="quarter"
                      style="margin-left:10px;" placeholder="example: 2020Q3" required>
        </b-form-input>
      </b-form-group>
      <b-form-group inline id="select-group" label="Select Company:">
      </b-form-group>
      <b-form-checkbox-group
            id="checkbox-group-1"
            v-model="selected"
            :options="options"
            name="Company-Select"
      ></b-form-checkbox-group>
      <b-button @click="getData()" variant="primary" :disabled="!validationQ1 || !validationSelection">Search</b-button>
    </b-form>
    <b-form id="error-catcher">
      <b-form-group id="error-catcher-box" label="You may have following errors:">
        <b-form-invalid-feedback :state="validationQ1">
            Your input should be at the form format like 2020Q4
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationQ1">
          Your input quarter format looks good.
        </b-form-valid-feedback>
        <b-form-invalid-feedback :state="validationSelection">
        You need to select at least one company
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationSelection">
          Your selection of companies looks good.
        </b-form-valid-feedback>
      </b-form-group>
    </b-form>
    <bar-chart ref="barChart"></bar-chart>
    <stack-bar-chart ref="stackChart"></stack-bar-chart>
    <bar-line-charts ref="barLineChart"></bar-line-charts>
  </div>
</template>

<script>
import BarChart from '@/components/Cards/BarChart'
import StackBarChart from '@/components/Cards/StackBarChart'
import BarLineCharts from '@/components/Cards/BarPlusLineChart'
import DataSetting from '../../../../../backend/data_setting.json'
import helper from '../../helper'

export default {
  created () {
    let keyList = []
    let optionCatcher = DataSetting['institutions']
    for (let institution in optionCatcher) {
      if (optionCatcher.hasOwnProperty(institution)) {
        keyList.push(institution)
      }
    }
    let options = []
    for (let key in keyList) {
      if (keyList.hasOwnProperty(key)) {
        let option = {}
        option.text = optionCatcher[keyList[key]]['Nick']
        option.value = optionCatcher[keyList[key]]['Nick']
        options.push(option)
        this.selected.push(option.value)
      }
    }
    this.options = options
  },

  computed: {
    validationQ1 () {
      return /^[0-9]{4}[Qq][1-4]$/.test(this.quarter)
    },
    validationSelection () {
      return this.selected.length !== 0
    }
  },
  name: 'quarter-charts',
  components: {BarChart, StackBarChart, BarLineCharts},
  data: function () {
    return {
      selected: [],
      options: [],
      quarter: helper.getLatestQuarter()
    }
  },
  methods: {
    getData () {
      this.$refs.barChart.getData('VaR-SVaR-comparison', this.quarter, this.selected)
      this.$refs.barChart.getData('trading-asset-comparison', this.quarter, this.selected)
      this.$refs.barChart.getAggData('trading-asset-to-risk-ratio', this.quarter, this.selected)
      this.$refs.barChart.getAggData('trading-revenue-to-VaR-ratio', this.quarter, this.selected)
      this.$refs.stackChart.getData('standardized-market-risk-weighted-assets-breakdown-by-bank', this.quarter, this.selected)
      this.$refs.stackChart.getData('VaR-by-asset-class-and-diversification-effect', this.quarter, this.selected)
      this.$refs.barLineChart.getData('trading-asset', this.quarter, this.selected)
      this.$refs.barLineChart.getData('trading-liabilities', this.quarter, this.selected)
      this.$refs.barLineChart.getData('net-trading-asset', this.quarter, this.selected)
      this.$refs.barLineChart.getData('gross-trading-asset', this.quarter, this.selected)
    }
  }
}
</script>

<style scoped>
#input-group {
  margin: 5px;
}
#input-quarter{
  margin: 10px;
  width: 200px;
}

#select-group {
  margin: 5px;
}
#checkbox-group-1{
  margin: 10px;
}

#error-catcher {
  margin: 5px;
}
.QH_header_span{
  font-family: 'Poppins', sans-serif;
  font-weight: bold;
  color: #323030;
}
.QH_header{
  margin-bottom: 10px;
}
.QH_header_layout{
  border-bottom: 1px solid;
  border-bottom-color: #CACACA;
  margin-bottom: 15px;
  margin-top: 5px;
  box-sizing: border-box;
}

</style>
