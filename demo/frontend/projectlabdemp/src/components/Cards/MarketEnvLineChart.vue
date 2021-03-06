<template>
  <div class="lineChart">
    <b-card-group deck>
      <b-card class="line-chart-card" title="Interest Rate">
        <div class="line-chart" id="interest-rate-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="WTI">
        <div class="line-chart" id="wti-overtime"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="line-chart-card" title="Credit Spread">
        <div class="line-chart" id="credit-spread-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Equities Market">
        <div class="line-chart" id="equity-market-overtime"></div>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import myAPI from '../../api'
import * as echarts from 'echarts'

export default {
  name: 'MarketEnvLineChart',
  data: function () {
    return {
      lineChartData: {}
    }
  },
  methods: {
    drawLineChart (id) {
      let that = this
      let chartDom = document.getElementById(id)
      let myChart = echarts.getInstanceByDom(chartDom)
      if (myChart == null) {
        myChart = echarts.init(chartDom)
      }
      let option = {
        legend: {
          bottom: 0,
          data: that.lineChartData.legend
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
        xAxis: {
          type: 'category',
          data: that.lineChartData.xAxisData
        },
        yAxis: that.lineChartData.yAxis,
        tooltip: {
          trigger: 'axis'
        },
        series: that.lineChartData.series
      }
      myChart.setOption(option, true)
    },
    getData (id, stdate, eddate) {
      let that = this
      let endpointDict = {
        'interest-rate-overtime': 'getInterestRateOvertime',
        'wti-overtime': 'getWTIOvertime',
        'credit-spread-overtime': 'getCreditSpreadOvertime',
        'equity-market-overtime': 'getEquityMarketOvertime'
      }
      myAPI
        .getDataOvertime(endpointDict[id], stdate, eddate)
        .then(function (response) {
          let data = response.data
          console.log(data)
          let xString = []
          let item = []
          let series = []
          if (id !== 'equity-market-overtime') {
            for (const [key, value] of Object.entries(data)) {
              if (data.hasOwnProperty(key)) {
                if (key === 'Date') {
                  xString = value
                } else {
                  let chartItem = {}
                  item.push(key)
                  chartItem.name = key
                  chartItem.type = 'line'
                  chartItem.data = value
                  series.push(chartItem)
                }
              }
            }
          } else {
            for (const [key, value] of Object.entries(data)) {
              if (data.hasOwnProperty(key)) {
                if (key === 'Date') {
                  xString = value
                } else if (key === 'S&P 500') {
                  let chartItemOne = {}
                  item.push(key)
                  chartItemOne.name = key
                  chartItemOne.type = 'line'
                  chartItemOne.data = value
                  series.push(chartItemOne)
                } else if (key === 'VIX') {
                  let chartItemTwo = {}
                  item.push(key)
                  chartItemTwo.name = key
                  chartItemTwo.type = 'line'
                  chartItemTwo.data = value
                  chartItemTwo.yAxisIndex = 1
                  series.push(chartItemTwo)
                }
              }
            }
          }
          console.log(series)
          let rateYAxis = [
            {
              type: 'value',
              name: 'rate',
              axisLabel: {
                formatter: function (value) {
                  // Original Amount: Dollar Amounts in Thousands
                  // show tick with comma
                  return (value).toLocaleString()
                }
              }
            }
          ]
          let rateYAxisOne =
            {
              type: 'value',
              name: 'point',
              axisLabel: {
                formatter: function (value) {
                  // Original Amount: Dollar Amounts in Thousands
                  // show tick with comma
                  return (value).toLocaleString()
                }
              },
              max: 4000,
              min: 3000
            }
          let rateYAxisTwo =
            {
              type: 'value',
              name: 'rate',
              axisLabel: {
                formatter: function (value) {
                  // Original Amount: Dollar Amounts in Thousands
                  // show tick with comma
                  return (value).toLocaleString()
                }
              },
              max: 50,
              min: 0
            }
          let yAxisMap = {
            'interest-rate-overtime': rateYAxis,
            'wti-overtime': rateYAxis,
            'credit-spread-overtime': rateYAxis
          }
          that.lineChartData.legend = item
          that.lineChartData.xAxisData = xString
          if (id !== 'equity-market-overtime') {
            that.lineChartData.yAxis = yAxisMap[id]
          } else {
            that.lineChartData.yAxis = [rateYAxisOne, rateYAxisTwo]
          }
          that.lineChartData.series = series
          that.drawLineChart(id)
        })
    }
  }
}
</script>

<style scoped> /* Styles are scoped to this component only.*/
/* Style for Desktop/Tablet  */
.search-parent {
  display: flex;
  flex-flow: row wrap;
  justify-content: space-between;
  background-color: lightgray;
}
.card-inner {
  position: relative;
  overflow: hidden;
  box-shadow: 2px 2px 8px grey;
}
.card-img {
  width: 100%;
}
.card-bottom {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 30px;
  width: 100%;
  background-color: white;
  opacity: 0.7;
  display: flex;
  justify-content: space-between;
}
.card-hover {
  position: absolute;
  right: 15px;
  left: 15px;
  top: 15px;
  bottom: 15px;
  background-color: white;
  opacity: 0.7;
  display: flex;
  flex-flow: column wrap;
  justify-content: center;
  align-items: center;
}
.absolute-star {
  position: absolute;
  top: 10px;
  right: 10px;
}
.card-hover p {
  font-size: 10px;
  text-align: center;
}
.bold {
  font-weight: 500;
}
.rating-div {
  width: 200px;
}
.search-bar {
  position: relative;
}
.search-bar input {
  padding-left: 30px;
}
.search-icon {
  position: absolute;
  top: 8px;
  left: 8px;
}
/* For Mobile Device, we will be going with column wrap approach */
@media screen and (max-width: 550px) {
  .search-parent {
    display: flex;
    flex-flow: column wrap;
    justify-content: center;
    align-items: center;
    background-color: lightgray;
  }
.search-parent div {
    width: 100%;
    text-align: center;
  }
}

.line-chart-card {
  max-width: 80rem;
  max-height: 40rem;
  margin-bottom: 20px;
}

.line-chart {
  width: 100%;
  height: 35rem;
  display: inline-block;
}

</style>
