import Vue from 'vue'
import Router from 'vue-router'
import flaskTovue from '@/components/Connectors/flaskTovue'
import flaskTovue2 from '@/components/Connectors/flaskTovue2'
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
      path: '/flaskTovue',
      name: 'flaskTovue',
      component: flaskTovue,
      meta: {
        keepalive: true
      }
    },
    {
      path: '/flaskTovue2',
      name: 'flaskTovue2',
      component: flaskTovue2,
      meta: {
        keepalive: true
      }
    }
  ]
})
