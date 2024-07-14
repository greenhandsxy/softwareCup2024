<template>
  <el-table :data="myCourses" stripe style="width: 100%">
    <el-table-column label="课程ID" prop="courseId" />
    <el-table-column label="课程名称">
      <template #default="{ row }">
        <router-link :to="{ name: 'courseDetail', params: { courseName: row.courseName }}">
          {{ row.courseName }}
        </router-link>
      </template>
    </el-table-column>
    <el-table-column label="课程类型" prop="courseType" />
    <el-table-column label="先修要求" prop="prerequisites" />
    <el-table-column label="课程简介" prop="courseDescription">
      <template #default="{ row }">
        <div class="description-cell">{{ row.courseDescription }}</div>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="150">
      <template #default="{ row }">
        <el-button size="small" @click="handlePredict(row.courseName)">课程热度预测</el-button>
        <br>
        <el-button size="small" @click="handleDownload(row.courseName)">生成教学ppt</el-button>
      </template>
    </el-table-column>
  </el-table>
  <br>
  <el-button type="primary" @click="drawer = true">去开课</el-button>
  <div v-if="predictUrl">
    <p>课程热度预测图：</p>
    <img :src=predictUrl style="height: 300px; width: 400px"/>
  </div>

  <el-dialog v-model="drawer" size = '100%' direction='btt'
             :before-close="handleClose">

    <div
        title="发布新课程"
        width="600px"
        @close="handleClose"
    >
      <el-form
          :model="newCourseInfo"
          :rules="rules"
          :label-position="labelPosition"
          label-width="auto"
          ref="newCourseFormRef"
      >
        <el-form-item label="课程ID" prop="courseId">
          <el-input v-model="newCourseInfo.courseId" />
        </el-form-item>
        <el-form-item label="课程名" prop="courseName">
          <el-input v-model="newCourseInfo.courseName" />
        </el-form-item>
        <el-form-item label="课程类型" prop="courseType">
          <el-input v-model="newCourseInfo.courseType" />
        </el-form-item>
        <el-form-item label="先修课程" prop="prerequisites">
          <el-input v-model="newCourseInfo.prerequisites" />
        </el-form-item>
        <el-form-item label="课程描述" prop="courseDescription">
          <el-input v-model="newCourseInfo.courseDescription" />
        </el-form-item>
        <el-form-item>
      <span slot="footer" class="dialog-footer">
        <el-button @click="drawer = false">取 消</el-button>
        <el-button type="primary" @click="teaReleaseCourse">确 定</el-button>
      </span>
        </el-form-item>
      </el-form>
    </div>
  </el-dialog>
</template>

<script>
import {ref, onMounted, reactive} from 'vue';
import api from '../../api';
import {ElMessageBox} from "element-plus";
import {toast} from "@/utils/popup";
import axios from "axios";
import path  from "@/api/path"

export default {
  name: "MyCourses",
  setup() {
    const myCourses = ref([]);

    const fetchCourses = () => {
      api.teaGetCourses().then(res => {
        myCourses.value = res.data.data;
      });
    };

    onMounted(fetchCourses);

    const drawer = ref(false)

    const handleClose = (done) => {
      ElMessageBox.confirm('确定要取消开课？')
          .then(() => {
            done()
            userInfoFormRef.value.resetFields(); // 清空表单字段
          })
          .catch(() => {
            // catch error
          })
    }

    const newCourseInfo = reactive({
      courseId: '',
      courseName: '',
      courseType: '',
      prerequisites: '',
      courseDescription: '',
    })
    const rules = {
      courseId: [
        {required: true, message: "课程ID不能为空", trigger: "blur"},
      ],
      courseName: [
        {required: true, message: "课程名不能为空", trigger: "blur"},
        {min: 2, max: 20, message: "课程名长度必须是2-20个字符", trigger: "blur"},
      ],
      courseType: [
        {required: true, message: "课程类型不能为空", trigger: "blur"},
      ],
      prerequisites: [
        {required: true, message: "先修课程描述不能为空", trigger: "blur"},
      ],
      courseDescription: [
        {required: true, message: "课程描述不能为空", trigger: "blur"},
      ],
    };

    const newCourseFormRef = ref(null);

    function teaReleaseCourse() {
      newCourseFormRef.value.validate((valid) => {
        if (valid) {
          drawer.value = false
          api.teaReleaseCourse(newCourseInfo).then(res => {
            if (res.data.code === 200) {
              toast("课程已发布成功，快让学生来选课吧！", 'success')
              fetchCourses()
            } else {
              toast(res.data.msg, 'error')
            }
          })
        } else {
          toast("表单有误", "error");
        }
      })
    }

    function handleDownload(courseName) {
      generatePPT(courseName).then(downloadUrl => {
        if (downloadUrl) {
          toast("生成ppt完成！", "success")
          const link = document.createElement('a');
          link.href = downloadUrl;
          link.download = courseName + `教学.pptx`; // 假设你想以课程名为文件名
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

    async function generatePPT(courseName) {
      toast("生成ppt中，请稍后...", "success")
      try {
        const response = await axios.post(path.remoteBaseUrl+"/ppt", {
          pptName: "请根据以下内容生成ppt，要求ppt样式美观，展现方式多样，底色避免高对比度高饱和度的颜色：" + courseName
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

    const predictUrl = ref(null)
    function handlePredict(courseName){
      toast("生成预测图中，请稍后...", "warning")
      axios.post(path.remoteBaseUrl+"/transformer", {
        "will_train": false,
        "add_new": { "date": "2015/12/17", "open": Math.floor(Math.random() * (4000 - 2000 + 1)) + 3000
        },
        "mode": 0,
        "courseName": courseName,
        "userName": "666"
      }, {
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(res => {
        predictUrl.value = res.data[1].url
        toast("生成预测图完成！", "success")
      })
    }

    return {
      myCourses,
      drawer,
      handleClose,
      newCourseInfo,
      rules,
      newCourseFormRef,
      teaReleaseCourse,
      handleDownload,
      handlePredict,
      predictUrl,

    };
  }
};
</script>

<style scoped>
.description-cell {
  max-height: 80px;
  overflow: auto;
}
</style>
