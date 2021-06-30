<template>
  <div>
    <div class="FD_header_layout">
      <h3 class="FD_header">
        <span class="FD_header_span">Market Environment Analysis</span>
      </h3>
    </div>
    <b-form id="main-input" inline>
      <b-form-group inline id="input-group-1" label="Start Date:" label-for="input-date-1">
        <b-form-input id="input-date-1" name="input-date" v-model.trim="quarter1"
                      style="margin-left:10px;" placeholder="example: 2021-01-01" required>
        </b-form-input>
      </b-form-group>
      <b-form-group inline id="input-group-2" label="End Date: " label-for="input-date-2">
        <b-form-input id="input-date-2" name="input-date" v-model.trim="quarter2"
                      style="margin-left:10px;" placeholder="example: 2021-06-01" required>
        </b-form-input>
      </b-form-group>
      <b-button @click="getData()" variant="primary" :disabled="!validationDate">Search</b-button>
    </b-form>
    <b-form id="error-catcher">
      <b-form-group id="error-catcher-box" label="You may have following errors:">
        <b-form-invalid-feedback :state="validationQ1">
          Your start date should be at the form format like 2021-01-01
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationQ1">
          Your start date format looks good.
        </b-form-valid-feedback>
        <b-form-invalid-feedback :state="validationQ2">
          Your end date should be at the form format like 2021-01-01
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationQ2">
          Your end date format looks good.
        </b-form-valid-feedback>
        <b-form-invalid-feedback :state="validationDate">
          Your start date should be later than the end date
        </b-form-invalid-feedback>
        <b-form-valid-feedback :state="validationDate">
          Your date sequence input looks good.
        </b-form-valid-feedback>
      </b-form-group>
    </b-form>
    <market-env-line-chart ref="MarketEnvLineChart"></market-env-line-chart>
  </div>
</template>

<script>
import helper from '../../helper'
import MarketEnvLineChart from '../Cards/MarketEnvLineChart'

export default {
  computed: {
    validationQ1 () {
      return /^\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$/.test(this.quarter1)
    },
    validationQ2 () {
      return /^\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$/.test(this.quarter2)
    },
    validationDate () {
      return /^\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$/.test(this.quarter1) && /^\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$/.test(this.quarter2) && this.quarter1 < this.quarter2
    }
  },
  name: 'market-env-charts',
  components: {MarketEnvLineChart},
  data: function () {
    return {
      selected: [],
      options: [],
      quarter1: helper.getDefaultMarketEnvStartDate(),
      quarter2: helper.getDefaultMarketEnvEndDate()
    }
  },
  methods: {
    getData () {
      this.$refs.MarketEnvLineChart.getData('interest-rate-overtime', this.quarter1, this.quarter2)
      this.$refs.MarketEnvLineChart.getData('wti-overtime', this.quarter1, this.quarter2)
      this.$refs.MarketEnvLineChart.getData('credit-spread-overtime', this.quarter1, this.quarter2)
      this.$refs.MarketEnvLineChart.getData('equity-market-overtime', this.quarter1, this.quarter2)
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
