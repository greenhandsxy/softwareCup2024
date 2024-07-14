<template>
    <el-dialog v-model="drawer" size="50%" direction="btt" :before-close="handleClose">
      <div
          title="修改个人信息"
          :visible.sync="dialogVisible"
          width="200px"
          @close="handleClose"
      >
        <el-form
            :model="userUpdateInfo"
            :rules="rules"
            :label-position="labelPosition"
            label-width="auto"
            ref="userInfoFormRef"
        >
          <el-form-item label="昵称" prop="nickname">
            <el-input v-model="userUpdateInfo.nickname" />
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="userUpdateInfo.email" />
          </el-form-item>
          <el-form-item label="手机" prop="phone">
            <el-input v-model="userUpdateInfo.phone" />
          </el-form-item>
          <el-form-item>
            <span slot="footer" class="dialog-footer">
              <el-button @click="drawer = false">取 消</el-button>
              <el-button type="primary" @click="submitForm">确 定</el-button>
            </span>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>

  <el-dialog v-model="cameraDialog" size="50%" :before-close="handleClose" style="width: 700px">
    <div
        title="制作趣味头像"
        width="150px"
        @close="handleClose"
    >
      <camera  @avatar-updated="onAvatarUpdated"></camera>
    </div>
  </el-dialog>

  <el-descriptions
      class="margin-top"
      :column="2"
      size="large"
      border
  >
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <user />
          </el-icon>
          用户名
        </div>
      </template>
      {{ $store.state.user.username }}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <user />
          </el-icon>
          昵称
        </div>
      </template>
      {{ $store.state.user.nickname }}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <Female />
          </el-icon>
          性别
        </div>
      </template>
      <el-tag size="small">{{ $store.state.user.gender }}</el-tag>
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <iphone />
          </el-icon>
          联系方式
        </div>
      </template>
      {{ $store.state.user.phone }}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <ChatLineRound />
          </el-icon>
          电子邮箱
        </div>
      </template>
      {{ $store.state.user.email }}
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <tickets />
          </el-icon>
          用户身份
        </div>
      </template>
      <el-tag size="small">{{ userRole }}</el-tag>
    </el-descriptions-item>
    <el-descriptions-item>
      <template #label>
        <div class="cell-item">
          <el-icon :style="iconStyle">
            <Avatar />
          </el-icon>
          用户头像
        </div>
      </template>
      <uploadAvatar></uploadAvatar>
      <el-button  @click="cameraDialog = true">制作趣味头像</el-button>
    </el-descriptions-item>
  </el-descriptions>
  <br>
    <el-button type="primary" @click="drawer = true">修改个人信息</el-button>


</template>


<script>

import api from '../../api'
import { ref, onMounted, reactive } from 'vue'
import {ElMessageBox} from "element-plus";
import store from "@/store";
import { toast, showModal } from "@/utils/popup";
import courseVideo from "@/components/courseVideo";
import defaultImg from "@/assets/default.png";
import uploadAvatar from "@/components/uploadAvatar"
import {Avatar} from "@element-plus/icons-vue";
import Camera from "@/components/Camera";



export default {
  name: "studentHome",
  components: {Camera, Avatar, courseVideo,uploadAvatar },

  data() {
    return {
      dialogVisible: true, // 控制对话框的显示与隐藏
      labelPosition: 'right',
    };
  },

  setup() {
    const drawer = ref(false)
    const cameraDialog = ref(false)

    const username = store.getters.getUsername

    const userUpdateInfo = reactive({
      username: username,
      email: '',
      phone: '',
      nickname: '',
    })

    const rules = {
      nickname: [
        { required: true, message: "昵称不能为空", trigger: "blur" },
        { min: 6, max: 20, message: "昵称长度必须是6-20个字符", trigger: "blur" },
      ],
      email: [
        { required: true, message: "邮箱不能为空", trigger: "blur" },
        { type: "email", message: "请输入正确的邮箱地址", trigger: ["blur", "change"] },
      ],
      phone: [
        { required: true, message: "手机不能为空", trigger: "blur" },
        {
          pattern: /^1[3-9]\d{9}$/,
          message: "请输入正确的手机号码",
          trigger: "blur",
        },
      ],
    };

    const userRole = ref();
    onMounted(() => {
      userRole.value = store.state.user.role == 1 ? '学生' : '教师';
    })

    const handleClose = (done) => {
      ElMessageBox.confirm('确定要取消更改？')
          .then(() => {
            done()
            userInfoFormRef.value.resetFields(); // 清空表单字段
          })
          .catch(() => {
          })
    }

    const userInfoFormRef = ref(null) // 表单引用

    function submitForm() {
      // 提交表单的逻辑，这里简单打印表单数据，实际应提交至后端
      userInfoFormRef.value.validate(valid => {
        if (valid) {
          // 表单验证通过，执行提交逻辑
          // 这里可以调用API更新用户信息，并处理响应
          api.updateUserInfo(userUpdateInfo).then((res) => {
            store.dispatch("updateUserInStore", res.data.data)
          })
          toast('信息修改成功！', 'success');
          drawer.value = false; // 提交成功后关闭对话框
        } else {
          toast("表单有误", "error");
        }
      });
    }

    const AvatarUrl = store.state.user.avatar == null ? defaultImg : store.state.user.avatar;

    function onAvatarUpdated(updated){
      if(updated){
        cameraDialog.value = false
      }
    }


    return {
      drawer,
      handleClose,
      userUpdateInfo,
      rules,
      submitForm,
      userInfoFormRef,
      AvatarUrl,
      userRole,
      cameraDialog,
      onAvatarUpdated,
    }
  }
}
</script>

<style scoped>
.my-info {
  text-align: center;
  font-weight: bold;
  margin-bottom: 20px;
}

.info-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.info-label {
  font-weight: bold;
  margin-right: 10px;
}

.el-descriptions {
  margin-top: 20px;
}
.cell-item {
  display: flex;
  align-items: center;
}
.margin-top {
  margin-top: 20px;
}
</style>