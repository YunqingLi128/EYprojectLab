<template>
  <div>
    <button @click="getData();">GET DATA</button>
    <div id="market-risk-weighted-assets" :style="{width: '100%', height: '600px'}"></div>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';

export default {
  name: 'LineChart',
  data: function () {
    return {
      lineChartData: {}
    }
  },
  methods: {
    drawLineChart () {
      let that = this;
      let chartDom = document.getElementById('market-risk-weighted-assets');
      let myChart = echarts.init(chartDom)
      let option = {
        title: {
          text: 'Advanced market risk-weighted assets over time'
        },
        legend: {
          bottom: 0,
          data: that.lineChartData.legend
        },
        xAxis: {
          type: 'category',
          data: that.lineChartData.xAxisData
        },
        yAxis: {
          type: 'value'
        },
        tooltip: {
          trigger: 'axis'
        },
        series: that.lineChartData.series
      }
      myChart.setOption(option);
    },
    getData () {
      let that = this;
      that.chartData = {};
      // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
      const start = '2015Q3';
      const end = '2016Q3';
      const base = 'http://127.0.0.1:5000/getAdvancedMarketRiskWeightedAssets';
      axios
        .get(base, {
          params: {
            'start': start,
            'end': end
          }
        })
        .then(function (response) {
          let data = response.data
          let companies = []
          let series = []
          for (let key in data) {
            if (data.hasOwnProperty(key)) {
              companies.push(key)
              let chartItem = {}
              chartItem.name = key
              chartItem.type = 'line'
              chartItem.data = []
              for (const item of data[key]) {
                chartItem.data.push(item[1])
              }
              series.push(chartItem)
            }
          }
          console.log(companies)
          console.log(series)
          that.chartData.legend = companies
          that.lineChartData.xAxisData = ['2015Q3', '2015Q4', '2016Q1', '2016Q2', '2016Q3'] // TODO: write function
          that.lineChartData.series = series
          that.drawLineChart()
        });
    }
  }
}
</script>

<style scoped>

</style>
