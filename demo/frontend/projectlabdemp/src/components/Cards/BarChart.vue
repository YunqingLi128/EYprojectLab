<template>
  <div class="barChart">
    <label>
      <b-form-input id="input-quarter" v-model.trim="quarter" placeholder="Enter the quarter"></b-form-input>
      <button @click="get_Data('Company ID VS VaR and SVaR');get_Data('Company Trading Asset Comparison');">GET COMPARISON</button>
    </label>
    <b-card-group deck>
    <b-card
      title="Company ID VS VaR and SVaR"
      style="max-width: 60rem; max-height: 40rem;"
    >
      <div id='Company ID VS VaR and SVaR' style="width: 100%; height: 35rem; display: inline-block;"></div>
    </b-card>
    <b-card
      title="Company Trading Asset Comparison"
      style="max-width: 60rem; max-height: 40rem;"
    >
      <div id='Company Trading Asset Comparison' style="width: 100%; height: 35rem; display: inline-block;"></div>
    </b-card>
    </b-card-group>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';

export default {
  name: 'BarChart_Comparison',
  data: function () {
    return {
      quarter: '',
      barChartData: {}
    }
  },
  methods: {
    DrawBarChart (id) {
      let that = this;
      let chartDom = document.getElementById(id);
      let myChart = echarts.init(chartDom);
      // let dictName = {
      //   'Company ID VS VaR and SVaR': ['VaR', 'sVaR'],
      //   'Company Trading Asset Comparison': ['Gross', 'Net']
      // };
      let option = {
        title: {
          text: id,
          show: false
        },
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
        series: that.barChartData.series
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
      const start = this.quarter;
      const end = this.quarter;
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
          let data = response.data;
          let companies = [];
          let groups = {};
          for (let key in data) {
            if (data.hasOwnProperty(key)) {
              companies.push(key)
              for (let itemName in data[key]) {
                if (data[key].hasOwnProperty(itemName)) {
                  if (groups.hasOwnProperty(itemName)) {
                    groups[itemName].push(data[key][itemName]);
                  } else {
                    groups[itemName] = [data[key][itemName]];
                  }
                }
              }
            }
          }
          let series = [];
          for (let key in groups) {
            let chartItem = {};
            chartItem.name = key
            chartItem.type = 'bar'
            chartItem.data = groups[key]
            series.push(chartItem)
          }
          console.log(companies)
          console.log(series)
          that.barChartData.legendData = Object.keys(groups)
          that.barChartData.xAxisData = companies
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
