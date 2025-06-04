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
