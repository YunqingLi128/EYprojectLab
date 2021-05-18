<template>
  <b-card class="over-time-bar-chart-card" title="Number of VaR Breach">
    <div class="over-time-bar-chart" id="number-of-VaR-breach"></div>
  </b-card>
</template>

<script>
import myAPI from '../../api'
import helper from '../../helper'
import * as echarts from 'echarts'

export default {
  name: 'OverTimeBarChart',
  created () {
    this.getQuarterList = helper.getQuarterList
  },
  data: function () {
    return {
      barChartData: {}
    }
  },
  methods: {
    drawOverTimeBarChart (id) {
      let that = this
      let chartDom = document.getElementById(id)
      let myChart = echarts.getInstanceByDom(chartDom)
      if (myChart == null) {
        myChart = echarts.init(chartDom)
      }
      let option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: that.barChartData.legendData,
          y: 'bottom'
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
        yAxis: [
          {
            type: 'category',
            axisTick: {show: false},
            data: that.barChartData.xAxisData
          }
        ],
        xAxis: [
          {
            type: 'value'
          }
        ],
        series: that.barChartData.series
      }
      myChart.setOption(option, true)
    },
    getData (id, quarter1, quarter2, selected) {
      let that = this
      that.chartData = {}
      let endpointDict = {
        'number-of-VaR-breach': 'getVaRBreachOvertime'
      }
      const start = quarter1
      const end = quarter2
      let xString = that.getQuarterList(quarter1, quarter2)
      myAPI
        .getDataOvertime(endpointDict[id], start, end)
        .then(function (response) {
          let data = response.data
          let companies = []
          let series = []
          for (let key of selected) {
            if (data.hasOwnProperty(key)) {
              companies.push(key)
              let chartItem = {}
              chartItem.name = key
              chartItem.type = 'bar'
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
          that.barChartData.xAxisData = xString
          that.barChartData.series = series
          that.drawOverTimeBarChart(id)
        })
    }
  }
}

</script>

<style scoped>

.over-time-bar-chart-card {
  max-width: 80rem;
  max-height: 40rem;
  margin-bottom: 20px;
}

.over-time-bar-chart {
  width: 100%;
  height: 35rem;
  display: inline-block;
}

</style>
