<template>
  <div>
    <side-menu></side-menu>
  </div>
</template>
<script>

import SideMenu from "@/components/SideBar/SideMenu.vue";
import Headers from "@/components/Headers/Headers.vue";

export default {
  name: "Admin",
  components: {
    SideMenu,
    Headers
  }
}
</script>
