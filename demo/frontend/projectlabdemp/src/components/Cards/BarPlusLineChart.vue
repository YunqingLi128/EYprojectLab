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
import axios from 'axios';
import * as echarts from 'echarts';

export default {
  name: 'BarLineCharts',
  data: function () {
    return {
      barLineChartsData: {}
    }
  },
  methods: {
    DrawBarLineChart (id) {
      let that = this;
      let chartDom = document.getElementById(id);
      let myChart = echarts.init(chartDom);
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
      myChart.setOption(option);
    },
    getData (id, quarter, selected) {
      let that = this;
      that.chartData = {};
      let dictBase = {
        'trading-asset': 'getTradingAssetsAndChangeByQuarter',
        'trading-liabilities': 'getTradingLiabilitiesAndChangeByQuarter',
        'net-trading-asset': 'getNetTradingAssetAndPercentChange',
        'gross-trading-asset': 'getGrossTradingAssetAndPercentChange'
      };
      let legendBase = {
        'trading-asset': ['Trading Asset', 'Trading Asset Change from Last Quarter'],
        'trading-liabilities': ['Trading Liability', 'Trading Liability Change from Last Quarter'],
        'net-trading-asset': ['Net Trading Asset', 'Net Trading Asset Change from Last Quarter'],
        'gross-trading-asset': ['Gross Trading Asset', 'Gross Trading Asset Change from Last Quarter']
      }
      const base = 'http://127.0.0.1:5000/' + dictBase[id];
      axios
        .get(base, {
          params: {
            'quarter': quarter
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
          let groupOne = [];
          let groupTwo = [];
          for (let key of selected) {
            if (data.hasOwnProperty(key)) {
              companies.push(key)
              groupOne.push(data[key][0][0])
              groupTwo.push(data[key][0][1])
            }
          }
          let series = [];
          let legendList = [];
          let chartItemOne = {};
          let chartItemTwo = {};
          let yAxisOne = {};
          let yAxisTwo = {};
          let yAxis = [];

          chartItemOne.name = legendBase[id][0];
          chartItemOne.type = 'bar';
          chartItemOne.data = groupOne;

          chartItemTwo.name = legendBase[id][1];
          chartItemTwo.type = 'line';
          chartItemTwo.data = groupTwo;
          chartItemTwo.yAxisIndex = 1;

          yAxisOne.name = legendBase[id][0];
          yAxisOne.scale = true;
          yAxisOne.type = 'value';
          yAxisOne.max = Math.max.apply(Math,groupOne) + 50000000;
          yAxisOne.min = 0;

          yAxisTwo.name = 'Percentage';
          yAxisTwo.scale = true;
          yAxisTwo.type = 'value';
          yAxisTwo.max = Math.round(Math.max.apply(Math,groupTwo) + 20);
          yAxisTwo.min = Math.round(Math.min.apply(Math,groupTwo) - 20);

          series = [chartItemOne, chartItemTwo];
          legendList = legendBase[id];
          yAxis = [yAxisOne, yAxisTwo]
          console.log(companies);
          console.log(series);
          that.barLineChartsData.legendData = legendList;
          that.barLineChartsData.xAxisData = companies;
          that.barLineChartsData.yAxisData = yAxis;
          that.barLineChartsData.series = series;
          that.DrawBarLineChart(id);
        });
    },
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
  max-width: 60rem;
  max-height: 40rem;
  margin-bottom: 20px;
}

.bar-line-chart {
  width: 100%;
  height: 35rem;
  display: inline-block;
}

</style>
