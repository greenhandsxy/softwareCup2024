<template>
<!--  <nav>-->
<!--    <router-link to="/">Home</router-link> |-->
<!--    <router-link to="/about">About</router-link>-->
<!--  </nav>-->
<!--  <router-view/>-->
<!--  <register/>-->
<router-view></router-view>
<!--  <LatexService></LatexService>-->
<!--  <talkModel></talkModel>-->
<!--  <AutoScoring2></AutoScoring2>-->
<!--  <videoTranslate></videoTranslate>-->
<!--  <translate></translate>-->
<!--  <camera></camera>-->
<!--  <AutoScoring></AutoScoring>-->
<!--  <XFBigModel></XFBigModel>-->
<!--  <course-video></course-video>-->
<!--  <upload-avatar></upload-avatar>-->
<!--  <index></index>-->
</template>

<script>
import login from "@/components/user/login";
import register from "@/components/user/register";
import teacherHome from "@/views/teacher/teacherHome";
import index from "./views/"
import camera from "@/components/Camera";
import XFBigModel from '@/components/XFBigModel'
import AutoScoring2 from '@/components/AutoScoring2'
import uploadAvatar from '@/components/uploadAvatar'
import translate from '@/components/translate'
import videoTranslate from '@/components/videoTranslate'
import talkModel from '@/components/talkModel'
import LatexService from '@/components/LatexService'

export default {
  name: "App",
  components: {
    login,
    register,
    teacherHome,
    index,
    camera,
    XFBigModel,
    AutoScoring2,
    // courseVideo,
    uploadAvatar,
    translate,
    videoTranslate,
    talkModel,
    LatexService
  }
};

</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.custom-drawer-title {
  /*background-color: #6495ed; !* 例如：#f5f5f5 *!*/
  font-weight: bold;
  font-size: 20px;
  color: #333333;
  font-family: 楷体;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
