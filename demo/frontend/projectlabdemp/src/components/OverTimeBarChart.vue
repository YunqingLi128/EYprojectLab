<template>
  <div class="StackBarChart">
    <button @click="get_Data ();">GET BAR TREND</button>
    <div id='Number of VaR Breach' :style="{width: '50%', height: '600px'}"></div>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';

export default {
  name: 'OverTimeBarChart',
  data: function () {
    return {
      barChartData: {}
    }
  },
  methods: {
    drawOverTimeBarChart () {
      let that = this;
      let chartDom = document.getElementById('Number of VaR Breach');
      let myChart = echarts.init(chartDom);
      let option = {
        title: {
          text: 'Number of VaR Breach'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
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
        series: [
          {
            name: that.barChartData.series[0].name,
            type: that.barChartData.series[0].type,
            barGap: 0,
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[0].data
          },
          {
            name: that.barChartData.series[1].name,
            type: that.barChartData.series[1].type,
            barGap: 0,
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[1].data
          },
          {
            name: that.barChartData.series[2].name,
            type: that.barChartData.series[2].type,
            barGap: 0,
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[2].data
          },
          {
            name: that.barChartData.series[3].name,
            type: that.barChartData.series[3].type,
            barGap: 0,
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[3].data
          },
          {
            name: that.barChartData.series[4].name,
            type: that.barChartData.series[4].type,
            barGap: 0,
            emphasis: {
              focus: 'series'
            },
            data: that.barChartData.series[4].data
          }
        ]
      }
      myChart.setOption(option);
    },
    get_Data () {
      let that = this;
      that.chartData = {};
      const start = '2015Q3';
      const end = '2016Q3';
      const base = 'http://127.0.0.1:5000/getVaRBreachOvertime';
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
          that.chartData.legend = companies
          that.barChartData.xAxisData = ['2015Q3', '2015Q4', '2016Q1', '2016Q2', '2016Q3'] // TODO: write function
          that.barChartData.series = series
          that.drawOverTimeBarChart()
        });
    }
  }
}

</script>

<style scoped>

</style>
