<template>
  <div>
    <b-form>
      <b-form-group id="input-group" label="Please input the quarter:" label-for="input-quarter">
        <b-form-input id="input-quarter" name="input-quarter" v-model.trim="quarter"
                      placeholder="example: 2020Q3" required>
        </b-form-input>
      </b-form-group>
      <b-button @click="getData()" variant="primary" style="margin-bottom: 25px">Search</b-button>
    </b-form>
    <bar-chart ref="barChart"></bar-chart>
    <stack-bar-chart ref="stackChart"></stack-bar-chart>
  </div>
</template>

<script>
import BarChart from '@/components/Cards/BarChart';
import StackBarChart from '@/components/Cards/StackBarChart';

export default {
  name: 'quarter-charts',
  components: {BarChart, StackBarChart},
  data: function () {
    return {
      quarter: ''
    };
  },
  methods: {
    getData () {
      this.$refs.barChart.getData('companyID-vs-VaR-SVaR', this.quarter)
      this.$refs.barChart.getData('company-trading-asset-comparison', this.quarter)
      this.$refs.stackChart.getData('standardized-market-risk-weighted-assets-breakdown-by-bank', this.quarter)
      this.$refs.stackChart.getData('VaR-by-asset-class-and-diversification-effect', this.quarter)
    }
  }
};
</script>
