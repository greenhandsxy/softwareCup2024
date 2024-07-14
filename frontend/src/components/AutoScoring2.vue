<template>
  <el-upload
      class="upload-demo"
      drag
      action="http://a929594m76.zicp.fun/ocr"
      multiple
      :before-upload="beforeImageUpload"
      :on-success="handleSuccess"
      :on-fail="handleError"
      accept=".jpg,.png"
  >
    <el-icon class="el-icon--upload">
      <upload-filled />
    </el-icon>
    <div class="el-upload__text">
      将文件拖到此处，或<em>点击上传</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        只能上传jpg/png的图片文件
      </div>
    </template>
  </el-upload>
  <el-row>
    <el-col :span="8">
      <p v-if="rawImgSrc">作业图片：</p>
      <img v-if="rawImgSrc" :src="rawImgSrc" style="width: 280px;">
    </el-col>
    <el-col :span="8">
      <p v-if="text">文字识别结果：</p>
      <textarea v-if="text" style="width: 400px; height: 400px">{{ text }}</textarea>
    </el-col>
    <el-col :span="8">
      <p v-if="imageSrc">批改结果：</p>
      <img v-if="imageSrc" :src="imageSrc" alt="Uploaded Image" style="width: 280px;" />
    </el-col>

  </el-row>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { toast } from "../utils/popup"
import path  from "@/api/path"

export default {
  name: "AutoScoring2",
  setup() {
    const fileInput = ref(null);
    const imageSrc = ref('');
    const rawImgSrc = ref('')
    const text = ref(null);

    async function handleSuccess(response, file) {
      toast("文件上传成功,自动批改中，请稍后...", "warning")
      text.value = response.text;

      const reader = new FileReader(); // 直接实例化 FileReader，无需导入
      reader.onload = (e) => {
        // e.target.result 是一个包含文件内容的data URL，可以直接用于img标签的src
        rawImgSrc.value = e.target.result;
      };
      reader.readAsDataURL(file.raw); // 读取文件并转换为data URL

      let formData = new FormData();
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

    function handleError(){
      toast("文件上传失败", "error")
    }

    function beforeImageUpload(file) {
      const isImage = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/gif';
      if (!isImage) {
        toast('只能上传图片文件！', "error");
        return false; // 阻止非图片文件上传
      }
      imageSrc.value = '';
      rawImgSrc.value = '';
      text.value = '';
      return true;
    }

    return {
      fileInput,
      imageSrc,
      text,
      handleSuccess,
      rawImgSrc,
      handleError,
      beforeImageUpload
    };
  },
};
</script>

<style scoped>
/* 样式可以根据需要调整 */
</style>
