<template>
  <div class="myDiv">
    <button @click="getData();getData_2();getData_3();">GET DATA</button>
    <div id="change-in-var-measure-overtime" :style="{width: '50%', height: '600px'}"></div>
    <div id="market-risk-weighted-assets" :style="{width: '50%', height: '600px'}"></div>
    <div id="svar-var-ratio-overtime" :style="{width: '50%', height: '600px'}"></div>
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
      let chartDom = document.getElementById('change-in-var-measure-overtime');
      let myChart = echarts.init(chartDom)
      let option = {
        title: {
          text: 'Change in VaR-based Measure Over Time'
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
    drawLineChart2 () {
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
    drawLineChart3 () {
      let that = this;
      let chartDom = document.getElementById('svar-var-ratio-overtime');
      let myChart = echarts.init(chartDom)
      let option = {
        title: {
          text: 'sVaR to VaR Ratio Over Time'
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
      const base = 'http://127.0.0.1:5000/getChangeInVaRBasedMeasureOvertime';
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
    },
    getData_2 () {
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
          that.drawLineChart2()
        });
    },
    getData_3 () {
      let that = this;
      that.chartData = {};
      // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address
      const start = '2015Q3';
      const end = '2016Q3';
      const base = 'http://127.0.0.1:5000/getVaRsVaRRatioOvertime';
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
          that.drawLineChart3()
        });
    }
  }
}
</script>

<style scoped>

</style>

