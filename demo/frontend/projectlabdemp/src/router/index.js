import Vue from 'vue'
import Router from 'vue-router'
import OverTimeAnalysis from '@/components/Connectors/OverTimeAnalysis'
import QuarterlyHighlight from '@/components/Connectors/QuarterlyHighlight'
import MarketEnvironment from '@/components/Connectors/FredAnalysis'
import home from '@/components/Connectors/home'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'home',
      component: home,
      meta: {
        keepalive: true
      }
    },
    {
      path: '/OverTimeAnalysis',
      name: 'OverTimeAnalysis',
      component: OverTimeAnalysis,
      meta: {
        keepalive: true
      }
    },
    {
      path: '/QuarterlyHighlight',
      name: 'QuarterlyHighlight',
      component: QuarterlyHighlight,
      meta: {
        keepalive: true
      }
    },
    {
      path: '/MarketEnvironment',
      name: 'MarketEnvironment',
      component: MarketEnvironment,
      meta: {
        keepalive: true
      }
    }
  ]
})
