<template>
  <div >
    <div style="font-size:14px">
      <h3>录音时长：{{ recorder && recorder.duration.toFixed(4) }}</h3>
      <br />
      <el-button type="primary" @click="handleStart">开始录音</el-button>
      <el-button v-if="msg" type="info" @click="handlePause">暂停录音</el-button>
      <el-button v-if="msg" type="success" @click="handleResume">继续录音</el-button>
      <el-button type="warning" @click="handleStop">停止录音</el-button>
      <br v-if="msg"/>
      <br v-if="msg"/>
<!--      <h3>-->
<!--        播放时长：{{ recorder && (playTime > recorder.duration ? recorder.duration.toFixed(4) : playTime.toFixed(4)) }}-->
<!--      </h3>-->
<!--      <br />-->
<!--      <br />-->
      <el-button v-if="msg" type="primary" @click="handlePlay">播放录音</el-button>
<!--      <el-button type="info" @click="handlePausePlay">暂停播放</el-button>-->
<!--      <el-button type="success" @click="handleResumePlay">继续播放</el-button>-->
<!--      <el-button type="warning" @click="handleStopPlay">停止播放</el-button>-->
      <el-button type="error" @click="handleDestroy">重新录音</el-button>
<!--      <br />-->
<!--      <br />-->
<!--      <el-button type="primary" @click="downloadPCM">下载PCM数据</el-button>-->
      <el-button v-if="msg" type="primary" @click="downloadWAV">下载WAV数据</el-button>
      <el-button type="primary" @click="uploadRecord">确定</el-button>
      <el-divider></el-divider>
    </div>
  </div>
</template>

<script>
import Recorder from 'js-audio-recorder'
import axios from "axios";
import {DataLine} from "@element-plus/icons-vue";
import { toast } from "../utils/popup"
import path  from "@/api/path"


export default {
  name: 'talkModel',
  components: {DataLine},
  props: ["msg"],
  data() {
    return {
      recorder: null,
      playTime: 0,
      timer: null,
      src: null
    }
  },
  created() {
    this.recorder = new Recorder({
      sampleBits: 16, // 采样位数，支持 8 或 16，默认是 16
      sampleRate: 16000, // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，Chrome 是 48000
      numChannels: 1, // 声道数，支持 1 或 2， 默认是 1
    })
  },
  methods: {
    // 开始录音
    handleStart() {
      this.recorder = new Recorder({
        sampleBits: 16, // 采样位数，支持 8 或 16，默认是 16
        sampleRate: 16000, // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，Chrome 是 48000
        numChannels: 1, // 声道数，支持 1 或 2， 默认是 1
      }),
          Recorder.getPermission().then(() => {
            this.recorder.start() // 开始录音
          }, (error) => {
            this.$message({
              message: '请先允许该网页使用麦克风',
              type: 'info'
            })
            toast("请先允许该网页使用麦克风", "error")
          })
    },
    handlePause() {
      this.recorder.pause() // 暂停录音
    },
    handleResume() {
      this.recorder.resume() // 恢复录音
    },
    handleStop() {
      this.recorder.stop() // 停止录音
    },
    handlePlay() {
      this.recorder.play() // 播放录音

      // 播放时长
      this.timer = setInterval(() => {
        try {
          this.playTime = this.recorder.getPlayTime()
        } catch (error) {
          this.timer = null
        }
      }, 100)
    },
    handlePausePlay() {
      this.recorder.pausePlay() // 暂停播放

      // 播放时长
      this.playTime = this.recorder.getPlayTime()
      this.time = null
    },
    handleResumePlay() {
      this.recorder.resumePlay() // 恢复播放

      // 播放时长
      this.timer = setInterval(() => {
        try {
          this.playTime = this.recorder.getPlayTime()
        } catch (error) {
          this.timer = null
        }
      }, 100)
    },
    handleStopPlay() {
      this.recorder.stopPlay() // 停止播放

      // 播放时长
      this.playTime = this.recorder.getPlayTime()
      this.timer = null
    },
    handleDestroy() {
      this.recorder.destroy() // 销毁实例
      this.timer = null
    },
    downloadPCM() {
      // 注：使用该方法会默认调用 stop() 方法
      this.recorder.downloadPCM("record" + new Date().getTime())
    },
    downloadWAV() {
      // 注：使用该方法会默认调用 stop() 方法
      this.recorder.downloadWAV("record" + new Date().getTime())
    },
    async uploadRecord() {
      if (this.recorder == null || this.recorder.duration === 0) {
        this.$message({
          message: '请先录音',
          type: 'error'
        })
        return false
      }
      this.recorder.pause() // 暂停录音
      this.timer = null
      toast("录音识别中，请稍后...", "warning")
      // const blob = this.recorder.getPCMBlob() // 获取 pcm 格式音频数据
      const blob = this.recorder.getWAVBlob() // 获取 pcm 格式音频数据
      const newBlob = new Blob([blob])
      // 此处获取到 blob 对象后需要设置 fileName 满足项目上传需求，这里选择把 blob 包装成 file 塞入 formData
      const fileOfBlob = new File([newBlob], new Date().getTime() + '.pcm')

      const formData = new FormData()
      formData.append('file', fileOfBlob)
      const url = window.URL.createObjectURL(fileOfBlob)
      this.src = url
      // axios.post('http://127.0.0.1:5000/voice', formData, {
      await axios.post(path.remoteBaseUrl + '/voice', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        this.$emit('getVideoMsg', response.data.message)
        toast("录音识别成功！", "success")
      }).catch(error => {
        toast("出错了", "error")
      })
    },
  }
}
</script>
