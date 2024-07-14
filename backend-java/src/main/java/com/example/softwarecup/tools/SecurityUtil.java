package com.example.softwarecup.tools;

import cn.hutool.crypto.digest.DigestAlgorithm;
import cn.hutool.crypto.digest.Digester;

/**
 * @author SaoE
 * @date 2024/4/18 11:24
 */
public class SecurityUtil {
    public static String crypto(String salt, String message) {
        Digester md5 = new Digester(DigestAlgorithm.MD5);
        StringBuilder sb = new StringBuilder();
        int i = 0, j = message.length() - 1;
        while (i < salt.length() || j >= 0) {
            if (i < salt.length()) sb.append(salt.charAt(i++));
            if (j >= 0) sb.append(message.charAt(j--));
            else break;
        }
        System.out.println(sb);
        return md5.digestHex(sb.toString());
    }
}
