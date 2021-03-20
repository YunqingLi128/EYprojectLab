<template>
    <el-col :span="24">
        <el-menu class="el-menu-vertical-demo" style="height: 860px" router @open="handelOpen" @close="handleClose" @select="menuSelect" background-color="#5A5858" text-color="#fff" active-text-color="#ffd04b">
            <!-- <el-submenu v-for="item in menu" :index="item.id" :key="item.id">
                <template slot="title">
                    <span v-text="item.name"></span>
                </template>
                <el-menu-item-group class="menu_hide" v-for="sub in item.sub" :key="sub.componentName">
                    <el-menu-item :index="sub.componentName" v-text="sub.name" -->
                <!-- <el-menu-item-group title="Quarterly Highlights">
                <el-menu-item index="/flaskTovue"> Quarterly Highlights</el-menu-item>
                </el-menu-item-group>
                <el-menu-item-group title="2">
                <el-menu-item index="/flaskTovue"> Overtime Analysis</el-menu-item>
                </el-menu-item-group>
                <el-menu-item-group title="3">
                <el-menu-item index="/flaskTovue"> Other</el-menu-item>
                </el-menu-item-group> -->
                <el-menu-item index="/home">
                    <span slot="title"> Home</span>
                </el-menu-item>
                <el-menu-item index="/flaskTovue2">
                    <span slot="title"> Quarterly Highlights</span>
                </el-menu-item>
                <el-menu-item index="/flaskTovue">
                    <span slot="title"> Overtime Analysis</span>
                </el-menu-item>
                <el-menu-item index="4">
                    <span slot="title"> Other</span>
                </el-menu-item>
        </el-menu>
    </el-col>
</template>
