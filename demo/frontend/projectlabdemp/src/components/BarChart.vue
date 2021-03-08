<template>
  <div class="barChart">
    <button @click="get_Data('Company ID VS VaR and SVaR');get_Data('Company Trading Asset Comparison');">GET COMPARISON</button>
    <div id='Company ID VS VaR and SVaR' :style="{width: '50%', height: '600px'}"></div>
    <div id='Company Trading Asset Comparison' :style="{width: '50%', height: '600px'}"></div>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';

export default {
  name: 'BarChart_Comparison',
  data: function() {
    return {
      barChartData: {}
    }
  },
  methods: {
    DrawBarChart (id) {
      let that = this;
      let chartDom = document.getElementById(id);
      let myChart = echarts.init(chartDom);
      let dictName = {
        'Company ID VS VaR and SVaR': ['VaR', 'sVaR'],
        'Company Trading Asset Comparison': ['Gross', 'Net']
      };
      let option = {
        title: {
          text: id
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: [dictName[id][0], dictName[id][1]]
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
            name: dictName[id][0],
            type: that.barChartData.series[0].type,
            barGap: 0,
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[0].data
          },
          {
            name: dictName[id][1],
            type: that.barChartData.series[1].type,
            barGap: 0,
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[1].data
          }
        ]
      }
      myChart.setOption(option);
    },
    get_Data (id) {
      let that = this;
      that.chartData = {};
      let dictBase = {
        'Company ID VS VaR and SVaR': 'getVaRsVarRComparisonQuery',
        'Company Trading Asset Comparison': 'getTradingAssetComparison'
      };
      const start = '2015Q3';
      const end = '2016Q3';
      const base = 'http://127.0.0.1:5000/' + dictBase[id];
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
          that.barChartData.xAxisData = companies// TODO: write function
          that.barChartData.series = series
          that.DrawBarChart(id)
        });
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
  width: 100%;
  width: 40vw;
  min-width: 400px;
  height: 400px;
}
.chart {
  height: 400px;
}

</style>
