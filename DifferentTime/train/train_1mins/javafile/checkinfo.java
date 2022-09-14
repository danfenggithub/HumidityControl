// STAR-CCM+ macro: checkinfo.java
// Written by STAR-CCM+ 14.02.012
package macro;

import java.util.*;
import star.common.*;
import star.base.neo.*;
import star.flow.*;
import star.species.*;
import star.base.report.*;
import java.io.File;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileWriter;

public class checkinfo extends StarMacro {

  public void execute() {
  		while(true){

            try { // 防止文件建立或读取失败，用catch捕捉错误并打印，也可以throw
                /* 读入TXT文件 */
                String pathname = "javafile/info.txt"; // 绝对路径或相对路径都可以，这里是绝对路径，写入文件时演示相对路径
                File filename = new File(pathname); // 要读取以上路径的input。txt文件
                InputStreamReader reader = new InputStreamReader(new FileInputStream(filename)); // 建立一个输入流对象reader
                BufferedReader br = new BufferedReader(reader); // 建立一个对象，它把文件内容转成计算机能读懂的语言
                String line = "";
                line = br.readLine();
                if (line.equals("true")){
                    break;
                }

            } catch (Exception e) {
                System.out.println(e);
            }

            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                System.out.println(e);
            }

		}


  }
}
