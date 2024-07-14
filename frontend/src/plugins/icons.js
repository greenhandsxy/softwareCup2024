// element-plus引入所有图标的配置
// 固定写法
import * as components from "@element-plus/icons-vue"
export default {
    install: (app) =>{
        for(const key in components){
            const componentConfig  = components[key];
            app.component(componentConfig.name, componentConfig);
        }
    }
};