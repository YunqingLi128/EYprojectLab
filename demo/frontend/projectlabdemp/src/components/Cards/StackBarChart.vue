<template>
  <div class="StackBarChart">
    <button @click="get_Data ('Standardized Market Risk-Weighted Assets Breakdown By Bank'); get_Data ('VaR by Asset Class and Diversification Effect');">GET STACK BAR</button>
    <b-card-group deck>
    <b-card
      title="Standardized Market Risk-Weighted Assets Breakdown By Bank"
      style="max-width: 60rem; max-height: 40rem;"
    >
    <div id='Standardized Market Risk-Weighted Assets Breakdown By Bank' style="width: 100%; height: 35rem; display: inline-block;"></div>
    </b-card>
    <b-card
      title="VaR by Asset Class and Diversification Effect"
      style="max-width: 60rem; max-height: 40rem;"
    >
    <div id='VaR by Asset Class and Diversification Effect' style="width: 100%; height: 35rem; display: inline-block;"></div>
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
        series: [
          {
            name: that.barChartData.series[0].name,
            type: that.barChartData.series[0].type,
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[0].data
          },
          {
            name: that.barChartData.series[1].name,
            type: that.barChartData.series[1].type,
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[1].data
          },
          {
            name: that.barChartData.series[2].name,
            type: that.barChartData.series[2].type,
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[2].data
          },
          {
            name: that.barChartData.series[3].name,
            type: that.barChartData.series[3].type,
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[3].data
          },
          {
            name: that.barChartData.series[4].name,
            type: that.barChartData.series[4].type,
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[4].data
          },
          {
            name: that.barChartData.series[5].name,
            type: that.barChartData.series[5].type,
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[5].data
          }
        ]
      }
      myChart.setOption(option);
    },
    get_Data (id) {
      let that = this;
      that.chartData = {};
      let dictBase = {
        'Standardized Market Risk-Weighted Assets Breakdown By Bank': 'getStandardizedRiskWeightedAssets',
        'VaR by Asset Class and Diversification Effect': 'getVaRByAssetClassDiversification'
      };
      let compDict = {
        '1073757': 'BAC',
        '1951350': 'CITI',
        '2380443': 'GS',
        '1039502': 'JPMC',
        '2162966': 'MS',
        '1120754': 'WF'
      };
      const start = '2020Q3';
      const end = '2020Q3';
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
          console.log(data)
          let companies = []
          let series = []
          let flag = 0
          for (let key in data) {
            if (data.hasOwnProperty(key)) {
              let chartItem = {}
              chartItem.name = key
              chartItem.type = 'bar'
              chartItem.data = []
              if (flag === 0) {
                for (const item of data[key]) {
                  companies.push(compDict[item[0]])
                }
                flag = 1
              }
              for (const item of data[key]) {
                chartItem.data.push(Math.round(item[1]))
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
