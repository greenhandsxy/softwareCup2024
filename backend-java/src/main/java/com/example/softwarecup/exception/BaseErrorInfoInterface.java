package com.example.softwarecup.exception;

/**
 * @author SaoE
 * @date 2024/4/18 11:33
 */
public interface BaseErrorInfoInterface {
    /**
     * 错误码
     *
     * @return
     */
    String getResultCode();

    /**
     * 错误描述
     *
     * @return
     */
    String getResultMsg();
}
