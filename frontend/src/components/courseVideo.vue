<template>
  <div id="app">
    <h1 style=""></h1>
    <div id="titleBar"  @blur="moveon">
      <a href="logo.png" target="_blank" @click.prevent="goHome">
        <img class="logo" src="../assets/logo.png" >
      </a>
      <ul>
        <li style="cursor: default"><router-link to="/courseCenter">首页</router-link></li>
        <li style="cursor: help">
          <router-link :to="{ name: 'courseDetail', params: { courseName: courseName }}">
            <span>课程详情</span>
          </router-link>
        </li>
      </ul>
    </div>

    <div id="player">
      <video id="video1" controls autoplay :src=video_source type="video/mp4" :poster=video_poster></video>

      <div id="name">请选择视频</div>
      <div id="author"></div>
    </div>

    <div id="selector">
      <div id=index v-for="(item, index) in list" @mouseover="moveon(index)" @mouseout="moveoff(index)" :style="{backgroundColor: item.bgcolor}" :key=index @click="be_clicked(index)">
        <video :src=item.src poster="../assets/courseLogo.jpg"></video>
        <div><strong>{{item.videoname}}</strong></div>

      </div>
    </div>
    <div id="d" style="width: 0px; height: 0px;"></div>
  </div>
</template>
<script>
import {useRoute, useRouter} from 'vue-router';
import {computed} from "vue";
import img from "../assets/courseLogo.jpg"

export default {
  name: "courseVideo",
  data() {
    return {
      msg: 'Welcome to Your Vue.js App',
      list : [
        {author:"作者",videoname:"1.1 周易的作者", describe:"当讨论《周易》的起源和作者时，我们进入了中国古代文化中最为深远和神秘的领域之一。《周易》被视为中国传统文化的重要组成部分，它不仅仅是一部占卜经典，更是一部充满智慧和哲理的文化遗产。", bgcolor: 'transparent',src: "https://media.w3.org/2010/05/sintel/trailer.mp4"},
        {author:"作者",videoname:"1.2 乾、坤、泰卦解读", describe:"在中国文化中，《周易》中的乾、坤、泰卦象征着宇宙间最基本的力量和原理。乾为天，坤为地，泰为两者和谐共处的状态。这些卦象不仅仅是占卜工具，更是古代智者对宇宙运行规律的深刻洞察和哲学思考的结晶。", bgcolor: 'transparent',src: "https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-360p.mp4"},
        {author:"作者",videoname:"2.1 老子其人", describe:"在中国哲学史上，老子被视为道家学派的创始人之一，他的思想深刻影响了中国文化和哲学的发展。", bgcolor: 'transparent',src: "http://www.w3school.com.cn/example/html5/mov_bbb.mp4"},
        {author:"作者",videoname:"2.2 《道德经》这本书", describe:"《道德经》是中国古代哲学经典之一，也是世界文化宝库中的重要组成部分。这部短小却蕴含深刻智慧的书籍，由老子创作，被誉为道家思想的典范。本视频将深入解读《道德经》中的主要思想和核心理念，探索其在古代和现代的意义与价值。", bgcolor: 'transparent',src: "https://www.w3schools.com/html/movie.mp4"},
        {author:"作者",videoname:"3.1 上善若水", describe:"“上善若水，水善利万物而不争”，这句著名的道德经箴言，深刻概括了道家哲学的核心理念之一。水以其柔和而无处不在的特性，成为了老子用以比喻道德与治理之道的象征。本视频将探索“上善若水”这一理念背后的深刻内涵，探讨其在道家思想中的重要地位以及其在现代社会中的普适性和价值。", bgcolor: 'transparent',src: "https://media.w3.org/2010/05/sintel/trailer.mp4"},
        {author:"作者",videoname:"4.1 《论语》与‘对话录’", describe:"《论语》作为中国古代儒家经典之一，记录了孔子及其门徒的言行和思想，被誉为儒家学说的核心典籍之一。它不仅是一部伦理道德和政治治理的指南，更是中国文化中重要的思想宝库。本视频将深入探讨《论语》这部书中所包含的“对话录”，揭示其中的智慧和哲理，以及其对中国和世界文化产生的深远影响。", bgcolor: 'transparent',src: "https://stream7.iqilu.com/10339/upload_transcode/202002/09/20200209105011F0zPoYzHry.mp4"},
        {author:"作者",videoname:"5.1 孔子的历史形象", describe:"孔子，作为中国历史上最为杰出的思想家和教育家之一，他的思想和影响远超其时代。他的生平和思想被后人奉为圭臬，成为中国儒家传统的奠基者。本视频将探索孔子的历史形象，审视他在中国文化中的地位和影响力，以及他对道德、教育和社会治理理念的重大贡献。", bgcolor: 'transparent',src: "https://stream7.iqilu.com/10339/upload_transcode/202002/09/20200209104902N3v5Vpxuvb.mp4"},
        {author:"作者",videoname:"5.2 孔子的学习之道", describe:"孔子不仅是中国古代伟大的思想家，也是一位卓越的教育家。他提倡的学习之道深深植根于中国传统文化中，对后世教育理念产生了深远影响。本视频将深入探讨孔子的学习之道，探索他的教育思想和方法，以及这些理念如何影响了中国古代及今日教育的发展和实践。", bgcolor: 'transparent',src: "http://vjs.zencdn.net/v/oceans.mp4"},
      ],
      video_source:"../assets/1.mp4",
      video_poster: img,
    }
  },
  mounted() {
  },
  methods: {
    moveoff(index) {
      this.list[index].bgcolor='transparent';

    },
    moveon(index) {
      this.list[index].bgcolor="cadetblue";
    },
    be_clicked(index){
      document.getElementById("author").innerHTML = this.list[index].author;
      document.getElementById("name").innerHTML = "<strong>导言：</strong>"+this.list[index].describe;
      this.video_source = this.list[index].src;
      this.video_poster = img;
    },
  },

  setup(){
    const route = useRoute(); // 获取当前路由信息
    const courseName = computed(() => route.params.courseName); // 使用computed属性获取courseName参数
    const router = useRouter()
    function goHome(){
      router.push('/')
    }

    return {
      goHome,
      courseName
    }
  }
};
</script>
<style scoped>
body{
  /* background-color: #7BC5AE; */
  background-color: rgb(240,248,255);
  width: 100%;
  height: 100%;
}
*{
  margin: 0px;
  padding: 0px;
}
#titleBar{
  background-color: rgb(85,125,203);
  height: 10%;
  position: absolute;
  width: 100%;
  /* display: flex; */
}

#titleBar .logo{
  width: 10%;
  height: 85%;
  margin: 0.4% 0.8%;
  float: left;
  -webkit-transition: -webkit-transform 0.3s;
}
#titleBar .logo:hover{
  /* 鼠标放在上面，拉伸的比例 */
  transform: scale(1.1,1.1);
}

#titleBar>.name{
  padding-top: 16px;
  height: 60px;
  line-height: 60px;
  font-size: 40px;
  font-family: 黑体;
  margin: 0px 0.8%;
  line-height: 100%;
  float: left;
  background: white;
  -webkit-text-fill-color: transparent;
  -webkit-background-clip: text;
}

#titleBar>ul{
  float: right;
  list-style-type: none;
  width: 15%;
  margin-right: 5%;
}
#titleBar>ul li{
  text-align: center;
  width: 50%;
  float: left;
  font-size: 20px;
  font-family: 行楷;
  paddig: 0 5%;
  line-height: 350%;
  transition:font-weight 0.3s, color 0.3s, background-color 0.3s,transform 0.3s;
  -moz-transition:font-weight 0.3s, color 0.3s, background-color 0.3s,-moz-transform 0.3s;
  -webkit-transition:font-weight 0.3s, color 0.3s, background-color 0.3s,-webkit-transform 0.3s;
  -o-transition:font-weight 0.3s, color 0.3s, background-color 0.3s,-o-transform 0.3s;
}
#titleBar>ul li:hover{
  font-weight: bolder;
  color: white;
  background-color: darkslategray;
  transform: scale(1.1,1.1);
}
#titleBar>ul a{
  color: #000000;
  text-decoration: none;
}

#player{
  height: 80%;
  width: 55%;
  position: absolute;
  left: 5%;
  top: 15%;
  box-shadow: 5px 5px 10px 2px black ;
  -moz-box-shadow: 5px 5px 10px 2px black ;   		/* 老的 Firefox */
  background-color: rgb(240,248,255);
}
#player>#video1{
  width: 100%;
  height: 82.3%;
  /*position: absolute;*/
  top: 0;
}
#player>#name{
  width: 90%;
  height: 15%;
  font-size: 25px;
  font-family: 楷体;
  position: absolute;
  top: 83%;
  overflow: auto;
  left: 1%;
}
#player>#author{
  width: 100%;
  height: 3%;
  font-size: 18px;
  font-family: 楷体;
  position: absolute;
  bottom: 2%;
  left: 90%;
}

#selector{  /*右侧选项栏*/
  overflow: auto;
  height: 85%;
  width: 30%;
  position: absolute;
  right: 3%;
  top: 12.5%;
  background-color: rgb(240,248,255);
}
#selector>div{			/*这是selector里每个选项框*/
  width: 100%;
  height: 31%;
  position: relative;
  padding: 2px 0px;
  border-bottom: 2px solid black;
}
#selector>div>video{	/*选项的视频 */
  width: 60%;
  position: relative;
  height: 100%;
  float: left;
  padding-left: 3px;
}
#selector>div>div{		/*选项视频的名称*/
  width: 28%;
  height: 100%;
  position: relative;
  padding: 2px 1px;
  top: 2%;
  cursor: default;
  float: right;
  color: rgb(5, 0, 0);
  zIndex: 9999;
  font-family: 楷体;
}
</style>