<template>
  <div>
    <el-row>
      <el-col :span="10" style="text-align: right">
        请选择PPT生成方式:
      </el-col>
      <el-col :span="14" style="text-align: left; padding-left: 20px">
        <el-select-v2
            v-model="value"
            :options="options"
            placeholder="请选择PPT生成方式"
            size="large"
            style="width: 240px"
            @change="handelChange()"
        />
      </el-col>
    </el-row>
    <br><br>
    <el-row v-if="value == 'context'">
      <el-col :span="20">
        <el-input v-model="inputText" placeholder="请输入PPT内容描述" @keyup.enter.prevent="generatePPT(inputText)"></el-input>
      </el-col>
      <el-col :span="4">
        <el-button type="primary" @click="generatePPT(inputText)" >生成PPT</el-button>
      </el-col>
    </el-row>
    <el-row v-if="value == 'list'">
      <el-col :span="20">
        <el-input v-model="inputText" placeholder="请输入PPT主题以自动生成大纲" @keyup.enter.prevent="generatePPTList(inputText)"></el-input>
      </el-col>
      <el-col :span="4">
        <el-button type="primary" @click="generatePPTList(inputText)" >生成大纲</el-button>
      </el-col>
    </el-row>
    <br>
    <div v-if="PPTList">
      <p >生成的PPT大纲如下，可根据需要进行更改:</p>
      <textarea  style="width: 500px; height: 500px" v-model="PPTList">{{ PPTList }}</textarea>
      <br>
      <el-button type="primary" @click="generatePPT(PPTList)" >生成PPT</el-button>
      <br>
    </div>
    <div v-if="pptUrl">
      <p>PPT生成完成！点击链接预览或直接下载<br></p>
        <a :href="pptUrl" target="_blank" style="padding-right: 50px">《{{ inputText }}》PPT</a>
        <el-button type="primary" @click="downloadPPT()">下载PPT</el-button>
    </div>
  </div>
</template>

<script>
import {toast} from "@/utils/popup";
import axios from "axios";
import {ref} from 'vue'
import path  from "@/api/path"




export default {
  name: "PPTGenerate",

  setup(){
    const inputText = ref('');
    const pptUrl = ref(null)
    async function generatePPT(text) {
      pptUrl.value = ''
      toast("生成ppt中，请稍后...", "warning")
      try {
        const response = await axios.post(path.remoteBaseUrl+"/ppt", {
          pptName: "请根据以下内容生成ppt，要求ppt样式美观，展现方式多样，底色避免高对比度高饱和度的颜色：" + text
        }, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
        });
        pptUrl.value = response.data.download_url;
        toast("ppt生成完成！", "success")
      } catch (error) {
        throw error; // 重新抛出错误以便在调用处被捕获
      }
    }

    function convertNewlinesToBreaks(text) {
      if (text) {
        // 使用正则表达式全局替换\n为<br>
        return text.replace('\\n', '<br/>');
      }
      return text;
    }
    const PPTList = ref('')
    function generatePPTList(text) {
      pptUrl.value = ''
      PPTList.value = ''
      if(text == ''){
        toast("请输入PPT主题！", "error")
        return
      }
      toast("生成大纲中，请稍后...", "warning")
      axios.post(path.remoteBaseUrl+'/process_text', {
        // axios.post('http://127.0.0.1:5001/process_text/', {
        // axios.post('http://139.196.253.125:5000/process_text/', {
        text: "生成"+ text +"ppt大纲，不需要有其他任何内容，一级标题用“一，二”，二级标题用“1.1，1.2，2.3”这样，以此类推"
      }, {
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(response => {
        PPTList.value = convertNewlinesToBreaks(response.data.result);
        toast("PPT大纲生成完毕！", "success")
      });
    }

    const value = ref()
    const options = [
      {
        label: '生成PPT大纲->生成PPT',
        value: 'list'
      },
      {
        label: '对内容进行描述->生成PPT',
        value: 'context'
      },
    ];

    function handelChange(){
      pptUrl.value = ''
      inputText.value = ''
      PPTList.value = ''
    }

    async function downloadPPT() {
      try {
        // 使用fetch请求pptUrl，注意这里的处理基于pptUrl可以直接访问到文件Blob
        const response = await fetch(pptUrl.value);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // 获取Blob数据
        const blob = await response.blob();

        // 创建隐藏的可下载链接
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;

        // 设置下载的文件名，这里简单地使用"演示文稿.PPTX"作为示例
        const pptFileName = `${inputText.value.trim().replace(/ /g, '_') || '演示文稿'}.pptx`;
        a.download = pptFileName;

        // 触发点击
        document.body.appendChild(a);
        a.click();

        // 清理
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        toast("PPT下载开始，请留意浏览器下载提示。", "success");
      } catch (error) {
        toast("下载PPT时发生错误，请重试。", "error");
      }
    }

    return {
      generatePPT,
      pptUrl,
      inputText,
      value,
      options,
      generatePPTList,
      PPTList,
      handelChange,
      downloadPPT
    }
  }
}
</script>

<style scoped>

</style>