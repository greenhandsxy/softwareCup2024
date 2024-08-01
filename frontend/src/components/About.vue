<template>
  <h1>一、关于项目</h1>
  <p>
    <b>本项目是由南京邮电大学-徐竟晗、肖逸、杜小龙三人团队使用星火认知大模型及相关API结合前后端技术开发的一款“提升教师教学效率，减轻学生学习压力”的智慧教育平台。</b>
  </p>
  <p>
    <b>本项目技术栈主要包括：</b><br>
  </p>
    <ul>
      <li>前端部分：Vue3、VueRouter、Vuex、Element-Plus、Axios等</li>
      <li>后端部分：Java、SpringBoot、Python、Flask、MySQL、Redis、Nginx等</li>
      <li>其他技术：Git、OSS、内网穿透等</li>
    </ul>
  <p>
    <b>本项目主要完成内容：</b><br>
  </p>
  <ul>
    <li>
      用户通用功能模块：登录、注册、查看/修改个人信息、修改头像<b>（制作个性化头像）</b>、退出登录
    </li>
    <li>
      课程信息模块：课程信息分类分页展示，课程详情展示
    </li>
    <li>
      学生功能模块：学生选课、退课、查看选课学习情况<b>（预测得分）</b>、学习课程视频
    </li>
    <li>
      教师功能模块: 教师发布课程、查看开课情况<b>（预测课程热度）</b>、查看学生学习情况<b>（预测得分、一键导出）</b>、作业自动批改
    </li>
    <li>
      AI功能模块：AI智能助教、语音翻译、英汉翻译、OCR图片文字识别、PPT自动生成、Latex公式识别
    </li>
    <li>
      项目实现在线部署：前端、Java后端和数据库部署在阿里云服务器，项目在线部署地址：<a href="http://tools.elearninghome.cn:8887"><b>http://tools.elearninghome.cn:8887</b></a>
    </li>
    <li>
      代码开源：项目代码托管在GitHub平台上，地址为<a href="https://github.com/greenhandsxy/softwareCup2024" target="_blank"><b>https://github.com/greenhandsxy/softwareCup2024</b></a>
    </li>
  </ul>
    <p>
    <b>测试账号</b><br>
    </p>
  <ul>
    <li>
      学生账号：aaaaaa，密码：aaaaaa
    </li>
    <li>
      教师账号：韩海花，密码：666666
    </li>
  </ul>
  <h3>项目设置</h3>
    <p><b>
      为使项目可以运行完整功能，需要获取浏览器相关权限，具体作以下设置：<br>
      1、使用chorme或edge浏览器打开<br>
      2、浏览器网址输入：chrome://flags/#unsafely-treat-insecure-origin-as-secure<br>
      3、在第一个高亮输入框中输入：http://tools.elearninghome.cn:8887<br>
      4、点击右下角重启浏览器按钮，重启浏览器后完成设置<br>
    </b>
      <img src="./img.png" alt="img">
    </p>

  <h1>二、关于开发团队</h1>
    <ul>
      <li>
        徐竟晗（队长）：主要负责系统算法部分，结合讯飞API实现可用功能。撰写一篇发明专利。
      </li>
      <li>
        肖逸：主要负责设计数据库、开发系统前后端并部署上线，进行网站运维。撰写一篇发明专利。
      </li>
      <li>
        杜小龙：主要负责讯飞AI接口的集成，Python后端实现、内网穿透部署以及系统测试。
      </li>
    </ul>
  <h1>三、版本更新日志</h1>
  <ul>
    <li>
      <h3>20240801-至今</h3>
      <b>国赛加油！</b>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <p>
        1、界面优化<br>
        2、修复已知bug
      </p>

    </li>
    <li>
      <h3>20240706-20240715</h3>
      <p>
        1、完善页面显示和信息提示体系<br>
        2、部分代码重构，完善系统
      </p>
    </li>
    <li>
      <h3>20240705</h3>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <b>功能至此全部开发完毕！</b>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <el-icon><Flag /></el-icon>
      <p>
        1、新增根据AI工具<b>Latex公式功能</b><br>
        2、完善PPT显示方式，新增<b>预览链接和下载按钮</b><br>
        2、完善信息提示体系<br>
      </p>
    </li>
    <li>
      <h3>20240704</h3>
      <p>
        1、新增根据<b>生成的PPT大纲生成PPT功能</b><br>
        2、修改PPT生成界面UI<br>
        3、完善信息提示体系<br>
      </p>
    </li>
    <li>
      <h3>20240703</h3>
      <p>
        1、新增语音翻译使用<b>录音上传功能</b><br>
        2、修改语音翻译界面，新增<b>拖拽上传音频文件功能</b><br>
        3、完善信息提示体系<br>
      </p>
    </li>
    <li>
      <h3>20240702</h3>
      <p>
        1、新增大模型对话<b>语音上传功能</b>、回答内容<b>朗读及暂停功能</b><br>
        2、完善大模型问答<b>倒叙输出</b>，优化用户体验<br>
        3、完善信息提示体系<br>
      </p>
    </li>
    <li>
      <h3>20240629</h3>
        <p>
          新增<b>OCR拖拽上传文件功能</b>，修改首页UI，新增“项目及团队介绍”界面
        </p>
    </li>
    <li>
      <h3>20240628</h3>
        <p>
          完善教师自动批改界面，新增<b>拖拽上传作业功能</b>，完善展示功能
        </p>
    </li>
    <li>
      <h3>20240414-20240626</h3>
      <p>
        功能开发基本完成，同时完成上线部署。包括以下功能模块：<br>
        1、用户通用功能模块：登录、注册、查看/修改个人信息、修改头像<b>（制作个性化头像）</b>、退出登录<br>
        2、课程信息模块：课程信息分类分页展示，课程详情展示<br>
        3、学生功能模块：学生选课、退课、查看选课学习情况<b>（预测得分）</b>、学习课程视频<br>
        4、教师功能模块: 教师发布课程、查看开课情况<b>（预测课程热度）</b>、查看学生学习情况<b>（预测得分、一键导出）</b>、作业自动批改<br>
        5、AI功能模块：AI智能助教、语音翻译、英汉翻译、OCR图片文字识别、PPT自动生成<br>
      </p>
    </li>
  </ul>


</template>

<script>
export default {
  name: "About"
}
</script>

<style scoped>
*{
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
}
</style>