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
                            Water Model (cSPCE/cTIP3P)
      --dieps DIEPS         Dielectric Constant (default = 78.44)
      --n N                 Number of Cores (default = 1)
</details>

1. rism3d.py takes in either PDB or SDF file formats. Topology and coordinate files can be specified, else it will be generated from provided input files.

2. Placevent is used to carry out water placement using oxygen density distribution file from 3D RISM

3. Output files include solute free energy denisty file (exchem.mol.1.dx)
