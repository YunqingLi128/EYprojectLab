<template>
  <div class="StackedBarChart">
    <button @click="getData('Standardized Market risk-weighted assets breakdown by bank');">GET RISK WEIGHTED ASSETS BREAKDOWN</button>
    <button @click="getData('VaR by Asset Class and Diversification Effect');">GET VAR AND DIVERSIFICATION</button>
    <div id='Standardized Market risk-weighted assets breakdown by bank' :style="{width: '50%', height: '600px'}"></div>
    <div id='VaR by Asset Class and Diversification Effect' :style="{width: '50%', height: '600px'}"></div>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';
import ECharts from "vue-echarts";
export default {
  name: 'StackedBarChart_Comparison',
  data: function() {
    return {
      chartData: []
    }
  },
  methods: {
    DrawStackedBarChart(id) {
      let that = this;
      let chartDom = document.getElementById(id);
      let myChart = echarts.init(chartDom)
      let dict_name = {
        'Standardized Market risk-weighted assets breakdown by bank': ['De minimis positions and other adjustment', 'Standardized comprehensive risk measure','Incremental risk capital requirement','Standardized measure of specific risk add-ons','VaR-based capital','sVaR-based capital'],
        'VaR by Asset Class and Diversification Effect': ['IR', 'Debt','Equity','FX','Commodities','Diversification']
      };
      let option = {
          title: {
            text: id
          },
          legend: {
            data:[dict_name[id][0], dict_name[id][1],dict_name[id][2],dict_name[id][3],dict_name[id][4],dict_name[id][5]]
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
              type: 'bar',
              stack: 'total',
              label: {
                     show: true
              },
              emphasis: {
                     focus: 'series'
              },
              data: that.chartData[1]
          },
          {
              name: dict_name[id][1],
              type: 'bar',
              stack: 'total',
              label: {
                     show: true
              },
              emphasis: {
                     focus: 'series'
              },
              data: that.chartData[2]
          }
          {
              name: dict_name[id][2],
              type: 'bar',
              stack: 'total',
              label: {
                     show: true
              },
              emphasis: {
                       focus: 'series'
              },
              data: that.chartData[3]
          }
          {
              name: dict_name[id][3],
              type: 'bar',
              stack: 'total',
              label: {
                     show: true
              },
              emphasis: {
                     focus: 'series'
              },
              data: that.chartData[4]
          }
          {
              name: dict_name[id][4],
              type: 'bar',
              stack: 'total',
              label: {
                     show: true
              },
              emphasis: {
                     focus: 'series'
              },
              data: that.chartData[5]
          }
          {
              name: dict_name[id][5],
              type: 'bar',
              stack: 'total',
              label: {
                     show: true
              },
              emphasis: {
                     focus: 'series'
              },
              data: that.chartData[6]
          }
          ]
      }
      myChart.setOption(option);
    },
    getData (id) {
      let that = this;
      that.chartData = [];
      let dict_base = {
        'Standardized Market risk-weighted assets breakdown by bank': 'getStandardizedRiskWeightedQuery',
        'VaR by Asset Class and Diversification Effect': 'getVaRbyAssetandDiversificationQuery'
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
          let y3_data = []
          let y4_data = []
          let y5_data = []
          let y6_data = []
          chartData.push(itemNames)
          for (let key in data) {
            let company = []
            if (data.hasOwnProperty(key)) {
              x_data.push(key)
              y1_data.push(data[key][0][1])
              y2_data.push(data[key][1][1])
              y3_data.push(data[key][2][1])
              y4_data.push(data[key][3][1])
              y5_data.push(data[key][4][1])
              y6_data.push(data[key][5][1])
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
          that.chartData.push(x_data,y1_data,y2_data,y3_data,y4_data,y5_data,y6_data)
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
