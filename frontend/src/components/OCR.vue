<template>
  <div>
    <el-upload
        class="upload-demo"
        drag
        action="http://9iq1vp362785.vicp.fun:80/ocr"
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
    <el-divider></el-divider>
    <p v-if="text">文字识别结果为：<br></p>
    <textarea v-if="text" style="width: 400px; height: 400px">{{ text }}</textarea>

  </div>
</template>

<script>
import {ref} from "vue";
import {toast} from "@/utils/popup";
import axios from "axios";
import path  from "@/api/path"

export default {
  name: "OCR",
  setup() {
    const fileInput = ref(null);
    const response = ref('');
    const result = ref('');

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
    toast("图片处理中，请稍后...", "warning");
    try {
      const responseFromOCR = await axios.post(path.remoteBaseUrl+'/ocr', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      text.value = responseFromOCR.data.text;
      toast("文字识别完成！", "success");
    } catch (error) {
      if (error.response) {
        toast("文件上传失败:" + `${error.response.statusText}`, "error");
        response.value = `文件上传失败: ${error.response.statusText}`;
      }
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
      toast("图片处理中，请稍后...", "warning")
      return true;
    }
    function handleSuccess(res) {
      toast("文字识别完成！", "success");
      text.value = res.text;
    }

  return {
    uploadFile,
    text,
    fileInput,
    handleFileChange,
    result,
    response,
    handleError,
    beforeImageUpload,
    handleSuccess
  }

}

}
</script>

<style scoped>

</style>