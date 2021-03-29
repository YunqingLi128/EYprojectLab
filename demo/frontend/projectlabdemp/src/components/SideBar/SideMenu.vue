<template>
  <div class="wrapper">
    <nav id="sidebar" class>
      <div class="sidebar-header">
        <img :src="logoURL" style="height:50px; padding-top:3px; padding-left:30px;">
      </div>
      <ul class="list-unstyled components">
        <p>NAVIGATION</p>
        <li>
          <a href= "http://localhost:8080/#/home" data-toggle="collapse" aria-expanded="false">Home</a>
        </li>
        <li>
          <a href= "http://localhost:8080/#/flaskTovue2" data-toggle="collapse" aria-expanded="false">Quarterly Highlights</a>
        </li>
        <li>
          <a href= "http://localhost:8080/#/flaskTovue" data-toggle="collapse" aria-expanded="false">Overtime Analysis</a>
        </li>
      </ul>
    </nav>
    <div id="content">
      <nav>
        <div class="container-fluid">
          <button type="button" id="sidebarCollapse" class="navbar-btn">
            <span></span>
            <span></span>
            <span></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="nav navbar-nav ml-auto">
              <li></li>
              <li></li>
              <li></li>
            </ul>
          </div>
        </div>
      </nav>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>

var $ = require('jquery')
$(document).ready(function () {
  $('#sidebarCollapse').on('click', function () {
    $('#sidebar').toggleClass('active');
    $(this).toggleClass('active');
  });
});
export default {
  name: 'SideMenu',
  data () {
    return {
      logoURL: require("@/assets/EY.png")
    }
  },
  components: {
  },
};
</script>

<style scoped>
#sidebarCollapse {
    width: 40px;
    height: 40px;
    background: #f5f5f5;
}
#sidebarCollapse span {
    width: 80%;
    height: 2px;
    margin: 0 auto;
    display: block;
    background: #555;
    transition: all 0.5s cubic-bezier(0.810, -0.330, 0.345, 1.375);
}
#sidebarCollapse span:first-of-type {
    /* rotate first one */
    transform: rotate(45deg) translate(2px, 2px);
}
#sidebarCollapse span:nth-of-type(2) {
    /* second one is not visible */
    opacity: 0;
}
#sidebarCollapse span:last-of-type {
    /* rotate third one */
    transform: rotate(-45deg) translate(1px, -1px);
}
#sidebarCollapse.active span {
    /* no rotation */
    transform: none;
    /* all bars are visible */
    opacity: 1;
    margin: 5px auto;
}

.wrapper {
    display: flex;
    align-items: stretch;
    perspective: 1500px;
}

#sidebar {
    min-width: 250px;
    max-width: 250px;
    background: #5A5858;
    color: #fff;
    transition: all 0.6s cubic-bezier(0.945, 0.020, 0.270, 0.665);
    transform-origin: center left; /* Set the transformed position of sidebar to center left side. */
}

#sidebar.active {
    margin-left: -250px;
    transform: rotateY(100deg); /* Rotate sidebar vertically by 100 degrees. */
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
  width: 100%;
  padding: 20px;
    padding-top: 20px;
    padding-right: 20px;
    padding-bottom: 20px;
    padding-left: 20px;
  min-height: 100vh;
  transition: all 0.3s;
}
</style>
