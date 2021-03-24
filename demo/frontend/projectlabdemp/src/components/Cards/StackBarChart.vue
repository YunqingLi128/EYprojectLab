<template>
  <div class="StackBarChart">
    <b-card-group deck>
    <b-card
      title="Standardized Market Risk-Weighted Assets Breakdown By Bank"
      style="max-width: 60rem; max-height: 40rem;"
    >
    <div id='standardized-market-risk-weighted-assets-breakdown-by-bank' style="width: 100%; height: 35rem; display: inline-block;"></div>
    </b-card>
    <b-card
      title="VaR by Asset Class and Diversification Effect"
      style="max-width: 60rem; max-height: 40rem;"
    >
    <div id='VaR-by-asset-class-and-diversification-effect' style="width: 100%; height: 35rem; display: inline-block;"></div>
    </b-card>
    </b-card-group>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';

export default {
  name: 'StackBarChart',
  data: function () {
    return {
      barChartData: {}
    }
  },
  methods: {
    drawStackBarChart (id) {
      let that = this;
      let chartDom = document.getElementById(id);
      let myChart = echarts.init(chartDom);
      let option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          top: 'bottom',
          data: that.barChartData.legend
        },
        toolbox: {
          show: true,
          orient: 'vertical',
          left: 'right',
          top: 'center',
          feature: {
            mark: {show: true},
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        xAxis: [
          {
            type: 'category',
            axisTick: {show: false},
            data: that.barChartData.xAxisData
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: that.barChartData.series
      }
      myChart.setOption(option);
    },
    getData (id, quarter, selected) {
      let that = this;
      that.chartData = {};
      let dictBase = {
        'standardized-market-risk-weighted-assets-breakdown-by-bank': 'getStandardizedRiskWeightedAssets',
        'VaR-by-asset-class-and-diversification-effect': 'getVaRByAssetClassDiversification'
      };
      const start = quarter;
      const end = quarter;
      const base = 'http://127.0.0.1:5000/' + dictBase[id];
      axios
        .get(base, {
          params: {
            'start': start,
            'end': end
          },
          withCredentials: true,
          headers: {
            'secret-key': 'super secret key',
            'Access-Control-Allow-Origin': '*'
          }
        })
        .then(function (response) {
          let data = response.data
          let companies = []
          let series = []
          let flag = 0
          for (let key in data) {
            if (data.hasOwnProperty(key)) {
              let chartItem = {}
              chartItem.name = key
              chartItem.type = 'bar'
              chartItem.data = []
              chartItem.stack = 'total'
              chartItem.label = {show: true}
              chartItem.emphasis = {focus: 'series'}
              if (flag === 0) {
                for (const item of data[key]) {
                  if (selected.includes(item[0])) {
                    companies.push(item[0])
                  }
                }
                flag = 1
              }
              for (const item of data[key]) {
                if (selected.includes(item[0])) {
                  chartItem.data.push(Math.round(item[1]))
                }
              }
              series.push(chartItem)
            }
          }
          console.log(companies)
          console.log(series)
          that.barChartData.xAxisData = companies // TODO: write function
          that.barChartData.series = series
          that.drawStackBarChart(id)
        });
    }
  }
}

</script>

<style scoped>

</style>
