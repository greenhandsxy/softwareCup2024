<template>
  <div >
    <el-row>
      <el-col :span = "24">
        <el-text class="w-150px mb-2" truncated>
          用户注册
        </el-text>
      </el-col>
      <el-col :span = "24">
        <div class="flex items-center justify-center">
    <el-form :model="user" :rules="rules" ref="formRef" class="w-[250px]">
      <el-form-item prop="username" :span = "24">
        <el-text class="w-150px mb-2" truncated>
          用户名：
        </el-text>
        <el-input
            v-model="user.username"
            style="width: 240px"
            placeholder="请输入用户名"
            clearable
        />
        <br><br>
      </el-form-item>
      <el-form-item prop="password" class="flex items-center justify-center">
        <el-text class="w-150px mb-2" truncated>
          密码：
        </el-text>
        <el-input
            v-model="user.password"
            style="width: 240px"
            type="password"
            placeholder="请输入密码"
            show-password
        />
        <br><br>
      </el-form-item>

      <el-form-item prop="email">
        <el-text class="w-150px mb-2" truncated>
          邮箱：
        </el-text>
        <el-input
            v-model="user.email"
            style="width: 240px"
            type="text"
            placeholder="请输入邮箱"
            clearable
        />
        <br><br>
      </el-form-item>

      <el-form-item prop="phone">
        <el-text class="w-150px mb-2" truncated>
          手机：
        </el-text>
        <el-input
            v-model="user.phone"
            style="width: 240px"
            type="text"
            placeholder="请输入手机"
            clearable
        />
        <br><br>
      </el-form-item>

      <el-form-item prop="gender">
        <el-text class="w-150px mb-2" truncated>
          性别：
        </el-text>
        <el-select
            v-model="user.gender"
            placeholder="请选择性别"
            style="width: 240px"
        >
          <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
        <br><br>
      </el-form-item>

      <el-form-item prop="role">
        <el-text class="w-150px mb-2" truncated>
          身份：
        </el-text>
        <el-radio-group v-model="user.role">
          <el-radio :value=1>学生</el-radio>
          <el-radio :value=2>教师</el-radio>
        </el-radio-group>
        <br><br>
      </el-form-item>

      <el-form-item>
        <el-button round color="#626aef" class="w-[250px]" type="primary" @click="register" :loading="loading">
          注 册
        </el-button>
      </el-form-item>
    </el-form>
          </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>

import { ref, reactive} from 'vue'
import api from "../../api"
import { toast } from "../../utils/popup"
import router from "@/router";


export default {
  name: "register",
  setup(){
    const user = reactive({
      username: '',
      password: '',
      email: '',
      phone: '',
      gender: '',
      role: ''
    })

    const rules = {
      username: [
        { required: true, message: "用户名不能为空", trigger: "blur" },
        { min: 6, max: 20, message: "用户名长度必须是6-20个字符", trigger: "blur" },
      ],
      password: [
        {
          required: true,
          message: "密码不能为空",
          trigger: "blur",
        },
        { min: 6, max: 20, message: "密码长度必须是6-20个字符", trigger: "blur" },

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
      gender: [
        { required: true, message: "性别不能为空", trigger: "blur" },
      ],
      role: [
        { required: true, message: "身份不能为空", trigger: "blur" },
      ]
    };

    const formRef = ref(null) // 表单引用

    function register() {
      console.log("register")
      formRef.value.validate((valid) => {
        if (valid) {
          api.register(user).then(res => {
            if (res.data.code === 200) {
              toast("注册成功，请继续登录", "success")
              setTimeout(() => {
                router.push("/")
              }, 1000)
            }else {
              toast(res.data.msg, "error")
            }
          })
        }else {
          toast("表单有误", "error")
        }
      })
    }

    const value = ref('')
    const options = [
      {
        value: true,
        label: '男',
      },
      {
        value: false,
        label: '女',
      }
    ]

    return{
      user,
      register,
      options,
      rules,
      formRef
    }

  }
}
</script>

<style scoped>

</style>