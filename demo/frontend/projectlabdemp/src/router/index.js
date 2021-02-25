import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import flaskTovue from '@/components/flaskTovue'
import Home from '@/components/Home'
import getDataByCompanyID from '@/components/getDataByCompanyID'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/flaskTovue',
      name: 'flaskTovue',
      component: flaskTovue
    },
    {
      path: '/Home',
      name: 'Home',
      component: Home
    },
    {
      path: '/getDataByCompanyID/:id',
      name: 'getDataByCompanyID',
      component: getDataByCompanyID
    }
  ]
})
