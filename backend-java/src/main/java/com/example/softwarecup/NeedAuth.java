package com.example.softwarecup;

import java.lang.annotation.*;

/**
 * @author SaoE
 * @date 2024/5/9 12:03
 */
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface NeedAuth {

    String[] value() default {};

}
