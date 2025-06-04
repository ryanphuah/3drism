
import parmed as pmd
import argparse
import subprocess
import os

def rism3d(pdb_in,prm_in=None,coord_in=None,pdb_out=None,water_model='cTIP3P',dieps=78.44,n=1):
    if f'{pdb_in.split('.')[1]}'=='sdf':
        convertedpdb=f'{pdb_in.split('.')[0]}.pdb'
        with open(convertedpdb, "w") as f:
            result = subprocess.run(["obabel",pdb_in,"-O", convertedpdb],stdout=f)
        pdb_in=convertedpdb
    if pdb_out is None: rism3dout=f'{pdb_in.split('.')[0]}.out'
    else: rism3dout=f'{pdb_out}.out'
    
    #generate topology and coordinate files
    if prm_in is None and coord_in is None:
        #generate parameter and coord file if not specified
        amberout=f'{pdb_in.split('.')[0]}_amberfile.pdb'
        result=subprocess.run(["pdb4amber", "-i", pdb_in, "-o", amberout, "-d", "--no-conect", "-p"],capture_output=True, text=True)
        if result.returncode != 0:
            print("Error running pdb4amber:")
            print(result.stderr)
        else:
            print(f"pdb4amber successful. Output written to {amberout}")
        pdb_in=f'{pdb_in.split('.')[0]}_tleapfile.pdb'
        prm_in=f'{pdb_in.split('.')[0]}.prmtop'
        coord_in=f'{pdb_in.split('.')[0]}.rst7'
        
        tleap_input = f"""
    source leaprc.protein.ff14SB
    mol = loadpdb {amberout}
    savepdb mol {pdb_in}
    saveamberparm mol {prm_in} {coord_in}
    quit
    """
        with open("tleap_fix_protein.in", "w") as f:
            f.write(tleap_input)
        
        result = subprocess.run(["tleap", "-f", "tleap_fix_protein.in"], capture_output=True, text=True)

        if result.returncode != 0:
            print("Error running tleap:")
            print(result.stderr)
        else:
            print(f"Force field applied. Files to use for 3D-RISM are {pdb_in}, {prm_in} and {coord_in}")
            os.remove("tleap_fix_protein.in")  # Clean up if you like
        
    #1DRISM
    rism1d_input=f"""
&PARAMETERS
OUTLIST='gx', THEORY='DRISM', CLOSURE='PSE4',
NR=16384, DR=0.025,
MDIIS_NVEC=20, MDIIS_DEL=0.3, TOLERANCE=1.e-12,
KSAVE=-1, maxstep=10000,
TEMPERATURE=298.15, DIEPS={dieps}
NSP=1
/
&SPECIES
units = 'M' !unit in mol/L
DENSITY = 55.5D0,
MODEL="{water_model}.mdl"
/
"""
    rism1dmdl=f'{water_model}.mdl'
    rism1dout=f'{water_model}.out'
    os.system(f'cp "$AMBERHOME/dat/rism1d/mdl/{water_model}.mdl" "{rism1dmdl}"')
    with open(water_model+".inp", "w") as f:
        f.write(rism1d_input)
    with open(rism1dout, "w") as f:
        result=subprocess.run(["rism1d",water_model,">", rism1dout],stdout=f)
    if result.returncode != 0:
        print("Error running 1D RISM:")
        print(result.stderr)
    else:
        print(f"1D RISM successful. Output written to {rism1dout}")
        os.remove(rism1dmdl)
        os.remove(water_model+".inp")

    #3D RISM
    rism3d_input = f"""
mpiexec -n {n} rism3d.snglpnt.MPI --pdb {pdb_in} --prmtop {prm_in} --rst {coord_in} --xvv {water_model}.xvv --closure kh,pse2,pse3 --buffer 48 --exchem exchem --molReconstruct --volfmt dx --grdspc 0.5,0.5,0.5 --tolerance 1e-4,1e-6 --verbose 2 --progress --guv g > {rism3dout}
"""
    with open("3drism.sh", "w") as f:
        f.write(rism3d_input)
    with open(rism3dout, "w") as f:
        result = subprocess.run(["sh","./3drism.sh"],stdout=f)
    if result.returncode != 0:
        print("Error running 3D RISM:")
        print(result.stderr)
    else:
        print(f"3D RISM successful. Output written to {rism3dout}")
        os.remove("3drism.sh")

    #placevent
    placevent_output=f'{rism3dout.split('.')[0]}_placedwaters.pdb'
    with open(placevent_output, "w") as f:
        result = subprocess.run(["python","placevent.py","g.O.1.dx","55.5",">",placevent_output],stdout=f)
    if result.returncode != 0:
        print("Error running Placevent:")
        print(result.stderr)
    else:
        print(f"Placevent successful. Output written to {placevent_output}")

def main():
    parser= argparse.ArgumentParser(description='3D-RISM')
    parser.add_argument('pdb_in',help='Input pdb')
    parser.add_argument('--prm_in',help='Input parameter file',default=None)
    parser.add_argument('--coord_in',help='Input coordinate file', default=None)

    parser.add_argument('--pdb_out',help='Output pdb name',default=None)
    parser.add_argument('--water_model',help='Water Model (cSPCE/cTIP3P) (default = cTIP3P)',default='cTIP3P')
    parser.add_argument('--dieps',help='Dielectric Constant (default = 78.44)',default=78.44)
    parser.add_argument('--n',help='Number of Cores (default = 1)',default=1)
    args = parser.parse_args()
    rism3d(**vars(args))

if __name__=="__main__":
    main()
    
