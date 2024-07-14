<template>
  <!-- 在你的模板中添加一个文件输入元素 -->
  <input type="file" @change="handleFileChange" ref="avatarInput" style="display:none">
  <el-row>
    <el-col >
    <div class="demo-image__preview">
      <el-image
          style="width: 100px; height: 100px"
          :src="imgUrl"
          :zoom-rate="1.2"
          :max-scale="7"
          :min-scale="0.2"
          :preview-src-list="imgUrlList"
          :initial-index="4"
          fit="cover"
      />
    </div>
    </el-col>
    <el-col >
  <el-button @click="$refs.avatarInput.click()">更新头像</el-button>

    </el-col>
  </el-row>
</template>

<script>
import api from "../api"
import { toast } from "../utils/popup"
import { mapActions } from 'vuex';
import store from "@/store";
import defaultImg from "@/assets/default.png";
import Camera from "@/components/Camera";
import { mapState } from 'vuex';


export default {
  name: "uploadAvatar",
  components: {Camera},
  data() {
    return {
      imgUrl: store.state.user.avatar == null ? defaultImg : store.state.user.avatar,
      imgUrlList: [store.state.user.avatar],
    }
  },
  computed: {
    ...mapState(['user']),
  },
  watch: {
    'user.avatar': {
      handler(newValue) {
        this.imgUrl = newValue;
        this.imgUrlList = [newValue];
      },
    }
  },
  methods: {
    handleFileChange(e) {
      const file = e.target.files[0];
      if (file) {
        this.uploadAvatar(file);
      }
    },
    ...mapActions([
      'updateAvatarLocal',
    ]),
    async uploadAvatar(file) {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("token", localStorage.getItem("access_token"));

      try {
        api.uploadAvatar(formData).then((response)=>{
          if(response.data.code == 200){
            toast("上传成功", "success")
            this.imgUrl = response.data.data
            this.imgUrlList[0] = response.data.data
            this.updateAvatarLocal(response.data.data)
          }else{
            toast("上传失败", "error")
          }
        })
      } catch (error) {
        // 处理错误，例如显示错误信息
        toast("上传失败", "error")
      }
    },
  },
};
</script>
<style scoped>
.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
.demo-image__error .image-slot {
  font-size: 30px;
}
.demo-image__error .image-slot .el-icon {
  font-size: 30px;
}
.demo-image__error .el-image {
  width: 100%;
  height: 200px;
}
</style>