<template>
    <div v-if="message!=null" @click="drawerVisible = true" class="chat-bubble"
         @mouseover="hoverImage"
         @mouseout="resetImage"
         style="width: 200px;">
      <p class="bubble-content">星火助教有话说：<br/>{{ message }}</p>
    </div>
  <div class="container" >
    <img class="fixed-img" :src="imageSrc"
         @mouseover="hoverImage"
         @mouseout="resetImage"
         width="100px" height="100px" @click="drawerVisible = true">
    <el-drawer
        v-model="drawerVisible"
        size="30%"
        direction="rtl"
        :before-close="onClose"
        title="讯飞星火认知大模型 AI 聊天"
        :modal="true"
        :resizeable="true"
    >
      <el-form>
        <div class="drawer-content">
        <el-row>
          <el-col :span="20">
            <el-form-item label>
              <el-input  ref="input" v-model="ques" placeholder="请输入您的问题" @keyup.enter.prevent="submit" action="">
                <template #suffix>
                  <el-icon @click="talkModelView = talkModelView==true ? false : true"><Microphone /></el-icon>
                </template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-button type="primary" @click="submit">提交</el-button>
          </el-col>
        </el-row>
          <talk-model v-if="talkModelView" @getVideoMsg="getVideoMsg"></talk-model>
          <el-row v-for="(item, index) in history.slice().reverse()" :key="index">
            <el-col :span="24">
              <div class="question">{{ item.question }}</div>
            </el-col>
            <el-col :span="22">
              <div class="answer" v-html=item.answer ></div>
            </el-col>
            <el-col :span="1">
              <el-icon  @click="speakAnswer(item.answer)"><Headset /></el-icon>
            </el-col>
            <el-col :span="1">
              <el-icon  @click="pauseSpeaking"><VideoPause /></el-icon>
            </el-col>
            <el-divider></el-divider>
          </el-row>
        </div>

      </el-form>
    </el-drawer>
  </div>
</template>

<script>
import axios from 'axios';
import MarkdownIt from 'markdown-it';
import { toast } from "../utils/popup"
import path  from "@/api/path"
import aiImg from "./ai.png"
import aiHoverImg from "./ai-hover.png"
import talkModel from "@/components/talkModel";


const md = new MarkdownIt();

// 在你的Vue组件的methods或computed里添加这个逻辑
function convertNewlinesToBreaks(text) {
  if (text) {
    // 使用正则表达式全局替换\n为<br>
    return text.replace('\\n', '<br/>');
  }
  return text;
}
export default {
  name: "XFBigModel",
  data() {
    return {
      drawerVisible: false,
      ques: '',
      response: '',
      renderedResponse: '',
      text: '',
      history: [], // 新增历史记录数组
      imageSrc: aiImg,
      talkModelView: false,
      videoMsg: '',
      isSpeaking: false, // 新增状态来跟踪朗读状态
    };
  },
  components: {
    talkModel
  },
  props: ['message'],

  computed: {
    // 将response转换为HTML
    renderedResponse() {
      let processedResponse = md.render(this.response || '');
      // 处理换行
      // processedResponse = convertNewlinesToBreaks(processedResponse);
      return processedResponse;
    }
  },
  methods: {
    onClose() {
      this.drawerVisible = false;
      this.talkModelView = false
    },
    submit() {
      if(this.ques == ''){
        toast("请输入问题！", "error")
        return
      }
      this.talkModelView = false
      toast("处理中，请稍后...", "warning")
      axios.post(path.remoteBaseUrl+'/process_text', {
      // axios.post('http://127.0.0.1:5001/process_text/', {
      // axios.post('http://139.196.253.125:5000/process_text/', {
        text: this.ques
      }, {
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(response => {
        this.text = convertNewlinesToBreaks(response.data.result);
        this.response = convertNewlinesToBreaks(response.data.result);
        this.renderedResponse = md.render(this.response);
        // 添加新问题和答案到历史记录
        this.history.push({ question: this.ques, answer: this.renderedResponse });
        this.ques = '';
        toast("结果生成完毕！", "success")
      });
    },

    speakAnswer(answer) {
      if ('speechSynthesis' in window) {
        this.isSpeaking = true; // 开始朗读前设置为true
        const utterance = new SpeechSynthesisUtterance(answer);

        utterance.onend = () => {
          this.isSpeaking = false; // 朗读结束后设置回false
        };

        speechSynthesis.cancel(); // 取消当前所有朗读任务，确保只朗读最新的
        speechSynthesis.speak(utterance);
      } else {
        alert('您的浏览器不支持文本转语音功能。');
      }
    },
    pauseSpeaking() {
      if ('speechSynthesis' in window && speechSynthesis.paused) {
        speechSynthesis.resume(); // 如果已暂停，则恢复朗读
      } else if ('speechSynthesis' in window && !speechSynthesis.paused) {
        speechSynthesis.pause(); // 如果正在朗读，则暂停
      }
    },

    getVideoMsg(childMsg){
        this.videoMsg = childMsg
        this.ques = childMsg
    },

  onMounted() {
  },
    hoverImage() {
      this.imageSrc = aiHoverImg;
    },
    resetImage() {
      this.imageSrc = aiImg;
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: flex-end;
  /*align-items: center;*/
  /*height: 100vh;*/
}
.fixed-img {
  position: fixed;
  bottom: 10px;
  right: 10px;
  cursor: pointer;
  z-index: 1000;
}

.drawer-content {
  display: flex;
  flex-direction: column;
}

.question {
  margin-bottom: 10px;
  text-align: left;
}

.answer {
  margin-bottom: 10px;
  text-align: left;
}
.chat-bubble {
  background-color: #E3ECFC;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 10px;

  display: inline-block;
  max-width: 70%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

  position: fixed;
  bottom: 120px;
  right: 10px;
  cursor: pointer;
  z-index: 1000;
}
.el-icon {
  cursor: pointer;
}
</style>
