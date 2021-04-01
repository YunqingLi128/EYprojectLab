<template>
  <div>
    <!-- <router-view/> -->
    <el-container v-if='$route.meta.keepalive'>
      <el-header style="background-color:#323030; width:100%; z-index:1; text-align: left; position:fixed; top:0; left:0">
        <img :src="logoURL" style="height:50px; padding-top:3px; padding-left:30px;">
      </el-header >
      <el-container style="margin-top: 60px">
        <el-aside style="width:200px; height:100%; position: fixed;">
          <keep-alive>
            <v_leftmenu></v_leftmenu>
          </keep-alive>
        </el-aside>
      <el-container style="margin-left: 200px; position: relative; z-index: 0">
        <el-main>
            <router-view></router-view>
        </el-main>
      </el-container>
      </el-container>
    </el-container>
    <router-view v-if="!$route.meta.keepalive"></router-view>
  </div>
</template>

<script>

import SideMenu from '@/components/SideBar/SideMenu'

export default {
  name: 'Headers',
  data () {
    return {
      logoURL: require('@/assets/EY.png')
    }
  },
  components: {
    'v_leftmenu': SideMenu
  },
  beforeCreate () {
    document.querySelector('body').setAttribute('style', 'margin: 0px;')
  },
  beforeDestroy () {
    document.body.removeAttribute('style')
  }
}
</script>

<style scoped>

</style>
