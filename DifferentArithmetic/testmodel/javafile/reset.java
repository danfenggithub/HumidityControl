// STAR-CCM+ macro: reset.java
// Written by STAR-CCM+ 14.02.012
package macro;

import java.util.*;
import star.common.*;
import star.base.neo.*;
import star.species.*;

public class reset extends StarMacro {

  public void execute() {
    execute0();
    // C:/Users/97922/Desktop/starccm tutorial/humidity.sim
  }

  private void execute0() {

    Simulation simulation_0 = 
      getActiveSimulation();

    Solution solution_0 = 
      simulation_0.getSolution();

    solution_0.clearSolution(Solution.Clear.History, Solution.Clear.Fields, Solution.Clear.LagrangianDem);

    PhysicsContinuum physicsContinuum_0 =
      ((PhysicsContinuum) simulation_0.getContinuumManager().getContinuum("Physics 1"));

    MassFractionProfile massFractionProfile_0 =
      physicsContinuum_0.getInitialConditions().get(MassFractionProfile.class);
    // 33
    massFractionProfile_0.getMethod(ConstantArrayProfileMethod.class).getQuantity().setArray(new DoubleVector(new double[] {0.0097803, 0.9902197}));

    simulation_0.saveState("humidity.sim");
  }

}
