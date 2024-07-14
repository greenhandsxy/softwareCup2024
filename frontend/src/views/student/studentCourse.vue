<template>
  <el-card style="width: 100%">
    <el-table :data="myCourses.value" stripe style="width: 100%">
      <el-table-column label="课程名称" prop="courseName" />
      <el-table-column label="授课老师/单位" prop="teacherName" />
      <el-table-column label="活跃天数" prop="studyDay" />
      <el-table-column label="视频观看数量" prop="todayStudyTime" />
      <el-table-column label="章节完成数" prop="studyTimeSum" />
      <el-table-column label="预估学习得分" prop="score">
        <template #default="scope">
          <el-tag v-if="scope.row.score >= 90" size="small" type="success">
            <span>{{ scope.row.score }}，很好！继续保持！</span>
          </el-tag>
          <el-tag v-else-if="scope.row.score < 70" size="small" type="warning">
            <span>{{ scope.row.score }}，还需要加把劲哦！</span>
          </el-tag>
          <el-tag v-else size="small">
            <span>{{ scope.row.score }}，再努力一把会更棒！</span>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column align="right">
        <template #default="scope">
          <el-button
              size="small"
              @click="$router.push('/courseVideo/'+scope.row.courseName)"
          >
            去学习
          </el-button>
          <el-button
              size="small"
              type="danger"
              @click="stuDeleteCourse(scope.row.courseName)"
          >
            退选
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-button class="mt-4" style="width: 100%" @click="$router.push('/courseCenter')">
      去选课
    </el-button>
  </el-card>
</template>

<script>
import api from '../../api'
import {ref, onMounted, reactive} from 'vue'
import {ElMessageBox} from "element-plus";
import { toast, showModal } from "@/utils/popup";
import courseVideo from "@/components/courseVideo";

export default {
  name: "studentCourse",
  components: { courseVideo },

  data() {
    return {
      dialogVisible: true, // 控制对话框的显示与隐藏
      labelPosition: 'right',
    };
  },

  setup() {
    onMounted(() => {
      getCourseStudyInfo()
    })

    // 加载课程数据
    const userInfo = () => {
      api.getUserInfo()
          .then((res) => {
          });
    };

    const handleClose = (done) => {
      ElMessageBox.confirm('确定要取消更改？')
          .then(() => {
            done()
            userInfoFormRef.value.resetFields(); // 清空表单字段
          })
          .catch(() => {
            toast('出错了', 'error')
          })
    }

    const myCourses = reactive([{}])

    function getCourseStudyInfo() {
      api.getCourseStudyInfo()
          .then((res) => {
            myCourses.value = res.data.data
          })
    }

    async function stuDeleteCourse(courseName) {
      try {
        const shouldDelete = await showModal('确定删除该课程吗？', '提示', 'warning')
        if (shouldDelete) {
          api.stuDeleteCourse(courseName)
              .then((res) => {
                getCourseStudyInfo()
              })
          toast('退选课程成功', 'success')
        }
      } catch (err) {
      }
    }


    return {
      handleClose,
      myCourses,
      stuDeleteCourse,
    }
  }
}
</script>

<style scoped>

</style>