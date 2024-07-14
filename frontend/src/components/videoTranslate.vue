<template>
  <div>
    <el-row>
      <el-col :span="10" style="text-align: right">
        请选择语音上传方式:
      </el-col>
      <el-col :span="14" style="text-align: left; padding-left: 20px">
        <el-select-v2
            v-model="value"
            :options="options"
            placeholder="请选择语音上传方式"
            size="large"
            style="width: 240px"
            @change="result = ''"
        />
      </el-col>
    </el-row>
    <br><br>
    <el-upload
        v-if="value == 'file'"
        class="upload-demo"
        drag
        action="http://a929594m76.zicp.fun/voice"
        multiple
        :before-upload="beforeImageUpload"
        :on-success="handleSuccess"
        :on-fail="handleError"
        accept="audio/mpeg, audio/wav,audio/x-wav"
    >
      <el-icon class="el-icon--upload">
        <upload-filled />
      </el-icon>
      <div class="el-upload__text">
        将文件拖到此处，或<em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          只能上传mp3/mav音频文件
        </div>
      </template>
    </el-upload>
    <el-divider v-if="value == 'file'"></el-divider>
    <talkModel
        v-if="value == 'video'"
        msg="videoTranslate"
        @getVideoMsg="getMsg">
    </talkModel>
    <p v-if="result">语音翻译结果为：<br>{{ result }}</p>

  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { toast } from "../utils/popup"
import path  from "@/api/path"
import talkModel from "@/components/talkModel";

export default {
  name: "videoTranslate",
  components: {talkModel},

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

    const uploadFile = async () => {
      const formData = new FormData();
      if (!fileInput.value.files.length) {
        toast("请选择文件", "error")
        return;
      }
      formData.append("file", fileInput.value.files[0]);
      toast("音频处理中，请稍后...", "warning")
      try {
        // const responseFromServer = await axios.post('http://127.0.0.1:5000/voice', formData, {
        const responseFromServer = await axios.post(path.remoteBaseUrl +'/voice', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        result.value = responseFromServer.data.message;
        toast("音频翻译完成！", "success")
      } catch (error) {
        if (error.response) {
          toast("文件上传失败:"+`${error.response.statusText}`, "error")
          response.value = `文件上传失败: ${error.response.statusText}`;
        }
      }
    };

    function beforeImageUpload(file) {
      const isVideo = file.type === 'audio/mpeg' || file.type === 'audio/wav' || file.type === 'audio/x-wav';
      if (!isVideo) {
        toast('只能上传音频文件！', "error");
        return false; // 阻止非音频文件上传
      }
      toast("音频处理中，请稍后...", "warning")
      return true;
    }

    function handleSuccess(res) {
      toast("音频翻译完成！", "success")
      result.value = res.message;
    }
    function handleError(){
      toast("文件上传失败", "error")
    }
    function getMsg(chileMsg){
      result.value = chileMsg;
    }
    const value = ref()
    const options = [
      {
        label: '文件上传',
        value: 'file'
      },
      {
        label: '语音录制上传',
        value: 'video'
      },
      ]

    return {
      fileInput,
      response,
      handleFileChange,
      uploadFile,
      result,
      beforeImageUpload,
      handleSuccess,
      handleError,
      getMsg,
      options,
      value
    };
  },
}
</script>

<style scoped>

</style>