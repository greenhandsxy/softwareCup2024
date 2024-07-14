package com.example.softwarecup.tools;

import com.example.softwarecup.exception.BaseErrorInfoInterface;
import com.example.softwarecup.exception.ExceptionEnum;
import com.example.softwarecup.pojo.Course;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * @author SaoE
 * @date 2024/4/18 17:29
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Result<T> {

    @ApiModelProperty(value = "状态码")
    private int code;
    @ApiModelProperty(value = "提示信息")
    private String msg;
    @ApiModelProperty(value = "返回数据")
    private T data;

    private Result(BaseErrorInfoInterface errorInfo) {
        this.code = Integer.parseInt(errorInfo.getResultCode());
        this.msg = errorInfo.getResultMsg();
    }


    private Result(BaseErrorInfoInterface errorInfo, T data) {
        this.code = Integer.parseInt(errorInfo.getResultCode());
        this.msg = errorInfo.getResultMsg();
        if (data != null && data.getClass() != ExceptionEnum.class) {
            this.data = data;
        }
    }

    /**
     * 成功时候的调用
     */
    public static <T> Result<T> success(T data) {
        return new Result<>(ExceptionEnum.SUCCESS, data);
    }

    public static <T> Result<T> success(List<Course> data) {
        return new Result(ExceptionEnum.SUCCESS, data);
    }


    /**
     * 失败
     */
    public static <T> Result<T> error(BaseErrorInfoInterface errorInfo) {
        Result<T> result = new Result<>(errorInfo);
        result.setData(null);
        return result;
    }

    /**
     * 失败
     */
    public static <T> Result<T> error(Integer code, String message) {
        Result<T> result = new Result<T>();
        result.setCode(code);
        result.setMsg(message);
        result.setData(null);
        return result;
    }

    /**
     * 失败
     */
    public static <T> Result<T> error(String message) {
        Result<T> result = new Result<T>();
        result.setCode(-1);
        result.setMsg(message);
        result.setData(null);
        return result;
    }

}
