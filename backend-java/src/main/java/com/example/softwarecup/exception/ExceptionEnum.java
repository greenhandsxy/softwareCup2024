package com.example.softwarecup.exception;

/**
 * @author SaoE
 * @date 2024/4/18 17:31
 */
public enum ExceptionEnum implements BaseErrorInfoInterface{
    // 数据操作错误定义
    SUCCESS("200", "成功!"),
    EXISTED("4001", "账号已存在!"),
    INTERNAL_SERVER_ERROR("4002", "服务器内部错误!"),
    SERVER_BUSY("4003", "服务器正忙，请稍后再试!"),
    AUTH_ERROR("4004", "用户未登录！"),
    AUTH_NOT_ENOUGH("4005", "权限不足，请联系管理员!"),
    LOGIN_ERROR("4006", "用户名或密码错误!"),
    NOT_LOGIN("4007", "用户未登录!"),
    Course_Has_Been_Chosen("4008", "该课程已选!"),
    Course_Has_Not_Been_Chosen("4009", "请先选择该课程!"),
    NOT_SELECT_ANY_COURSES("4010", "还未选课");

    /**
     * 错误码
     */
    private final String resultCode;

    /**
     * 错误描述
     */
    private final String resultMsg;

    ExceptionEnum(String resultCode, String resultMsg) {
        this.resultCode = resultCode;
        this.resultMsg = resultMsg;
    }

    @Override
    public String getResultCode() {
        return resultCode;
    }

    @Override
    public String getResultMsg() {
        return resultMsg;
    }
}
