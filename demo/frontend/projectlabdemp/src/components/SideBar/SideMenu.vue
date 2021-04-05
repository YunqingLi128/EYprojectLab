<template>
  <div class="wrapper">
    <nav id="sidebar" class>
      <div class="sidebar-header">
        <img :src="logoURL" style="height:50px; padding-top:3px; padding-left:30px;">
      </div>
      <ul class="list-unstyled components">
        <p>NAVIGATION</p>
        <li>
          <a href= "/#/home" data-toggle="collapse" aria-expanded="false">Home</a>
        </li>
        <li>
          <a href= "/#/QuarterlyHighlight" data-toggle="collapse" aria-expanded="false">Quarterly Highlights</a>
        </li>
        <li>
          <a href= "/#/OverTimeAnalysis" data-toggle="collapse" aria-expanded="false">Overtime Analysis</a>
        </li>
      </ul>
    </nav>
    <div id="content">
      <nav>
        <div class="container-fluid">
          <b-button squared @click="changeStatus()" id="sidebarCollapse" class="navbar-btn" size='sm'>{{toggleStatus}}</b-button>
        </div>
      </nav>
    </div>
    <router-view id="router-view"></router-view>
  </div>
</template>

<script>
var $ = require('jquery')
$(document).ready(function () {
  $('#sidebarCollapse').on('click', function () {
    $('#sidebar').toggleClass('active')
    $(this).toggleClass('active')
  })
})

export default {
  name: 'SideMenu',
  data () {
    return {
      logoURL: require('@/assets/EY.png'),
      toggleStatus: '<'
    }
  },
  components: {
  },

  methods: {
    changeStatus () {
      if (this.toggleStatus === '<') {
        this.toggleStatus = '>'
      } else {
        this.toggleStatus = '<'
      }
    }
  }
}
</script>

<style scoped>
#sidebarCollapse {
  background: #5A5858;
  border-color: #5A5858;
  margin-left: -35px;
  margin-top:-36px;
}

#sidebarCollapse span {
  width: 80%;
  height: 2px;
  margin: 0 auto;
  display: block;
  background: #5A5858;
  border-color: #5A5858;
  transition: all 0.5s cubic-bezier(0.810, -0.330, 0.345, 1.375);
}

.wrapper {
  display: flex;
  align-items: stretch;
  perspective: 2000px;
}

#sidebar {
  min-width: 200px;
  max-width: 200px;
  background: #5A5858;
  color: #fff;
  transition: all 0.6s cubic-bezier(0.945, 0.020, 0.270, 0.665);
  transform-origin: center;
}

#sidebar.active {
  margin-left: -200px;
}

a[data-toggle="collapse"] {
  position: relative;
}

.dropdown-toggle::after {
  display: block;
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
}

body {
  font-family: 'Poppins', sans-serif;
  background: #999;
}

p {
  font-family: 'Poppins', sans-serif;
  font-size: 1.1em;
  font-weight: 300;
  line-height: 1.7em;
  color: #fff;
}

a, a:hover, a:focus {
  color: inherit;
  text-decoration: none;
  transition: all 0.3s;
}

#sidebar .sidebar-header {
  padding: 20px;
  background: #5A5858;
}

#sidebar ul.components {
  padding: 20px 0;
  border-bottom: 1px solid #5A5858;
}

#sidebar ul p {
  color: #fff;
  padding: 10px;
}

#sidebar ul li a {
  padding: 10px;
  font-size: 1.1em;
  display: block;
}

#sidebar ul li a:hover {
  color: #5A5858;
  background: #ffffff;
}

#sidebar ul li.active > a, a[aria-expanded="true"] {
  color: #ffffff;
  background: #5A5858;
}

ul ul a {
  font-size: 0.9em !important;
  padding-left: 30px !important;
  background: #5A5858;
}

.ml-auto, .mx-auto {
  margin-left: auto!important;
}

#content {
  width: 1px;
  padding: 17px 10px 15px 15px;
  min-height: 100vh;
  transition: all 0.3s;
  background-color: #5A5858;
}

#router-view {
  width: 100%;
  margin: 5px 15px 5px 20px;
}
</style>
