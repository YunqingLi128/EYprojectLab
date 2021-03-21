<template>
  <div>
    <b-container fluid>
      <b-row class="my-1">
        <b-col sm="2">
          <label for="input-quarter">Please input the quarter:</label>
        </b-col>
        <b-col sm="10">
          <b-form-input id="input-quarter" name="input-quarter"
                        v-model.trim="quarter" maxlength=100 size="sm" type="text"
                        placeholder="example: 2020Q3">
          </b-form-input>
        </b-col>
      </b-row>
    </b-container>
    <b-form>

      <b-button @click="getData()" variant="primary">Search</b-button>
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
