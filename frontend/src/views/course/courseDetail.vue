<template>
  <div class="container" style="background-color: aliceblue;">

    <!-- 图片需要更换 -->
    <img class="mb-5" src="../../../src/assets/course.jpg" alt="">
    <div class="containeriner">

      <p style="font-weight: bold; font-size: 2.2em;font-family: 隶书;" class="mb-4">{{ courseName }}</p>
      <p class="mr-4" style="font-family: 楷体; font-size: 2rex;">课程id:{{ courseId }}</p>
      <p class="mr-4" style="font-family: 楷体; font-size: 2rex;">课程类型：{{ courseType }}</p>
      <p class="mr-4" style="font-family: 楷体; font-size: 2rex;">授课教师/机构：{{ courseTeacherName }}</p>
    </div>


    <div class="flex items-center justify-center text-gray-400 mt-3">
      <span class="h-[0.1rem] w-50 bg-gray-400"></span>
      <span style="font-family: 隶书; font-size: 3rex;">先修要求</span>
      <span class="h-[0.1rem] w-50 bg-gray-400"></span>
    </div>
    <p style="text-align: center;font-family: 楷体; font-size: 2rex;" class="mr-30 ml-30">{{ coursePrerequisites }}</p>
    <div class="flex items-center justify-center text-gray-400 mt-3">
      <span class="h-[0.1rem] w-55 bg-gray-400"></span>
      <span style="font-family: 隶书; font-size: 3rex;">课程简介</span>
      <span class="h-[0.1rem] w-55 bg-gray-400"></span>
    </div>
    <p style="text-align: center;font-family: 楷体; font-size: 2rex; margin-left: 180px; margin-right: 180px" class="mr-30 ml-30 mb-5">{{ courseDescription }}</p>
    <div class="contanerbtn" style="margin-bottom: 2%;">
      <el-button v-if="$store.state.user.role == 2" round color="#6495ed"
                 class="w-[250px] text-white font-light hover:(bg-[#1343db] text-white) focus:(ring-8  font-semibold)"
                 type="primary" @click="handleDownload">生成课程教学PPT
      </el-button>
      <el-button v-else
                 round color="#6495ed"
                 class="w-[250px] text-white font-light hover:(bg-[#1343db] text-white) focus:(ring-8  font-semibold)"
                 type="primary" @click="selectCourse">加入我的选课
      </el-button>
      <el-button round color="#6495ed"
                 class="w-[250px] text-white font-light hover:(bg-[#1343db] text-white) focus:(ring-8  font-semibold)"
                 type="primary" @click="goBack">返回</el-button>
    </div>
    <XFBigModel :message="message"></XFBigModel>
    <div class="bestsellers-container">
      <chart-word-cloud :key="chartUpdateKey" :series="chartOptions"></chart-word-cloud>
    </div>
  </div>
</template>

<script>
import 'echarts-wordcloud';
import ChartWordCloud from '../../components/ChartWordCloud.vue'
import { useRoute, useRouter } from 'vue-router';
import { computed, onMounted, ref, reactive, nextTick } from "vue";
import api from "../../api"
import {toast} from "../../utils/popup";
import axios from 'axios';
import path  from "@/api/path"
import XFBigModel from "@/components/XFBigModel";

export default {
  name: "courseDetail",
  components: {
    ChartWordCloud,
    XFBigModel
  },

  setup() {
    const route = useRoute(); // 获取当前路由信息
    const router = useRouter();

    const courseId = ref();
    const courseDescription = ref();
    const courseType = ref();
    const coursePrerequisites = ref();
    const courseTeacherName = ref();
    const chartOptions = reactive({
      series: [
        {
          gridSize: 20,
          data: [
            {
              name: '词云生成中',
              value: 30,
              textStyle: {
                color: '#000', // 字体颜色设置为黑色
              },
            },
            { name: '词云生成中', value: 30 },
            { name: '词云生成中', value: 28 },
            { name: '词云生成中', value: 28 },
            { name: '词云生成中', value: 25 },
            { name: "词云生成中", value: 23 },
            { name: '词云生成中', value: 20 },
            { name: '词云生成中', value: 18 },
            { name: '词云生成中', value: 15 },
            { name: '词云生成中', value: 10 },
          ],
        },
      ],
    })
    const message = ref('');
    onMounted(() => {
      fetchData()
    })
    async function fetchData() {
      try {
        const response = await axios.post(
            path.remoteBaseUrl + '/process_text',
            {text: "我需要你为我介绍这门课的核心内容，要求100个字且不分段："+courseName.value},
            {headers: {'Content-Type': 'application/json'}}
        );
        message.value = response.data.result + "有疑问就来问我吧！"; // 正确设置message的值
      } catch (error) {
        // 可能需要处理错误情况，比如设置默认值或提示用户
        toast("获取数据失败，请稍后再试", "error")
      }
    }

    onMounted(() => {
      getCourseDetail()  //获取课程详细信息
      axios.post(path.remoteBaseUrl + "/word_cloud", {
        text: courseName.value
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(res => {
        chartOptions.series[0].data[0].name = res.data.ls_keyword[0];
        chartOptions.series[0].data[1].name = res.data.ls_keyword[1];
        chartOptions.series[0].data[2].name = res.data.ls_keyword[2];
        chartOptions.series[0].data[3].name = res.data.ls_keyword[3];
        chartOptions.series[0].data[4].name = res.data.ls_keyword[4];
        chartOptions.series[0].data[5].name = res.data.ls_keyword[5];
        chartOptions.series[0].data[6].name = res.data.ls_keyword[6];
        chartOptions.series[0].data[7].name = res.data.ls_keyword[7];
        chartOptions.series[0].data[8].name = res.data.ls_keyword[8];
        chartOptions.series[0].data[9].name = res.data.ls_keyword[9];
        chartUpdateKey.value = Date.now(); // 或者使用任何能表示数据已更新的变量
      })
    })

    const courseName = computed(() => route.params.courseName); // 使用computed属性获取courseName参数
    const chartUpdateKey = ref(0);

    function getCourseDetail() {
      api.getCourseDetail(courseName.value).then(res => {
        courseId.value = res.data.data.courseId;
        courseDescription.value = res.data.data.courseDescription;
        courseType.value = res.data.data.courseType;
        coursePrerequisites.value = res.data.data.prerequisites;
        courseTeacherName.value = res.data.data.teacherName;
        chartUpdateKey.value = Date.now(); // 或者使用任何能表示数据已更新的变量
      })
    };

    const goBack = () => {
      router.back();
    };

    const _nevents = ref(null);
    const _ndays_act = ref(null);
    const _nplay_video = ref(null);
    const _nchapters = ref(null);
    function selectCourse() {
      api.selectCourse(courseName.value).then(res => {
        if (res.data.data == null) {
          toast(res.data.msg, "error")
          return
        } else {
          toast("选课成功", "success")
        }
        _nevents.value = res.data.data.studyTimeSum;
        _ndays_act.value = res.data.data.studyDay;
        _nplay_video.value = res.data.data.studyTimeSum;
        _nchapters.value = res.data.data.todayStudyTime;
        predictScore(_nevents.value, _ndays_act.value, _nplay_video.value, _nchapters.value)
      })
    }
    const myScore = ref(null);
    function updateStudentPredictScore(score){
      myScore.value = Math.round(score * 100) + 50
      if (myScore.value > 100){
        myScore.value = 99
      }
      api.updateStudentPredictScore(courseName.value, myScore.value).then(res => {
      })
    }

    function predictScore(_nevents, _ndays_act, _nplay_video, _nchapters) {
      axios.post(path.remoteBaseUrl + "/score", {
        nevents: _nevents,
        ndays_act: _ndays_act,
        nplay_video: _nplay_video,
        nchapters: _nchapters
      }, {
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(res=>{
        updateStudentPredictScore(res.data.score)
      }).catch((error) => {
        toast("获取数据失败，请稍后再试", "error")
      });
    }
    function handleDownload() {
      generatePPT().then(downloadUrl => {
        if (downloadUrl) {
          toast("生成ppt完成！", "success")
          const link = document.createElement('a');
          link.href = downloadUrl;
          link.download = `《${courseName.value}》教学.pptx`; // 假设你想以课程名为文件名
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        } else {
          toast("下载链接无效！", "error")
        }
      }).catch(error => {
        toast("生成ppt失败！", "error")
      });
    }

    async function generatePPT() {
        toast("生成ppt中，请稍后...", "success")
      try {
        const response = await axios.post(path.remoteBaseUrl + "/ppt", {
          pptName: courseName.value
        }, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
        });
        return response.data.download_url; // 确保此响应包含正确的下载链接
      } catch (error) {
          toast("生成ppt失败！", "error")
      }
    }

    return {
      courseName,
      courseId,
      courseDescription,
      courseType,
      coursePrerequisites,
      courseTeacherName,
      getCourseDetail,
      goBack,
      selectCourse,
      chartOptions,
      chartUpdateKey,
      generatePPT,
      handleDownload,
      message
    };
  }
}
</script>

<style scoped lang="less">
.bestsellers-container {
  height: 18.56rem;
  width: 100%;
  background: white;
  #charts-content {
    /* 需要设置宽高后才会显示 */
    width: 100%;
    height: 100%;
  }
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.container>img {
  width: 100%;
  height: 5%;
}

.containeriner {
  display: flex;
  flex-direction: column;
  align-items: center;
  // margin-bottom: 50px;
}

.titlebar {
  display: flex;
  flex-direction: horizontal;
  align-items: center;
  // margin-bottom: 50px;
}

.containerbtn {
  display: flex;
  flex-direction: horizontal;
  align-items: center;
  margin-bottom: 50px;
}
</style>