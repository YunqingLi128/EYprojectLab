<template>
  <div>
    <b-form inline>
      <b-form-group id="input-group" label="Please input the quarter:" label-for="input-quarter">
        <b-form-input id="input-quarter" name="input-quarter" v-model.trim="quarter"
                      style="margin-left:10px;" placeholder="example: 2020Q3" required>
        </b-form-input>
        <b-form-invalid-feedback :state="validationQ1">
          Your Input should be at the form format like 2020Q4
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationQ1">
          Your Input looks good.
        </b-form-valid-feedback>
      </b-form-group>
    </b-form>
    <b-form-group label="Select Company:">
        <b-form-checkbox-group
          id="checkbox-group-1"
          v-model="selected"
          :options="options"
          name="Company-Select"
        ></b-form-checkbox-group>
      <b-form-invalid-feedback :state="validationSelection">
        You need to select at least one company
      </b-form-invalid-feedback>
      <b-form-valid-feedback :state="validationSelection">
        Your Input looks good.
      </b-form-valid-feedback>
    </b-form-group>
    <b-button @click="getData()" variant="primary" :disabled="!validationQ1 || !validationSelection">Search</b-button>
    <bar-chart ref="barChart"></bar-chart>
    <stack-bar-chart ref="stackChart"></stack-bar-chart>
    <bar-line-charts ref="barLineChart"></bar-line-charts>
  </div>
</template>

<script>
import BarChart from '@/components/Cards/BarChart';
import StackBarChart from '@/components/Cards/StackBarChart';
import BarLineCharts from '@/components/Cards/BarPlusLineChart';
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

  computed: {
    validationQ1(){
      return /^[0-9]{4}[Qq][1-4]$/.test(this.quarter)
    },
    validationSelection(){
      return this.selected.length != 0
    }
  },
  name: 'quarter-charts',
  components: {BarChart, StackBarChart, BarLineCharts},
  data: function () {
    return {
      selected: [],
      options: [],
      quarter: ''
    };
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
};
</script>
