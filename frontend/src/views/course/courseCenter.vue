<template>
  <el-carousel height="350px">
    <el-carousel-item v-for="item in images" :key="item.id" style="height: 100%;">
      <img :src="item.src" alt="" style="height: 100%;"/>
    </el-carousel-item>
  </el-carousel>
  <br>
  <div class="vertical-tabs-container">
    <el-tabs
        v-model="activeName"
        type="card"
        class="demo-tabs"
        @tab-click="handleClick"
    >
      <el-tab-pane label="全部" name="all">
        <ul class="course-grid">
          <li v-for="(course, index) in courses" :key="course.id" class="course-item">
            <img src="../../../src/assets/courses/3.png" height="100" width="120">
            <router-link :to="{ name: 'courseDetail', params: { courseName: course.courseName }}">
                      <span text="sm">
                        {{ course.courseName }}
                      </span>
            </router-link>
          </li>
        </ul>
      </el-tab-pane>
      <el-tab-pane v-for="category in courseTypes.value" :key="category.num" :label="category.type" :name="category.type" >
        <ul class="course-grid">
          <li v-for="course in courses" :key="course.id" class="course-item">
            <img src="../../../src/assets/courseLogo.jpg" height="100" width="120">
            <router-link :to="{ name: 'courseDetail', params: { courseName: course.courseName }}">
              <span>{{ course.courseName }}</span>
            </router-link>
          </li>
        </ul>
      </el-tab-pane>

    </el-tabs>
  </div>
  <div class="pagination-container">
    <el-pagination
        background
        @current-change="handlePageChange"
        :current-page="currentPage"
        :page-size="pageSize"
        layout="prev, pager, next"
        :total="total"
    />
  </div>

</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import api from '../../../src/api'
//引入指示器
import { Pagination } from 'swiper';
import 'swiper/css/pagination';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import { mapActions, mapGetters } from 'vuex';
import image from '@/assets/logo.png'
import teamImg from '@/assets/teamIntroduction.png'
import aiImg from '@/assets/aiImg.png'
import {ChatLineRound, DataLine} from "@element-plus/icons-vue";

export default {
  name: "courseCenter",
  components: {
    ChatLineRound,
    DataLine,
    Swiper,
    SwiperSlide
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'getUsername']),
  },
  methods: {
    ...mapActions(['logout']),
  },
  data() {
    return {
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
    const images = ref([
      {id: 1, src: image},
      {id: 2, src: teamImg},
      {id: 3, src: aiImg},
    ]);

    onMounted(() => {
      loadCourses(currType);
      loadCourseType();
    });


    // 加载课程数据
    const loadCourses = () => {
      api.getCourses({pageNum: currentPage.value, pageSize: pageSize.value}, currType.value)
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

    //修改类别
    const changeType = (type) => {
      currType.value = type;
    }


    const activeName = ref('all')

    const handleClick = (tab, event) => {
      if (tab.props.name == "all") {
        changeType("")
      } else {
        changeType(tab.props.name)
      }
      loadCourses(currType)
    };

    function getCssVarName(type) {
      return `--el-box-shadow${type ? '-' + type : ''}`;
    };

    return {
      value,
      courses,
      currentPage,
      pageSize,
      total,
      handlePageChange,
      activeName,
      handleClick,
      courseTypes,
      changeType,
      getCssVarName,
      images
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
  background: #FAFBFE;
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
</style>