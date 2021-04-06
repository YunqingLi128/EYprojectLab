<template>
  <div class="bar-line-charts">
    <b-card-group deck>
      <b-card class="bar-line-chart-card" title="Trading Asset">
        <div class="bar-line-chart" id="trading-asset"></div>
      </b-card>
      <b-card class="bar-line-chart-card" title="Trading Liabilities">
        <div class="bar-line-chart" id="trading-liabilities"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="bar-line-chart-card" title="Net Trading Asset">
        <div class="bar-line-chart" id="net-trading-asset"></div>
      </b-card>
      <b-card class="bar-line-chart-card" title="Gross Trading Asset">
        <div class="bar-line-chart" id="gross-trading-asset"></div>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import myAPI from '../../api'
import * as echarts from 'echarts'

export default {
  name: 'BarLineCharts',
  data: function () {
    return {
      barLineChartsData: {}
    }
  },
  methods: {
    DrawBarLineChart (id) {
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
          data: that.barLineChartsData.legendData,
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
        grid: {show: false},
        xAxis: [
          {
            type: 'category',
            axisTick: {show: false},
            data: that.barLineChartsData.xAxisData
          }
        ],
        yAxis: that.barLineChartsData.yAxisData,
        series: that.barLineChartsData.series
      }
      myChart.setOption(option, true)
    },
    getData (id, quarter, selected) {
      let that = this
      let endpointDict = {
        'trading-asset': 'getTradingAssetsAndChangeByQuarter',
        'trading-liabilities': 'getTradingLiabilitiesAndChangeByQuarter',
        'net-trading-asset': 'getNetTradingAssetAndPercentChange',
        'gross-trading-asset': 'getGrossTradingAssetAndPercentChange'
      }
      let legendBase = {
        'trading-asset': ['Trading Asset', 'Trading Asset Change from Last Quarter'],
        'trading-liabilities': ['Trading Liability', 'Trading Liability Change from Last Quarter'],
        'net-trading-asset': ['Net Trading Asset', 'Net Trading Asset Change from Last Quarter'],
        'gross-trading-asset': ['Gross Trading Asset', 'Gross Trading Asset Change from Last Quarter']
      }
      myAPI
        .getDataByQuarter(endpointDict[id], quarter)
        .then(function (response) {
          let data = response.data
          let companies = []
          let groupOne = []
          let groupTwo = []
          for (let key of selected) {
            if (data.hasOwnProperty(key)) {
              companies.push(key)
              groupOne.push(data[key][0][0] / 1000)
              groupTwo.push(data[key][0][1])
            }
          }
          let series = []
          let legendList = []
          let chartItemOne = {}
          let chartItemTwo = {}
          let yAxisOne = {}
          let yAxisTwo = {}
          let yAxis = []

          chartItemOne.name = legendBase[id][0]
          chartItemOne.type = 'bar'
          chartItemOne.data = groupOne

          chartItemTwo.name = legendBase[id][1]
          chartItemTwo.type = 'line'
          chartItemTwo.data = groupTwo
          chartItemTwo.yAxisIndex = 1

          yAxisOne.name = 'Millions'
          yAxisOne.scale = true
          yAxisOne.type = 'value'
          // yAxisOne.max = Math.max.apply(Math, groupOne) + 50000000;
          let curMax = Math.max.apply(Math, groupOne).toString()
          let highestDigit = parseInt(curMax[0])
          yAxisOne.max = (highestDigit + 1) * (10 ** (curMax.length - 1))
          yAxisOne.min = 0
          yAxisOne.splitLine = {
            show: false
          }
          yAxisOne.axisLabel = {
            formatter: function (value) {
              // Original Amount: Dollar Amounts in Thousands
              // show tick with comma
              return (value).toLocaleString()
            }
          }

          yAxisTwo.name = 'Percentage'
          yAxisTwo.scale = true
          yAxisTwo.type = 'value'
          // yAxisTwo.max = Math.round(Math.max.apply(Math,groupTwo) + 20);
          // yAxisTwo.min = Math.round(Math.min.apply(Math,groupTwo) - 20);
          curMax = Math.ceil(Math.max.apply(Math, groupTwo))
          highestDigit = parseInt(curMax / 10)
          let curMin = Math.floor(Math.min.apply(Math, groupTwo))
          let minValue = -10
          while (minValue > curMin) {
            minValue -= 10
          }
          yAxisTwo.max = (highestDigit + 1) * 10 + 20
          yAxisTwo.min = minValue - 20
          yAxisTwo.splitLine = {
            show: false
          }
          yAxisTwo.axisLabel = {
            formatter: '{value} %'
          }

          series = [chartItemOne, chartItemTwo]
          legendList = legendBase[id]
          yAxis = [yAxisOne, yAxisTwo]
          console.log(companies)
          console.log(series)
          that.barLineChartsData.legendData = legendList
          that.barLineChartsData.xAxisData = companies
          that.barLineChartsData.yAxisData = yAxis
          that.barLineChartsData.series = series
          that.DrawBarLineChart(id)
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

.bar-line-chart-card {
  max-width: 80rem;
  max-height: 40rem;
  margin-bottom: 20px;
}

.bar-line-chart {
  width: 100%;
  height: 35rem;
  display: inline-block;
}

</style>
