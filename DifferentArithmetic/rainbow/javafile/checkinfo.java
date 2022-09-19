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

            try {
                String pathname = "javafile/info.txt";
                File filename = new File(pathname);
                InputStreamReader reader = new InputStreamReader(new FileInputStream(filename));
                BufferedReader br = new BufferedReader(reader);
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
