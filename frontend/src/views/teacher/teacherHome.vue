<template>
  <div class="common-layout">
    <el-container>
      <el-header :class="{ dynamicTitle: true }">
        <div class="header-content">
          <img src="../../assets/logo.png" alt="logo" class="logo" width="110" height="55" style="margin-left: 50px">
          <h3 v-text="currentHeader"></h3>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <router-link @click.prevent="changeHeader('我的信息')" to="/teacherInfo">
          <el-avatar  :size="large" :src="AvatarUrl" style="width: 100px; height: 100px"/>
          </router-link>
          <p class="mb-2">你好：{{ $store.state.user.username }} 老师</p> <el-button @click="logout">退出登录</el-button>
            <XFBigModel :message="message"></XFBigModel>
          <el-col :span="24">
            <el-menu
                default-active="2"
                class="el-menu-vertical-demo"
                @open="handleOpen"
            >
              <router-link @click.prevent="changeHeader('我的信息')" to="/teacherInfo">
                <el-menu-item index="1" @click="message = '听说制作趣味头像还挺有趣的，快去试试吧！'">
                  <el-icon><UserFilled /></el-icon>
                  <span>
                  <p>
                      我的信息
                  </p>
                </span>
                </el-menu-item>
              </router-link>

              <router-link @click.prevent="changeHeader('开设课程')" to="/teacherCourse">
                <el-menu-item index="2" @click="message = '点击表格右边操作中的按钮，让我来发挥我的AI功能吧！'">
                  <el-icon><Menu /></el-icon>
                  <span>
                  <p>
                      我的开设课程
                  </p>
                </span>
                </el-menu-item>
              </router-link>
              <router-link  @click.prevent="changeHeader('选课学生情况')" to="/chosenCourses">
                <el-menu-item  index="3" @click="message = '一键导出学习情况，看看有没有吊车尾的同学吧！'">
                  <el-icon><Document /></el-icon>
                  <span>
                  <p>
                    选课学生情况
                  </p>
                </span>
                </el-menu-item>
              </router-link>
              <router-link  @click.prevent="changeHeader('自动批改')" to="/autoScoring">
                <el-menu-item  index="4" @click="message = '上传作业图片，让我来完成作业批改吧！'">
                  <el-icon><Collection /></el-icon>
                  <span>
            <p>
                作业自动批改
            </p>
                </span>
                </el-menu-item>
              </router-link>

              <el-sub-menu index="5" @click="message = 'AI工具，让教学更高效、更轻松！'">
                <template #title>
                  <el-icon><Box /></el-icon>
                  <span>AI助教工具</span>
                </template>
                <el-menu-item index="1-1" @click="showTranslate = true"><el-icon><Switch /></el-icon>英汉翻译</el-menu-item>
                <el-menu-item index="1-2" @click="showVideoTranslate = true"><el-icon><Mic /></el-icon>语音翻译</el-menu-item>
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
                  Latex公式工具
                </el-menu-item>
              </el-sub-menu>
            </el-menu>
          </el-col>
        </el-aside>
        <el-container>
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
                Latex公式工具
              </div>
            </template>
            <LatexService></LatexService>
          </el-drawer>
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
import {ref, onMounted, watchEffect} from 'vue'
import {mapActions} from 'vuex';
import store from "@/store";
import AutoScoring from '@/components/AutoScoring'
import XFBigModel from '@/components/XFBigModel'
import defaultImg from "@/assets/default.png"
import translate from "@/components/translate"
import videoTranslate from "@/components/videoTranslate"
import OCR from "@/components/OCR"
import PPTGenerate from "@/components/PPTGenerate";
import LatexService from "@/components/LatexService";



export default {
  name: "teacherHome",
  components: {
    AutoScoring,
    XFBigModel,
    translate,
    videoTranslate,
    OCR,
    PPTGenerate,
    LatexService
  },

  beforeRouteEnter(to, from, next) {
    next(vm => {
      // 在这里，vm指的是组件实例
      vm.$router.push({ name: 'teacherCourse' }); // 这将激活选课中心链接
    });
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
  data() {
    return {
      currentHeader: "开设课程", // 初始标题
    }
  },

  setup(){
    const AvatarUrl = ref("");
    const message = ref("")
    onMounted(() => {
      message.value = "老师您好，我是您的智能助教，有什么问题快来向我提问吧！"
      AvatarUrl.value = store.state.user.avatar == null ? defaultImg : store.state.user.avatar;
    })

    watchEffect(async () => {
      AvatarUrl.value = store.state.user.avatar || defaultImg;
    });

    const drawer = ref(false)
    const showTranslate = ref(false)
    const showVideoTranslate  =ref(false)
    const showPPTGenerate = ref(false)
    const showOCR = ref(false)
    const showLatex = ref(false)

    return{
      drawer,
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
.el-aside {
  background-image: linear-gradient(to top, #6495ed, #ffffff);
  /* 更改颜色以适应你的设计需求 */
  height: 100vh;
}
.el-header {
  background-image: linear-gradient(to left, #6495ed, #ffffff);
  height: 100px;
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