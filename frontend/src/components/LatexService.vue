<template>
  <el-upload
      class="upload-demo"
      drag
      action="http://a929594m76.zicp.fun/latex"
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
  <div style="text-align: -webkit-center" class="border-grey-100 border-3 ml-50 mr-50 mt-20 h-100">
    <el-form ref="ruleForm" label-width="100px" style="width: max-content">
      <br>
      <div style="text-align: left">在线latex公式编辑器:</div>
      <br>
      <el-form-item label-width="0">
        <el-input class="border-4 border-indigo-200" v-model="test" style="width: 480px" :rows="2" type="textarea"
                  placeholder="请输入latex公式" />
      </el-form-item>
      <VueLatex :expression=test display-mode/>
    </el-form>
  </div>
</template>

<script>
import {toast} from "@/utils/popup";
import {ref} from "vue";

export default {
  name: "LatexService",
  data() {
    return {
      equ: '\\frac{a_i}{1+x}',

    }
  },
  setup() {

    function handleError(){
      toast("文件上传失败", "error")
    }

    function beforeImageUpload(file) {
      const isImage = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/gif';
      if (!isImage) {
        toast('只能上传图片文件！', "error");
        return false; // 阻止非图片文件上传
      }
      toast('公式识别中，请稍后...', "warning");
      return true;
    }
    const test = ref('')
    function handleSuccess(res) {
      toast("公式识别成功！", "success")
      test.value = res.formula;
    }
    return {
      handleError,
      beforeImageUpload,
      handleSuccess,
      test
    }
  }
}

</script>