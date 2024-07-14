<template>

  <el-table :data="myCourses.value" :border="false" stripe style="width: 100%" id="my-table">
    <el-table-column type="expand">
      <template #default="props">
        <div m="4">
          <el-table :data="props.row.studentStudyInfoList" :border="true">
            <el-table-column label="选课学生姓名" prop="studentName" />
            <el-table-column label="学生活跃天数" prop="studyDay" />
            <el-table-column label="学生视频观看数量" prop="todayStudyTime" />
            <el-table-column label="学生章节完成数" prop="studyTimeSum" />
            <el-table-column label="学生预估分数" prop="score" />
            <el-table-column label="操作" width="100">
              <template #default="innerProps">
                <el-button type="text" @click="predictStudyStatue(innerProps.row.studentName, props.row.courseName)">预测学习状态</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="开课课程名" prop="courseName" />
    <el-table-column label="选修学生人数" prop="studentNum" />
  </el-table>

  <el-button type="primary" round @click="exportClick ">导出表格</el-button>
  <div v-if="predictUrl">
    <p>学生学习状态预测图：</p>
    <img :src="predictUrl" style="width: 400px; height: 300px"/>
  </div>
</template>

<script>
import api from '../../api'
import {ref, onMounted, reactive} from 'vue'
import {mapActions} from 'vuex';
import store from "@/store";
import { toast } from "@/utils/popup";
import FileSaver from 'file-saver'
import * as XLSX from 'xlsx';
import AutoScoring from '@/components/AutoScoring'
import path  from "@/api/path"
import axios from "axios";


export default {
  name: "chosenCourses",
  components: {
    AutoScoring
  },
  methods: {
    ...mapActions(['logout']),
  },

  setup() {
    onMounted(() => {
      teaGetCourseStudyInfo()
    })

    const myCourses = reactive([{}])

    function teaGetCourseStudyInfo() {
      api.teaGetCourseStudyInfo().then(res => {
        if (res.data.code === 200) {
          myCourses.value = res.data.data
        } else {
          toast(res.data.msg, 'error')
        }
      })
    }

    const exportClick = () => {
      // 首先，我们需要构建一个新的数据结构，其中包含主表格和子表格的数据
      // 合并数据，将子表格数据转换为JSON字符串
      // 创建一个新的数据结构，包含主表格和子表格的数据
      const mergedData = [];

      myCourses.value.forEach((course) => {
        course.studentStudyInfoList.forEach((student) => {
          const newRow = {
            courseName: course.courseName,
            teacherName: store.state.user.username,
            studentName: student.studentName,
            todayStudyTime: student.studyDay,
            studyDay: student.todayStudyTime,
            studyTimeSum: student.studyTimeSum,
            score: student.score,
          };
          mergedData.push(newRow);
        });
      });

      // 创建一个新的HTML表格
      const tableElement = document.createElement('table');
      const thead = document.createElement('thead');
      const tbody = document.createElement('tbody');

      // 创建表头
      const headerRow = document.createElement('tr');
      ['开课课程名', '开课教师名', '选修学生姓名', '学生活跃天数', '学生视频观看数量', '学生章节完成数', '学生预估分数'].forEach((header) => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);

      // 创建表格行
      mergedData.forEach((row) => {
        const tr = document.createElement('tr');
        Object.keys(row).forEach((key) => {
          const td = document.createElement('td');
          td.textContent = row[key];
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });

      tableElement.appendChild(thead);
      tableElement.appendChild(tbody);

      // 将新的表格转换为工作簿
      const wb = XLSX.utils.table_to_book(tableElement);

      /* get binary string as output */
      const wbout = XLSX.write(wb, {
        bookType: 'xlsx',
        bookSST: true,
        type: 'array',
      });

      try {
        FileSaver.saveAs(new Blob([wbout], {
          type: 'application/octet-stream',
        }), store.state.user.username + '-课程数据.xlsx'); // 自定义文件名
      } catch (e) {
        toast('导出失败'+ e, 'error')
      }
    };
    const drawer = ref(false)

    const newCourseInfo = reactive({
      courseId: '',
      courseName: '',
      courseType: '',
      prerequisites: '',
      courseDescription: '',
    })

    const predictUrl = ref(null)
    function predictStudyStatue(userName, courseName){
      toast("生成预测图中，请稍后...", "warning")
      axios.post(path.remoteBaseUrl+"/transformer", {
        "will_train": false,
        "add_new": { "date": "2015/12/17", "open": Math.floor(Math.random() * (4000 - 2000 + 1)) + 3000},
        "mode": 1,
        "courseName": courseName,
        "userName": userName
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(response => {
        predictUrl.value = response.data[1].url
        toast("生成预测图完成！", "success")
      })
    }

    return {
      teaGetCourseStudyInfo,
      myCourses,
      exportClick,
      drawer,
      newCourseInfo,
      predictStudyStatue,
      predictUrl,
    }
  }
}
</script>

<style scoped>

</style>