<template>
  <div class="barChart">
    <button @click="getData('Company ID VS VaR and SVaR');">GET VAR SVAR COMPARISON</button>
    <button @click="getData('Company Trading Asset Comparison');">GET TRADING ASSET</button>
    <div id='Company ID VS VaR and SVaR' :style="{width: '50%', height: '600px'}"></div>
    <div id='Company Trading Asset Comparison' :style="{width: '50%', height: '600px'}"></div>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';
import ECharts from "vue-echarts";
export default {
  name: 'BarChart_Comparison',
  data: function() {
    return {
      chartData: []
    }
  },
  methods: {
    DrawBarChart(id) {
      let that = this;
      let chartDom = document.getElementById(id);
      let myChart = echarts.init(chartDom)
      let dict_name = {
        'Company ID VS VaR and SVaR': ['VaR', 'sVaR'],
        'Company Trading Asset Comparison': ['Gross', 'Net']
      };
      let option = {
          title: {
            text: id
          },
          legend: {
            data:[dict_name[id][0], dict_name[id][1]]
          },
          xAxis: {
            type: 'category',
            data: that.chartData[0]
          },
          yAxis: {
              type: 'value'
          },
          tooltip: {
            trigger:'axis'
          },
          series: [
          {
              name: dict_name[id][0],
              data: that.chartData[1],
              type: 'bar'
          },
          {
              name: dict_name[id][1],
              data: that.chartData[2],
              type: 'bar'
          }
          ]
      }
      myChart.setOption(option);
    },
    getData (id) {
      let that = this;
      that.chartData = [];
      let dict_base = {
        'Company ID VS VaR and SVaR': 'getVaRsVarRComparisonQuery',
        'Company Trading Asset Comparison': 'getTradingAssetComparison'
      };
      const start = '2016Q4';
      const end = '2016Q4';
      const base = 'http://127.0.0.1:5000/' + dict_base[id];
      axios
        .get(base, {
          params: {
            'start': start,
            'end': end
          }
        })
        .then(function (response) {
          let itemNames = response.data.item
          let data = response.data.data
          let chartData = []
          let x_data = []
          let y1_data = []
          let y2_data = []
          chartData.push(itemNames)
          for (let key in data) {
            let company = []
            if (data.hasOwnProperty(key)) {
              x_data.push(key)
              y1_data.push(data[key][0][1])
              y2_data.push(data[key][1][1])
              company.push(key)
              console.log(data[key])
              for (const item of data[key]) {
                console.log(item)
                company.push(item[1])
              }
            }
            chartData.push(company)
          }
          console.log(chartData)
          that.chartData.push(x_data,y1_data,y2_data)
          console.log(that.chartData)
          that.DrawBarChart(id)
          return chartData
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
