// STAR-CCM+ macro: edit.java
// Written by STAR-CCM+ 14.02.012
package macro;

import java.util.*;
import star.common.*;
import star.base.neo.*;
import star.energy.*;
import star.flow.*;
import star.species.*;
import star.base.report.*;
import java.io.File;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileWriter;

@SuppressWarnings("unchecked")
public class editandrun extends StarMacro {

  private void execute0() {

    Simulation simulation_0 = 
      getActiveSimulation();

    Region region_0 = simulation_0.getRegionManager().getRegion("roomex");

    Boundary boundary_1 = region_0.getBoundaryManager().getBoundary("InletRHa");

    MassFractionProfile massFractionProfile_1 = boundary_1.getValues().get(MassFractionProfile.class);
    // 33
	massFractionProfile_1.getMethod(ConstantArrayProfileMethod.class).getQuantity().setArray(new DoubleVector(new double[] {0.00788,0.99212}));

	VelocityMagnitudeProfile velocityMagnitudeProfile_1 = boundary_1.getValues().get(VelocityMagnitudeProfile.class);
    // 37
	velocityMagnitudeProfile_1.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(1);
	
	
	
    Boundary boundary_2 = region_0.getBoundaryManager().getBoundary("InletRHb");

    MassFractionProfile massFractionProfile_2 = boundary_2.getValues().get(MassFractionProfile.class);
    // 45
	massFractionProfile_2.getMethod(ConstantArrayProfileMethod.class).getQuantity().setArray(new DoubleVector(new double[] {0.00788,0.99212}));

    VelocityMagnitudeProfile velocityMagnitudeProfile_2 = boundary_2.getValues().get(VelocityMagnitudeProfile.class);
    // 49
	velocityMagnitudeProfile_2.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(2);



    Boundary boundary_3 = region_0.getBoundaryManager().getBoundary("InletRHc");

    MassFractionProfile massFractionProfile_3 = boundary_3.getValues().get(MassFractionProfile.class);
    // 57
	massFractionProfile_3.getMethod(ConstantArrayProfileMethod.class).getQuantity().setArray(new DoubleVector(new double[] {0.00788,0.99212}));

    VelocityMagnitudeProfile velocityMagnitudeProfile_3 = boundary_3.getValues().get(VelocityMagnitudeProfile.class);
    // 61
	velocityMagnitudeProfile_3.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValue(1);


    // 是否要加indoor风口
    Boundary boundary_0 =
      region_0.getBoundaryManager().getBoundary("InletDoor");
    // 68
	WallBoundary wallBoundary_0 = ((WallBoundary) simulation_0.get(ConditionTypeManager.class).get(WallBoundary.class));
    // 70
	boundary_0.setBoundaryType(wallBoundary_0);
    // 72--------------------------------------------











    // 82-----------------------------------------------


    simulation_0.getSimulationIterator().runAutomation();

    ReportMonitor reportMonitor_0 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B91RH Monitor"));

    ReportMonitor reportMonitor_1 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B92RH Monitor"));

    ReportMonitor reportMonitor_2 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B93RH Monitor"));

    ReportMonitor reportMonitor_3 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B94RH Monitor"));

    ReportMonitor reportMonitor_4 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B95RH Monitor"));

    ReportMonitor reportMonitor_5 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B96RH Monitor"));

    ReportMonitor reportMonitor_6 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B97RH Monitor"));

    ReportMonitor reportMonitor_7 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B98RH Monitor"));

    ReportMonitor reportMonitor_8 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B99RH Monitor"));

    ReportMonitor reportMonitor_9 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B910RH Monitor"));

    ReportMonitor reportMonitor_10 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B911RH Monitor"));

    ReportMonitor reportMonitor_11 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B912RH Monitor"));

    ReportMonitor reportMonitor_12 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B913RH Monitor"));

    ReportMonitor reportMonitor_13 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B914RH Monitor"));

    ReportMonitor reportMonitor_14 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B915RH Monitor"));

    ReportMonitor reportMonitor_15 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B916RH Monitor"));

    ReportMonitor reportMonitor_16 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B917RH Monitor"));

    ReportMonitor reportMonitor_17 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B918RH Monitor"));

    ReportMonitor reportMonitor_18 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B919RH Monitor"));

    ReportMonitor reportMonitor_19 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B920RH Monitor"));

    ReportMonitor reportMonitor_20 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("\u70B921RH Monitor"));

    ReportMonitor reportMonitor_21 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("InletDoor Monitor"));

    ReportMonitor reportMonitor_22 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("InletRHa Monitor"));

    ReportMonitor reportMonitor_23 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("InletRHb Monitor"));

    ReportMonitor reportMonitor_24 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("InletRHc Monitor"));

    ReportMonitor reportMonitor_25 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("InletVela Monitor"));

    ReportMonitor reportMonitor_26 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("InletVelb Monitor"));

    ReportMonitor reportMonitor_27 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("InletVelc Monitor"));

    ReportMonitor reportMonitor_28 =
      ((ReportMonitor) simulation_0.getMonitorManager().getMonitor("InletVelDoor Monitor"));

    simulation_0.getMonitorManager().export("RHfile.csv", ",", new NeoObjectVector(new Object[] {
    reportMonitor_0, reportMonitor_1, reportMonitor_2, reportMonitor_3, reportMonitor_4, reportMonitor_5,
    reportMonitor_6, reportMonitor_7, reportMonitor_8, reportMonitor_9, reportMonitor_10, reportMonitor_11,
    reportMonitor_12, reportMonitor_13, reportMonitor_14, reportMonitor_15, reportMonitor_16, reportMonitor_17,
    reportMonitor_18, reportMonitor_19, reportMonitor_20, reportMonitor_21, reportMonitor_22, reportMonitor_23,
    reportMonitor_24, reportMonitor_25, reportMonitor_26, reportMonitor_27, reportMonitor_28}));

    simulation_0.saveState("humidity.sim");

    try {
        /* 写入Txt文件 */
        File writename = new File("javafile/info.txt"); // 相对路径，如果没有则要建立一个新的output。txt文件
        writename.createNewFile(); // 创建新文件
        BufferedWriter out = new BufferedWriter(new FileWriter(writename));
        out.write("false");
        out.flush(); // 把缓存区内容压入文件
        out.close(); // 最后记得关闭文件
    } catch (Exception e) {
        e.printStackTrace();
    }

  }

  public void execute() {
    execute0();
  }


}
