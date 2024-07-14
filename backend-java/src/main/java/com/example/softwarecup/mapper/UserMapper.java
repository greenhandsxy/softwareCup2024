package com.example.softwarecup.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.softwarecup.pojo.User;
import org.apache.ibatis.annotations.Mapper;

/**
 * @author SaoE
 * @date 2024/4/18 11:20
 */

@Mapper
public interface UserMapper extends BaseMapper<User> {
}
