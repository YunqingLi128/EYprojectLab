<template>
  <div class="overTimeBarChart">
    <b-card
      title="Number of VaR Breach"
      style="max-width: 60rem; max-height: 40rem;"
    >
    <div id='Number of VaR Breach' style="width: 100%; height: 35rem; display: inline-block;"></div>
    </b-card>
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
    drawOverTimeBarChart (id) {
      let that = this;
      let chartDom = document.getElementById('Number of VaR Breach');
      let myChart = echarts.init(chartDom);
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
      myChart.setOption(option);
    },
    getData (id, quarter1, quarter2) {
      let that = this;
      that.chartData = {};
      let dictBase = {
        'Num of VaR Breach': 'getVaRBreachOvertime'
      };
      const start = quarter1;
      const end = quarter2;
      const base = 'http://127.0.0.1:5000/' + dictBase[id];
      let listStart = [];
      let listEnd = [];
      listStart = start.split(/[Q]/);
      listEnd = end.split(/[Q]/);
      let quarters = parseInt(listStart[1]);
      let years = parseInt(listStart[0]);
      let xString = [];
      while (years <= listEnd[0]) {
        xString.push(years.toString() + 'Q' + quarters.toString())
        if (years === parseInt(listEnd[0]) && quarters === parseInt(listEnd[1])) {
          break
        }
        quarters += 1
        if (quarters > 4) {
          quarters = 1
          years += 1
        }
      }
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
          that.barChartData.xAxisData = xString// TODO: write function
          that.barChartData.series = series
          that.drawOverTimeBarChart()
        });
    }
  }
}

</script>

<style scoped>

</style>

