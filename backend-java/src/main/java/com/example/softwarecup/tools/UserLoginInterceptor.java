package com.example.softwarecup.tools;

import cn.hutool.json.JSONUtil;
import com.example.softwarecup.NeedAuth;
import com.example.softwarecup.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.util.StringUtils;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import java.io.IOException;

/**
 * @author SaoE
 * @date 2024/4/24 12:52
 */
@Slf4j
public class UserLoginInterceptor implements HandlerInterceptor {

    Logger logger = LoggerFactory.getLogger(UserLoginInterceptor.class);

    @Autowired
    private UserService userService;

    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws IOException {
        log.info("拦截器拦截");
        CodeMsg errorCode = null;
        //获取注解
        boolean hasAuth;
        HandlerMethod handlerMethod = (HandlerMethod) handler;
        NeedAuth access = handlerMethod.getMethod().getAnnotation(NeedAuth.class);
        //如果未标记注解，直接返回空 直接放行
        if (access == null) {
            return true;
        }
        String paramToken = request.getParameter(UserService.COOKIE_NAME_TOKEN);
        String cookieToken = RequestUtil.getCookieValue(request, UserService.COOKIE_NAME_TOKEN);
        //token为空，那么该用户未登录，返回null
        if (StringUtils.isEmpty(cookieToken) && StringUtils.isEmpty(paramToken)) {
            hasAuth = false;
            errorCode = CodeMsg.NO_LOGIN;
        } else {
            String token = paramToken == null ? cookieToken : paramToken;
            hasAuth = userService.isAuth(token);
            //用户携带token但是Session已经过期。
            if (!hasAuth) {
                errorCode = CodeMsg.SESSION_ERROR;
            }
        }
        //如果未验证，那么就会返回未登录。
        if (!hasAuth) {
            logger.error("用户请求被拦截");
            response.reset();
            response.setContentType("application/json;charset=UTF-8");
            response.setCharacterEncoding("UTF-8");

            //todo
            response.getWriter().write(JSONUtil.toJsonStr(Result.error("未验证")));
        }
        return hasAuth;
    }
}
