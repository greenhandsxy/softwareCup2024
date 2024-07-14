<template>
  <div class="translate-page">
    <label>模式选择:</label>
    <select v-model="translationMode" @change="clear">
      <option value="en2zh">英译汉</option>
      <option value="zh2en">汉译英</option>
    </select>
    <br><br>
    <div v-if="translationMode === 'en2zh'">
      <textarea v-model="englishText" placeholder="输入英文文本"></textarea>
      <el-button @click="translate">翻译</el-button>
      <p>翻译结果:</p>
      <textarea v-model="chineseText" readonly></textarea>
    </div>

    <div v-else>
      <textarea v-model="chineseText" placeholder="输入中文文本"></textarea>
      <el-button @click="translate">翻译</el-button>
      <p>翻译结果:</p>
      <textarea v-model="englishText" readonly></textarea>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { toast } from "../utils/popup"
import path  from "@/api/path"

export default {
  name: "translate",
  data() {
    return {
      translationMode: 'en2zh', // 默认为英译汉
      englishText: '',
      chineseText: '',
    };
  },
  methods: {
    // 这里应该调用实际的翻译API，但为了示例，我们仅模拟翻译过程
    translate() {
      if (this.translationMode === 'en2zh') {
        // 实际应用中，这里会调用英译汉的API
        if (!this.englishText){
          toast("请输入英文文本！", "error")
          return;
        }
        toast("翻译中，请稍后...", "warning")
        axios.post(path.remoteBaseUrl + '/translate', {
          mode: 0,
          str: this.englishText
        }, {
          headers: {
            'Content-Type': 'application/json'
          },
        }).then(response => {
          this.chineseText = response.data.result; // 模拟翻译
          toast("翻译完成！", "success")
        })
      } else {
        // 实际应用中，这里会调用汉译英的API
        if (!this.chineseText){
          toast("请输入中文文本！", "error")
          return;
        }
        toast("翻译中，请稍后...", "warning")
        axios.post(path.remoteBaseUrl+'/translate', {
          mode: 1,
          str: this.chineseText
        }, {
          headers: {
            'Content-Type': 'application/json'
          },
        }).then(response => {
          this.englishText = response.data.result; // 模拟翻译
          toast("翻译完成！", "success")
        })
      }
    },
    clear(){
      this.englishText = '';
      this.chineseText = '';
    }
  },
}
</script>

<style scoped>
.translate-page {
  width: 100%;
  max-width: 600px;
  margin: auto;
  padding: 20px;
}
textarea {
  width: 100%;
  height: 150px;
  margin-bottom: 10px;
}
</style>