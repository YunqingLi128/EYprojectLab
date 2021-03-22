<template>
  <div>
    <b-form>
      <b-form-group id="input-group-1" label="Please input the start quarter:" label-for="input-quarter-1">
        <b-form-input id="input-quarter-1" name="input-quarter" v-model.trim="quarter1"
                      placeholder="example: 2016Q3" required>
        </b-form-input>
      </b-form-group>
      <b-form-group id="input-group-2" label="Please input the end quarter:" label-for="input-quarter-2">
        <b-form-input id="input-quarter-2" name="input-quarter" v-model.trim="quarter2"
                      placeholder="example: 2020Q3" required>
        </b-form-input>
      </b-form-group>
      <b-button @click="getData()" variant="primary" style="margin-bottom: 25px">Search</b-button>
    </b-form>
    <line-chart ref="lineChart"></line-chart>
    <over-time-bar-chart ref="overTimeBarChart"></over-time-bar-chart>
  </div>
</template>

<script>
import LineChart from '@/components/Cards/LineChart'
import OverTimeBarChart from '@/components/Cards/OverTimeBarChart'

export default {
  name: 'overtime-charts',
  components: {LineChart,OverTimeBarChart},
  data: function () {
    return {
      quarter1: '',
      quarter2: ''
    }
  },
  methods: {
    getData () {
      this.$refs.lineChart.getData('Change In VaR Measure Overtime', this.quarter1, this.quarter2)
      this.$refs.lineChart.getData('Market Risk-Weighted Assets Overtime', this.quarter1, this.quarter2)
      this.$refs.lineChart.getData('sVaR-VaR Ratio Overtime', this.quarter1, this.quarter2)
      this.$refs.lineChart.getData('Diversification Overtime', this.quarter1, this.quarter2)
      this.$refs.overTimeBarChart.getData('Num of VaR Breach', this.quarter1, this.quarter2)
    }
  }
}
</script>
