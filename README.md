# 3D RISM
<details>
<summary><b>Help documentation</b> </summary>

    usage: rism3d.py [-h] [--prm_in PRM_IN] [--coord_in COORD_IN] [--pdb_out PDB_OUT] [--water_model WATER_MODEL] [--dieps DIEPS] [--n N] pdb_in

    positional arguments:
      pdb_in                Input pdb
    
    optional arguments:
      -h, --help            show this help message and exit
      --prm_in PRM_IN       Input parameter file
      --coord_in COORD_IN   Input coordinate file
      --pdb_out PDB_OUT     Output pdb name
      --water_model WATER_MODEL
                            Water Model (cSPCE/cTIP3P) (default = cTIP3P)
      --dieps DIEPS         Dielectric Constant (default = 78.44)
      --n N                 Number of Cores (default = 1)
</details>

This repository is the code for running 3D RISM on a given PDB/SDF file and subsequent water placement using the Placevent algorithm. 

By default, code takes in PDB/SDF file and generates parameter and coordinate files using pdb4amber. 1D RISM is done on the specified water model before 3D RISM is run on the protein and solvent.

Solute free energy density files are also output.

## Installing Required Packages
The latest version of AmberTools, which runs 1D and 3D RISM, can be downloaded at this link: https://ambermd.org/AmberTools.php

Placevent algorithm can be cloned from this repository: https://github.com/dansind/Placevent.git and run setup.py. Note that Grid and Numpy packages are required 

## Running 1D and 3D RISM
Required input files:
- PDB file of solute

If topology and coordinate files are nor specified, tleap in AmberTools is used to generate them using ff14SB force field.

1D RISM is run for the specified water model at the given dielectric constant value. Water concentration is set to 55.5M and a .xvv file is output. Note that this 1D RISM output can be used across different solutes.

3D RISM is then run with the specified number of CPU cores. A default buffer of 48A and grid spacing of 0.5A is set. Sequential closures of increasing accuracy (kh, PSE2, PSE3) are used.

## Running Placevent
Placevent takes in the population .dx file output from 3D RISM and places explicit solvent molecules around the solute. Water concentration is set to 55.5M. A PDB file of water coordinates is output.

## Outputs
In depth explanations of output files from 3D RISM can be found in Amber's tutorial: https://ambermd.org/tutorials/advanced/tutorial40/index.php

Briefly, 3D RISM outputs population density .dx files for both O and H atoms, discretised to a grid of spacing 0.5A. Compiled thermodynamic values are found in the .out file, with notable values such as excess chemical potential (dG)

Volumetric data of excess chemical potential (dG) is also generated. All .dx files can be visualised using VMD/PyMol

## Running test system 
Run bash script as follows
```
sh ./test_rism.sh
```
Reference output PDB file from Placevent as well as .out file from 3D RISM is provided.

## Known list of issues
- 3D RISM takes too long: Check the .out file to see if tolerance value is decreasing. If it stays relatively constant, closure/tolerance values may need to be adjusted
    - Another possible reason is solute being too large, which can slow down the calculations significantly
