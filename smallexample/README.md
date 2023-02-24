# Setting up an AWAKEN case

Follow these steps to set up a case similar to the AWAKEN case.

**Contents**
- [Turbine calibration](#turbine-calibration)
- [Determining the precursor BC](#determining-the-precursor-bc)
- [Setting up the precursor run](#setting-up-the-precursor-run)
- [Setting up the turbine run](#setting-up-the-turbine-run)


## Turbine calibration  
If you're using a brand new turbine model, you may need to calibrate the turbine parameters (such as epsilon or a vortex core size) so that it generates the correct power.

Take a look at one of the examples in the [turbines](../turbines) directory, such as the [GE2.5-116 model](../turbines/GE2.5-116), and run the [calibration notebook](turbines/GE2.5-116/RunCalibration_Joukowski_Eps5.00.ipynb) first.  Then run the [PlotCurves](../turbines/GE2.5-116/PlotCurves5.ipynb) notebook to look at the results.

## Determining the precursor BC 
Run this [precursor notebook](../precursor/UnstableABL1/precursor4_10m_largerdomain/KingPlains_unstable_precursor4_largerdomain.ipynb) for an example of how to set up a test case to match a particular hub-height wind speed/wind condition.

Then, after some iteration, you can compare results with this [Postprocessing notebook](../precursor/UnstableABL1/Postprocessing.ipynb).

## Setting up the precursor run
Once you have the correct boundary conditions determined, run the [UnstableABL_setup2.ipynb](#UnstableABL_setup2.ipynb) notebook to set up the appropriate domain for a wind farm configuration.

## Setting up the turbine run
Once you have boundary plane data saved from the precursor, run the [UnstableABL_FarmRunSmall.ipynb](UnstableABL_FarmRunSmall.ipynb) notebook.

