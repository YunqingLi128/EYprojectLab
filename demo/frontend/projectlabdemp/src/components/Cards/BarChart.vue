<template>
  <div class="bar-charts">
    <b-card-group deck>
      <b-card class="bar-chart-card" title="VaR and SVaR Comparison">
        <div class="bar-chart" id="VaR-SVaR-comparison"></div>
      </b-card>
      <b-card class="bar-chart-card" title="Trading Asset Comparison">
        <div class="bar-chart" id="trading-asset-comparison"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="bar-chart-card" title="Trading Asset to Risk Ratio">
        <div class="bar-chart" id="trading-asset-to-risk-ratio"></div>
      </b-card>
      <b-card class="bar-chart-card" title="Trading Revenue to VaR Ratio">
        <div class="bar-chart" id="trading-revenue-to-VaR-ratio"></div>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import myAPI from '../../api'
import * as echarts from 'echarts'

export default {
  name: 'BarChart_Comparison',
  data: function () {
    return {
      quarter: '',
      barChartData: {}
    }
  },
  methods: {
    DrawBarChart (id) {
      let that = this
      let chartDom = document.getElementById(id)
      let myChart = echarts.getInstanceByDom(chartDom)
      if (myChart == null) {
        myChart = echarts.init(chartDom)
      }
      let option = {
        title: {
          show: false
        },
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
        xAxis: [
          {
            type: 'category',
            axisTick: {show: false},
            data: that.barChartData.xAxisData
          }
        ],
        yAxis: that.barChartData.yAxis,
        series: that.barChartData.series
      }
      myChart.setOption(option, true)
    },
    getData (id, quarter, selected) {
      let that = this
      that.chartData = {}
      let endpointDict = {
        'VaR-SVaR-comparison': 'getVaRsVarRComparison',
        'trading-asset-comparison': 'getTradingAssetComparison'
      }
      myAPI
        .getDataByQuarter(endpointDict[id], quarter)
        .then(function (response) {
          let data = response.data
          let companies = []
          let groups = {}
          for (let key of selected) {
            if (data.hasOwnProperty(key)) {
              companies.push(key)
              for (let itemName in data[key]) {
                if (data[key].hasOwnProperty(itemName)) {
                  if (groups.hasOwnProperty(itemName)) {
                    groups[itemName].push(data[key][itemName])
                  } else {
                    groups[itemName] = [data[key][itemName]]
                  }
                }
              }
            }
          }
          let series = []
          let legendList = []
          for (let key in groups) {
            let chartItem = {}
            chartItem.name = key
            chartItem.type = 'bar'
            chartItem.data = groups[key]
            series.push(chartItem)
            legendList.push(key)
          }
          console.log(companies)
          console.log(series)
          that.barChartData.legendData = legendList
          that.barChartData.xAxisData = companies
          that.barChartData.yAxis = [
            {
              type: 'value',
              name: 'Millions',
              axisLabel: {
                formatter: function (value) {
                  // Original Amount: Dollar Amounts in Thousands
                  // show tick with comma
                  return (value / 1000).toLocaleString()
                }
              }
            }
          ]
          that.barChartData.series = series
          that.DrawBarChart(id)
        })
    },
    getAggData (id, quarter, selected) {
      let that = this
      let endpointDict = {
        'trading-asset-to-risk-ratio': 'getTradingAssetToRiskRatio',
        'trading-revenue-to-VaR-ratio': 'getTradingRevenueToVarRatio'
      }
      myAPI
        .getDataByQuarter(endpointDict[id], quarter)
        .then(function (response) {
          let data = response.data
          let itemNames = []
          let itemSet = new Set()
          let series = []
          let legendList = []
          for (let key of selected) {
            if (data.hasOwnProperty(key)) {
              legendList.push(key)
              let chartItem = {}
              chartItem.name = key
              chartItem.type = 'bar'
              chartItem.data = []
              for (let itemName in data[key]) {
                if (data[key].hasOwnProperty(itemName)) {
                  chartItem.data.push(data[key][itemName])
                  if (!itemSet.has(itemName)) {
                    itemSet.add(itemName)
                    itemNames.push(itemName)
                  }
                }
              }
              series.push(chartItem)
            }
          }
          console.log(itemNames)
          console.log(series)
          that.barChartData.legendData = legendList
          that.barChartData.xAxisData = itemNames
          that.barChartData.yAxis = [
            {
              type: 'value',
              axisLabel: {
                formatter: function (value) {
                  return value.toFixed(2) // show two decimals for ratio
                }
              }
            }
          ]
          that.barChartData.series = series
          that.DrawBarChart(id)
        })
    }
  }
}
</script>

<style scoped>

figure {
  display: inline-block;
  position: relative;
  margin: 2em auto;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  box-shadow: 0 0 45px rgba(0, 0, 0, 0.2);
  padding: 1.5em 2em;
  min-width: calc(40vw + 4em);
}

.echarts {
  width: 40vw;
  min-width: 400px;
  height: 400px;
}

.chart {
  height: 400px;
}

.bar-chart-card {
  max-width: 80rem;
  max-height: 40rem;
  margin-bottom: 20px;
}

.bar-chart {
  width: 100%;
  height: 35rem;
  display: inline-block;
}

</style>
