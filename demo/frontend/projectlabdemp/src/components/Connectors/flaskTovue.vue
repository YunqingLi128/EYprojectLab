<template>
  <div>
    <b-form>
      <b-form-group id="input-group-1" label="Start Quarter: " label-for="input-quarter-1">
        <b-form-input id="input-quarter-1" name="input-quarter" v-model.trim="quarter1"
                      placeholder="example: 2016Q3" required>
        </b-form-input>
        <b-form-invalid-feedback :state="validationQ1">
          Your Input should be at the form format like 2020Q4
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationQ1">
          Your Input looks good.
        </b-form-valid-feedback>
      </b-form-group>
      <b-form-group id="input-group-2" label="End Quarter: " label-for="input-quarter-2">
        <b-form-input id="input-quarter-2" name="input-quarter" v-model.trim="quarter2"
                      placeholder="example: 2020Q3" required>
        </b-form-input>
        <b-form-invalid-feedback :state="validationQ2">
          Your Input should be at the form format like 2020Q4
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationQ2">
          Your Input looks good.
        </b-form-valid-feedback>
      </b-form-group>
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
      <b-form-invalid-feedback :state="validationDate">
        Your End Quarter should be later than the Start Quarter
      </b-form-invalid-feedback>
      <b-form-valid-feedback :state="validationDate">
        Your Quarter period input looks good.
      </b-form-valid-feedback>
      <b-button block @click="getData()" variant="primary" :disabled="!validationDate || !validationSelection">Search</b-button>
    </b-form>
    <line-chart ref="lineChart"></line-chart>
    <b-card-group deck>
      <over-time-bar-chart ref="overTimeBarChart"></over-time-bar-chart>
      <over-time-table ref="overTimeTable"></over-time-table>
    </b-card-group>
  </div>
</template>

<script>
import LineChart from '@/components/Cards/LineChart'
import OverTimeBarChart from '@/components/Cards/OverTimeBarChart'
import OverTimeTable from '@/components/Cards/OverTimeTable';
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
      return /^[0-9]{4}[Qq][1-4]$/.test(this.quarter1)
    },
    validationQ2(){
      return /^[0-9]{4}[Qq][1-4]$/.test(this.quarter2)
    },
    validationDate(){
      return /^[0-9]{4}[Qq][1-4]$/.test(this.quarter1) && /^[0-9]{4}[Qq][1-4]$/.test(this.quarter2) && this.quarter1 < this.quarter2
    },
    validationSelection(){
      console.log("1111111", this.selected.length)
      return this.selected.length != 0
    }
  },
  name: 'overtime-charts',
  components: {OverTimeTable, LineChart,OverTimeBarChart},
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
      this.$refs.lineChart.getData('change-in-VaR-measure-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.lineChart.getData('market-risk-weighted-assets-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.lineChart.getData('sVaR-VaR-ratio-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.lineChart.getData('diversification-overtime', this.quarter1, this.quarter2, this.selected)
      this.$refs.overTimeBarChart.getData('number-of-VaR-breach', this.quarter1, this.quarter2, this.selected)
      this.$refs.overTimeTable.getData('stress-window-table', this.quarter1, this.quarter2, this.selected)
    }
  }
}
</script>
