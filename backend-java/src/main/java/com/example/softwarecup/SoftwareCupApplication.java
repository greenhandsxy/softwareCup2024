package com.example.softwarecup;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan(basePackages = "com.example.softwarecup.mapper")
public class SoftwareCupApplication {

    public static void main(String[] args) {
        SpringApplication.run(SoftwareCupApplication.class, args);
    }

}
