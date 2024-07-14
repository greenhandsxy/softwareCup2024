<template>
  <div>
    <video ref="video" width="640" height="480" autoplay></video><br>
    <el-button @click="startCamera">打开摄像头</el-button><br>
    <el-button @click="takeSnapshot">拍摄照片</el-button><br>
    <el-button type="primary" @click="changeAvater">确认更改头像</el-button><br>
    <img v-if="imgUrl" :src="imgUrl">
  </div>
</template>

<script>

import axios from 'axios'; // 确保已经安装并导入axios
import { toast } from "../utils/popup"
import api from "../api"
import {mapActions} from "vuex";
import path  from "@/api/path"


export default {
  name: "Camera",
  data() {
    return {
      stream: null,
      displayedImageUrl: '', // 新增一个数据属性用于存放要显示的图片URL
      imgUrl: '',
    };
  },

  methods: {
    ...mapActions([
      'updateAvatarLocal',
    ]),
    async startCamera() {
      try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const cameraAvailable = devices.some(device => device.kind === 'videoinput');

        if (!cameraAvailable) {
          toast("无摄像头硬件！", "error");
        } else {
          this.stream = await navigator.mediaDevices.getUserMedia({ video: true });
          const video = this.$refs.video;
          video.srcObject = this.stream;
        }
      } catch (error) {
        if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
          // 用户拒绝访问摄像头
          toast("您已拒绝访问摄像头权限", "error");
        } else {
          // 其他错误，例如摄像头忙或硬件问题
          toast("无法访问摄像头，请检查设置", "error");
          setTimeout(async () => {
            toast("请在浏览器网址输入：chrome://flags/#unsafely-treat-insecure-origin-as-secure", "warning");
          }, 500);
          setTimeout(async () => {
            toast("在第一个高亮输入框中输入：http://tools.elearninghome.cn:8887", "warning");
          }, 1000); // 增加延迟以分开显示提示
          setTimeout(async () => {
            toast("重启浏览器后重试", "warning");
          }, 1500); // 增加延迟以分开显示提示
        }
      }
    },
    stopCamera() {
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop());
        this.stream = null;
      }
    },
    takeSnapshot() {
      if (this.stream) {
        const canvas = document.createElement('canvas');
        canvas.width = this.$refs.video.clientWidth;
        canvas.height = this.$refs.video.clientHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(this.$refs.video, 0, 0, canvas.width, canvas.height);
        toast('已拍摄，处理中...', 'warning')
        // 将canvas转换为Blob对象
        canvas.toBlob((blob) => {
          const formData = new FormData();
          formData.append('image', blob, `img_from_frontend.png`);

          // 假设你有一个名为uploadImage的API接口
          axios.post(path.remoteBaseUrl+'/uploadImage', formData, {
          // axios.post('http://192.168.31.85:5002/uploadImage', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }).then(response => {
            if (response.data.url != undefined){
              toast('趣味头像制作完成！')
              this.imgUrl = response.data.url;
            }else {
              toast('图片正脸不清晰，请重试！', 'warning')
            }
          }).catch(error => {
            console.error('图片上传失败:', error);
          });
        }, 'image/png');
      }else {
        toast('请先打开摄像头！', 'warning')
      }
    },
    changeAvater(){
      if(this.imgUrl != ''){
        api.updateAvatarUrl(this.imgUrl).then((response)=>{
          if(response.data.code == 200){
            toast('头像更新成功！', 'success')
            this.updateAvatarLocal(this.imgUrl)
            this.imgUrl = ''
            this.$emit('avatar-updated', true); // 触发事件并传递一个标志表示头像更新成功

          }else {
            toast('头像更新失败！', 'error')
          }
        })
        // 关闭相机对话框
        this.cameraDialog = false
      }else {
        toast('请先拍摄一张照片！', 'warning')
      }
    },
  },
  beforeDestroy() {
    this.stopCamera();
  }
};
</script>

<style scoped>

</style>