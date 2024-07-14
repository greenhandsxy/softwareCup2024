// 封装网络请求的方法
import axios from "axios";


const errorHandler = (status, info) => {
    // 错误处理
    switch(status){
        case 400:
            console.log('请求错误')
            break
        case 401:
            console.log('未授权')
            break
        case 403:
            console.log('禁止访问')
            break
        case 404:
            console.log('请求地址错误')
            break
        case 500:
            console.log('服务器错误')
            break
        case 502:
            console.log('网关错误')
            break
        default:
            console.log(info || '未知错误'); // 添加一个默认值，避免 undefined 报错
    }
}


const instance = axios.create({
    //网络请求的公共配置
    timeout: 5000,
    headers:{
        'Content-Type': 'application/json'
    }

})

export default instance