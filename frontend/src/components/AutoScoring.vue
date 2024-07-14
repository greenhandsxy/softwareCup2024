<template>
  <div>
    <label for="fileInput">请选择文件</label>
    <input type="file" id="fileInput" ref="fileInput" @change="handleFileChange" />
    <el-button @click="uploadFile" >上传文件</el-button>
    <br>
    <el-row>
      <el-col :span="12">
      <p v-if="text">文字识别结果：</p>
      <textarea v-if="text" style="width: 400px; height: 400px">{{ text }}</textarea>
      </el-col>
      <el-col :span="12">
      <br><br>
    <img v-if="imageSrc" :src="imageSrc" alt="Uploaded Image" style="width: 280px;" />
    <div v-if="response">{{ response }}</div>
      </el-col>

    </el-row>
  </div>

  <el-upload
      class="upload-demo"
      drag
      action=""
      multiple
      @Change="fileChangee"
  >
    <el-icon class="el-icon--upload">
      <upload-filled />
    </el-icon>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        jpg/png files with a size less than 500kb
      </div>
    </template>
  </el-upload>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { toast } from "../utils/popup"
import path  from "@/api/path"
import { UploadFilled } from '@element-plus/icons-vue'


export default {
  name: "AutoScoring",
  setup() {
    const fileInput = ref(null);
    const response = ref('');
    const imageSrc = ref('');

    const handleFileChange = () => {
      // 确保选择了文件
      if (!fileInput.value.files.length) {
        alert("请选择文件");
        return;
      }
    };

    const text = ref(null);
    let fileContext = ref(null);
    const uploadFile = async () => {
      if (!fileInput.value.files.length) {
        toast("请选择文件", "error");
        return;
      }
      fileContext = fileInput.value.files[0]
      let formData = new FormData();

      // 重新初始化formData
      formData.append("file", fileContext);
        try {
          toast("文字识别中，请稍后...", "warning");
          const responseFromOCR = await axios.post(path.remoteBaseUrl + '/ocr', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          toast("文字识别完成！", "success");
          console.log(responseFromOCR.data.text);
          text.value = responseFromOCR.data.text;
        } catch (error) {
          if (error.response) {
            toast("文件上传失败:" + `${error.response.statusText}`, "error");
            response.value = `文件上传失败: ${error.response.statusText}`;
          }
        }
      setTimeout(async () => {
        toast("图片处理中，请稍后...", "warning");

      }, 500)
      formData = new FormData();
      formData.append("file", fileContext);
      try {
        // const responseFromUpload = await axios.post('http://127.0.0.1:5002/model_upload/', formData, {
        const responseFromUpload = await axios.post(path.remoteBaseUrl+'/autocheck', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        const parser = new DOMParser();
        const htmlDoc = parser.parseFromString(responseFromUpload.data, 'text/html');
        const imgElement = htmlDoc.querySelector('img'); // 获取第一个img标签

        if (imgElement) {
          imageSrc.value = imgElement.src; // 设置img src值
          response.value = "批改完成！";
          toast("作业批改完成！", "success");
        } else if (responseFromUpload.data.message) {
          response.value = responseFromUpload.data.message;
        } else {
          response.value = "文件上传成功，但未找到图像";
          toast("文件上传成功，但未找到图像", "error");
        }
      } catch (error) {
        if (error.response) {
          toast("文件上传失败:" + `${error.response.statusText}`, "error");
          response.value = `文件上传失败: ${error.response.statusText}`;
        }
        return; // 遇到错误时，不进行第二次请求
      }

    };


    onMounted(() => {
      // 初始化逻辑可以放在这里，但在这个场景中可能不需要
    });

    const files = ref([]);
    async function fileChangee(file) {
      console.log('当前上传的文件：', file);
      // files.value.push(file);
      console.log('当前所有上传的文件：', files.value);

      let formData = new FormData();

      // 重新初始化formData
      formData.append("file", file.raw);
      try {
        toast("文字识别中，请稍后...", "warning");
        const responseFromOCR = await axios.post(path.remoteBaseUrl + '/ocr', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        toast("文字识别完成！", "success");
        console.log(responseFromOCR.data.text);
        text.value = responseFromOCR.data.text;
      } catch (error) {
        if (error.response) {
          toast("文件上传失败:" + `${error.response.statusText}`, "error");
          response.value = `文件上传失败: ${error.response.statusText}`;
        }
      }
      setTimeout(async () => {
        toast("图片处理中，请稍后...", "warning");

      }, 500)
      formData = new FormData();
      formData.append("file", file.raw);
      try {
        // const responseFromUpload = await axios.post('http://127.0.0.1:5002/model_upload/', formData, {
        const responseFromUpload = await axios.post(path.remoteBaseUrl + '/autocheck', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        const parser = new DOMParser();
        const htmlDoc = parser.parseFromString(responseFromUpload.data, 'text/html');
        const imgElement = htmlDoc.querySelector('img'); // 获取第一个img标签

        if (imgElement) {
          imageSrc.value = imgElement.src; // 设置img src值
          response.value = "批改完成！";
          toast("作业批改完成！", "success");
        } else if (responseFromUpload.data.message) {
          response.value = responseFromUpload.data.message;
        } else {
          response.value = "文件上传成功，但未找到图像";
          toast("文件上传成功，但未找到图像", "error");
        }
      } catch (error) {
        if (error.response) {
          toast("文件上传失败:" + `${error.response.statusText}`, "error");
          response.value = `文件上传失败: ${error.response.statusText}`;
        }
        return; // 遇到错误时，不进行第二次请求
      }
    }


    return {
      fileInput,
      response,
      imageSrc,
      handleFileChange,
      uploadFile,
      text,
      fileChangee
    };
  },
};
</script>

<style scoped>
/* 样式可以根据需要调整 */
</style>
