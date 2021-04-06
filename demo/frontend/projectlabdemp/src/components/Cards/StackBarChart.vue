<template>
  <div class="stack-bar-charts">
    <b-card-group deck>
      <b-card class="stack-bar-chart-card" title="Standardized Market Risk-Weighted Assets Breakdown By Bank">
        <div class="stack-bar-chart" id="standardized-market-risk-weighted-assets-breakdown-by-bank"></div>
      </b-card>
      <b-card class="stack-bar-chart-card" title="VaR by Asset Class and Diversification Effect">
        <div class="stack-bar-chart" id="VaR-by-asset-class-and-diversification-effect"></div>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import myAPI from '../../api'
import * as echarts from 'echarts'

export default {
  name: 'StackBarChart',
  data: function () {
    return {
      barChartData: {}
    }
  },
  methods: {
    drawStackBarChart (id) {
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
        yAxis: that.barChartData.yAxis,
        series: that.barChartData.series
      }
      myChart.setOption(option, true)
    },
    getData (id, quarter, selected) {
      let that = this
      that.chartData = {}
      let endpointDict = {
        'standardized-market-risk-weighted-assets-breakdown-by-bank': 'getStandardizedRiskWeightedAssets',
        'VaR-by-asset-class-and-diversification-effect': 'getVaRByAssetClassDiversification'
      }
      myAPI
        .getDataByQuarter(endpointDict[id], quarter)
        .then(function (response) {
          let data = response.data
          let companies = []
          let series = []
          for (let key in data) {
            if (data.hasOwnProperty(key)) {
              let chartItem = {}
              chartItem.name = key
              chartItem.type = 'bar'
              chartItem.data = []
              chartItem.stack = 'total'
              chartItem.label = {show: true}
              chartItem.emphasis = {focus: 'series'}
              for (let selectComp of selected) {
                let flag = 0
                for (const item of data[key]) {
                  if (selectComp === item[0]) {
                    if (id === 'standardized-market-risk-weighted-assets-breakdown-by-bank') {
                      chartItem.data.push(Math.round(item[1] * 12.5 / 1000))
                    } else {
                      chartItem.data.push(Math.round(item[1]))
                    }
                    companies.push(item[0])
                    flag = 1
                  }
                }
                if (flag === 0) {
                  chartItem.data.push(0)
                }
              }
              series.push(chartItem)
            }
          }
          console.log(companies)
          console.log(series)
          let yAxisMap = {
            'standardized-market-risk-weighted-assets-breakdown-by-bank': [
              {
                type: 'value',
                name: 'Millions',
                axisLabel: {
                  formatter: function (value) {
                    // Original Amount: Dollar Amounts in Thousands
                    // show tick with comma
                    return (value).toLocaleString()
                  }
                }
              }
            ],
            'VaR-by-asset-class-and-diversification-effect': [
              {
                type: 'value',
                axisLabel: {
                  formatter: '{value} %'
                }
              }
            ]
          }
          that.barChartData.xAxisData = selected
          that.barChartData.yAxis = yAxisMap[id]
          that.barChartData.series = series
          that.drawStackBarChart(id)
        })
    }
  }
}

</script>

<style scoped>

.stack-bar-chart-card {
  max-width: 80rem;
  max-height: 40rem;
  margin-bottom: 20px;
}

.stack-bar-chart {
  width: 100%;
  height: 35rem;
  display: inline-block;
}

</style>
