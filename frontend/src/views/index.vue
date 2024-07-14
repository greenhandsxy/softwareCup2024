<template>

  <div class="common-layout">
    <el-container>
      <el-header :class="{ dynamicTitle: true }">
        <div class="header-content">
          <img src="../assets/logo.png" alt="logo" class="logo" width="110" height="55" style="margin-left: 50px">
          <h3 v-text="currentHeader"></h3>
        </div>
        <div class="right">
          <router-link v-if="!isLoggedIn" to="/login">
            <el-button>
              注册或登录
            </el-button>
          </router-link>
        </div>
      </el-header>
      <el-container style="">
        <el-aside width="200px" >

          <div v-if="isLoggedIn">
            <router-link @click.prevent="changeHeader('我的信息')" to="/studentInfo">
            <el-avatar  :size="large" :src="AvatarUrl" style="width: 100px; height: 100px"/>
            </router-link>
            <p class="mb-2">你好：{{ $store.state.user.nickname }}</p> <el-button @click="logout">退出登录</el-button>
          </div>
          <el-col :span="24">
            <el-menu
                default-active="1"
                class="el-menu-vertical-demo"
                @open="handleOpen"
                @close="handleClose"
            >
                    <router-link @click.prevent="changeHeader('选课中心')" :to="{ name: 'courseCenter' }">
              <el-menu-item index="1" @click="message = '快去找到自己喜欢的课程进行学习吧！'">
                <el-icon><Menu /></el-icon>
                <span>
                  <p>
                      选课中心
                  </p>
                </span>
              </el-menu-item>
                    </router-link>
                    <router-link  @click.prevent="changeHeader('我的信息')" to="/studentInfo">
              <el-menu-item v-if="isLoggedIn" index="2" @click="message = '听说制作趣味头像还挺有趣的，快去试试吧！'">
                <el-icon><UserFilled /></el-icon>
                <span>
                  <p>
                    我的信息
                  </p>
                </span>
              </el-menu-item>
                  </router-link>
              <router-link  @click.prevent="changeHeader('我的选课')" to="/studentCourse">
              <el-menu-item v-if="isLoggedIn" index="3" @click="message = '看看自己的课程成绩是否理想呢，加油去提高吧！'">
                <el-icon><Collection /></el-icon>
                <span>
            <p>
                我的选课
            </p>
                </span>
              </el-menu-item>
              </router-link>

              <router-link @click.prevent="changeHeader('项目及团队介绍')" to="/about">
                <el-menu-item v-if="!isLoggedIn" index="5">
                  <el-icon><InfoFilled /></el-icon>
                  <span>
                  <p>
                      项目及团队介绍
                  </p>
                </span>
                </el-menu-item>
              </router-link>

              <el-sub-menu v-if="isLoggedIn" index="4" @click="message = 'AI工具，让学习更高效、更轻松！'">
                <template #title>
                  <el-icon><Box /></el-icon>
                  <span>AI助学工具</span>
                </template>
                  <el-menu-item index="1-1" @click="showTranslate = true">
                    <el-icon><Switch /></el-icon>
                    英汉翻译
                  </el-menu-item>
                  <el-menu-item index="1-2" @click="showVideoTranslate = true">
                    <el-icon><Mic /></el-icon>
                    语音翻译
                  </el-menu-item>
                <el-menu-item index="1-3" @click="showPPTGenerate = true">
                  <el-icon><Document /></el-icon>
                  ppt自动生成
                </el-menu-item>
                <el-menu-item index="1-4" @click="showOCR = true">
                  <el-icon><Picture /></el-icon>
                  图片文字识别
                </el-menu-item>
                <el-menu-item index="1-5" @click="showLatex = true">
                  <el-icon><EditPen /></el-icon>
                  Latex公式识别
                </el-menu-item>
              </el-sub-menu>
            </el-menu>
          </el-col>
        </el-aside>
        <el-container class="myContainer">
        <el-main>

          <router-view></router-view>
          <el-drawer
              v-model="showTranslate"
              size="30%"
              direction="rtl"
              :before-close="onClose"
              :modal="true"
              :resizeable="true"
          >
            <template #title>
              <div class="custom-drawer-title">
                英汉翻译工具
              </div>
            </template>
            <translate></translate>
          </el-drawer>
          <el-drawer
              v-model="showVideoTranslate"
              size="30%"
              direction="rtl"
              :before-close="onClose"
              :modal="true"
              :resizeable="true"
          >
            <template #title>
              <div class="custom-drawer-title">
                语音翻译工具
              </div>
            </template>
            <videoTranslate></videoTranslate>
          </el-drawer>
          <el-drawer
              v-model="showPPTGenerate"
              size="30%"
              direction="rtl"
              :before-close="onClose"
              :modal="true"
              :resizeable="true"
          >
            <template #title>
              <div class="custom-drawer-title">
                ppt自动生成工具
              </div>
            </template>
            <PPTGenerate></PPTGenerate>
          </el-drawer>
          <el-drawer
              v-model="showOCR"
              size="30%"
              direction="rtl"
              :before-close="onClose"
              :modal="true"
              :resizeable="true"
          >
            <template #title>
              <div class="custom-drawer-title">
                图片文字识别工具
              </div>
            </template>
            <OCR></OCR>
          </el-drawer>
          <el-drawer
              v-model="showLatex"
              size="30%"
              direction="rtl"
              :before-close="onClose"
              :modal="true"
              :resizeable="true"
          >
            <template #title>
              <div class="custom-drawer-title">
                Latex公式识别
              </div>
            </template>
            <div class="drawer">
              <LatexService></LatexService>
            </div>
          </el-drawer>
          <div v-if="isLoggedIn">
            <XFBigModel :message="message"></XFBigModel>
          </div>
        </el-main>
        <el-footer>
          POWERED BY LXQZ TEAM
        </el-footer>
          </el-container>
      </el-container>
    </el-container>
  </div>


</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import api from '../../src/api'
//引入指示器
import { Pagination } from 'swiper';
import 'swiper/css/pagination';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import {toast} from "../../src/utils/popup";

import { mapActions, mapGetters } from 'vuex';
import { watchEffect } from 'vue'
import XFBigModel from '@/components/XFBigModel'
import {Loading} from "@element-plus/icons-vue";
import store from "@/store";
import defaultImg from "@/assets/default.png"
import translate from "@/components/translate"
import videoTranslate from "@/components/videoTranslate"
import OCR from "@/components/OCR"
import PPTGenerate from "@/components/PPTGenerate";
import router from "@/router";
import LatexService from "@/components/LatexService";

export default {
  name: "index",
  beforeRouteEnter(to, from, next) {
    next(vm => {
      // 在这里，vm指的是组件实例
      vm.$router.push({ name: 'courseCenter' }); // 这将激活选课中心链接
    });
  },
  components: {
    Loading,
    Swiper,
    SwiperSlide,
    XFBigModel,
    translate,
    videoTranslate,
    OCR,
    PPTGenerate,
    LatexService
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'getUsername', 'getUserAvatar', 'getUserRole']),
    ...mapGetters(['avatar']),
  },
  methods: {
    ...mapActions(['logout']),
    changeHeader(title) {
      this.currentHeader = title;
    },
    onClose() {
      this.showTranslate = false;
      this.showVideoTranslate = false;
      this.showPPTGenerate = false;
      this.showOCR = false;
      this.showLatex = false;
    },
  },
  data(){
    return {
      currentHeader: "选课中心", // 初始标题
      module: [Pagination]
    }
  },

  setup() {
    const value = ref(new Date())

    const courses = ref([]);
    const currentPage = ref(1); // 当前页码
    const pageSize = ref(10); // 每页显示条数
    const total = ref(0); // 总记录数
    const courseTypes = reactive([]);
    const currType = ref("");

    const AvatarUrl = ref("");
    const message = ref("")

    onMounted(() => {
      message.value = "同学你好，欢迎登录龙兴启智智教平台，我是你的智能助教，有什么问题快来向我提问吧！"
      if(store.state.user.isLoggedIn && store.state.user.username.includes('bear')){
        setTimeout(async () => {
          toast("一只pp人lai进来li！！！", "error")
        }, 500);
        setTimeout(async () => {
          toast("pp人lai进来li！！！", "error")
        }, 1000);
        setTimeout(async () => {
          toast("lai进来li！！！", "error")
        }, 1500);
      }

      loadCourses(currType);
      loadCourseType();
      AvatarUrl.value = store.state.user.avatar == null ? defaultImg : store.state.user.avatar;
    });

    watchEffect(async () => {
      AvatarUrl.value = store.state.user.avatar || defaultImg;
    });

    // 加载课程数据
    const loadCourses = () => {
      api.getCourses({ pageNum: currentPage.value, pageSize: pageSize.value }, currType.value)
          .then((res) => {
            courses.value = res.data.data.records; // 更新课程列表
            total.value = res.data.data.total; // 更新总记录数
          });
    };

    const loadCourseType = () => {
      api.getAllCourseType()
      .then((res) => {
        courseTypes.value = res.data.data;
      });
    }

    // 分页改变时的处理函数
    const handlePageChange = (newPage) => {
      currentPage.value = newPage;
      loadCourses(currType); // 重新加载数据
    };

    const showTranslate = ref(false)
    const showVideoTranslate  =ref(false)
    const showPPTGenerate = ref(false)
    const showOCR = ref(false)
    const showLatex = ref(false)

    return {
      value,
      courses,
      currentPage,
      pageSize,
      total,
      handlePageChange,
      courseTypes,
      AvatarUrl,
      showTranslate,
      showVideoTranslate,
      showPPTGenerate,
      showOCR,
      message,
      showLatex
    }
  }
}

</script>

<style scoped>
/*.custom-drawer-title {*/
/*  font-weight: bold;*/
/*  font-size: 15px;*/
/*  font-family: 楷体;*/
/*}*/

.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.vertical-tabs-container {
  display: flex;
  flex-direction: column;
}

.course-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 10px; /* 列与列之间的间隔 */
}

.course-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px; /* 图片与文字之间的间隔 */
  width: calc(20% - 10px); /* 每个item占20%，减去gap的宽度，以适应5个元素 */
}

.course-item img {
  max-width: 100%;
  height: auto; /* 保持图片宽高比 */
}
a{
  text-decoration: none;
}
.router-link-active {
  text-decoration: none;
}
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px; /* 或者具体的高度，根据实际情况调整 */
}
.el-aside {
  background-image: linear-gradient(to top, #6495ed, #ffffff);
  /* 更改颜色以适应你的设计需求 */
  height: 110vh;
}
.el-header {
  background-image: linear-gradient(to left, #6495ed, #ffffff);
  height: 100px;
  position: relative; /* 为容器添加相对定位 */
}
.right {
  position: absolute; /* 使用绝对定位 */
  top: 50%; /* 根据需要调整垂直位置，这里假设将按钮垂直居中 */
  transform: translateY(-50%); /* 用于垂直居中对齐，考虑按钮自身的高度 */
  right: 20px; /* 距离右侧的距离，按需调整 */
}
.header-content {
  display: flex;
  align-items: center; /* 保持垂直居中 */
  justify-content: center; /* 使 h3 文本居中 */
}

.logo {
  position: absolute; /* 使图片相对于 .header-content 定位 */
  left: 0; /* 将图片移到最左边 */
  margin-right: auto; /* 为标题提供右侧空间 */
}

/* 为标题添加额外的样式，确保它不受图片绝对定位影响 */
.header-content h3 {
  position: relative; /* 使 h3 能够覆盖图片区域 */
  z-index: 1; /* 确保 h3 在图片之上 */
}

.el-main {
  height: calc(100vh - 100px - 200px); /* 减去header和aside的高度 */
  overflow-y: auto; /* 允许内容溢出时出现垂直滚动条 */
}

.el-footer {
  background-color: #f2f2f2;
  color: #333;
  text-align: center;
  padding: 20px 0;
  font-size: 14px;
  border-top: 1px solid #e0e0e0;
}

</style>