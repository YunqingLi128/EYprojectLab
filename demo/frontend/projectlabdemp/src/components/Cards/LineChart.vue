<template>
  <div class="lineChart">
    <b-card-group deck>
      <b-card class="line-chart-card" title="Change In VaR Measure Overtime">
        <div class="line-chart" id="change-in-VaR-measure-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Market Risk-Weighted Assets Overtime">
        <div class="line-chart" id="market-risk-weighted-assets-overtime"></div>
      </b-card>
    </b-card-group>
    <b-card-group deck>
      <b-card class="line-chart-card" title="sVaR-VaR Ratio Overtime">
        <div class="line-chart" id="sVaR-VaR-ratio-overtime"></div>
      </b-card>
      <b-card class="line-chart-card" title="Diversification Overtime">
        <div class="line-chart" id="diversification-overtime"></div>
      </b-card>
    </b-card-group>
  </div>
</template>

<script>
import myAPI from '../../api'
import helper from '../../helper'
import * as echarts from 'echarts'

export default {
  name: 'LineChart',
  created () {
    this.getQuarterList = helper.getQuarterList
  },
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
    getData (id, quarter1, quarter2, selected) {
      let that = this
      let endpointDict = {
        'change-in-VaR-measure-overtime': 'getChangeInVaRBasedMeasureOvertime',
        'market-risk-weighted-assets-overtime': 'getAdvancedMarketRiskWeightedAssets',
        'sVaR-VaR-ratio-overtime': 'getVaRsVaRRatioOvertime',
        'diversification-overtime': 'getDiversificationVarOvertime'
      }
      const start = quarter1
      const end = quarter2
      let xString = that.getQuarterList(start, end)
      myAPI
        .getDataOvertime(endpointDict[id], start, end)
        .then(function (response) {
          let data = response.data
          console.log(data)
          let companies = []
          let series = []
          for (let key of selected) {
            if (data.hasOwnProperty(key)) {
              companies.push(key)
              let chartItem = {}
              chartItem.name = key
              chartItem.type = 'line'
              chartItem.data = []
              for (const item of data[key]) {
                if (id === 'change-in-VaR-measure-overtime' || id === 'market-risk-weighted-assets-overtime') {
                  chartItem.data.push((item[1] / 1000).toFixed(2))
                } else {
                  chartItem.data.push(item[1].toFixed(2))
                }
              }
              series.push(chartItem)
            }
          }
          console.log(companies)
          console.log(series)
          let millionYAxis = [
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
          ]
          let yAxisMap = {
            'change-in-VaR-measure-overtime': millionYAxis,
            'market-risk-weighted-assets-overtime': millionYAxis,
            'sVaR-VaR-ratio-overtime': [
              {
                type: 'value',
                axisLabel: {
                  formatter: function (value) {
                    return value.toFixed(2) // show two decimals for ratio
                  }
                }
              }
            ],
            'diversification-overtime': [
              {
                type: 'value',
                axisLabel: {
                  formatter: '{value} %'
                }
              }
            ]
          }
          that.lineChartData.legend = companies
          that.lineChartData.xAxisData = xString
          that.lineChartData.yAxis = yAxisMap[id]
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
