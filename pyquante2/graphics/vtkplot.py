import numpy as np

vtk_template = """\
# vtk DataFile Version 2.0
VTK file autogenerated for nemo3d via nemo_evec_to_vtk script
ASCII
DATASET STRUCTURED_POINTS
DIMENSIONS %(nx)d %(ny)d %(nz)d
ORIGIN %(ox)f %(oy)f %(oz)f
SPACING %(sx)f %(sy)f %(sz)f
POINT_DATA %(npts)d
%(recordstrings)s
"""

record_template = """\
SCALARS %(name)s float 1
LOOKUP_TABLE default
%(datastring)s
"""

def iterator_3d(nxyz,oxyz,sxyz):
    nx,ny,nz = nxyz
    sx,sy,sz = sxyz
    ox,oy,oz = oxyz
    for i in range(nx):
        x = ox + i*sx
        for j in range(ny):
            y = oy + j*sy
            for k in range(nz):
                z = oz + k*sz
                yield x,y,z
    return

def make_recordstrings(records,names):
    lines = []
    for name,record in zip(names,records):
        lines.append(make_recordstring(record,name))
    return "\n".join(lines)

def make_recordstring(record,name):
    datastring = "\n".join("%f" % fi for fi in record)
    return record_template % dict(name=name,datastring=datastring)

def write_vtk(records,nxyz,oxyz,sxyz,names=None,fname = "pyq_orb.vtk"):
    sx,sy,sz = sxyz
    ox,oy,oz = oxyz
    nx,ny,nz = nxyz
    npts = nx*ny*nz
    if not names:
        names = ["orb%d" % (i+1) for i in range(len(records))]
    recordstrings = make_recordstrings(records,names)
    open(fname,"w").write(vtk_template % locals())
    return

def eval_orb(orb,bfs,nxyz,oxyz,sxyz):
    nx,ny,nz = nxyz
    fxyz = np.zeros(nx*ny*nz,'d')
    for c,bf in zip(orb,bfs):
        for i,(x,y,z) in enumerate(iterator_3d(nxyz,oxyz,sxyz)):
            fxyz[i] += c*bf(x,y,z)
    return fxyz

def vtk_orbs(atoms,orbs,bfs,npts=8):
    xmin,xmax,ymin,ymax,zmin,zmax = atoms.bbox()
    oxyz = xmin,ymin,zmin
    sxyz = (xmax-xmin)/(npts-1.),(ymax-ymin)/(npts-1.),(zmax-zmin)/(npts-1.)
    nxyz = npts,npts,npts
    records = []
    for orb in orbs.T: # transpose makes iterations work right
        fxyz = eval_orb(orb,bfs,nxyz,oxyz,sxyz)
        records.append(fxyz)
    write_vtk(records,nxyz,oxyz,sxyz)
    return

def plot_orb():
    from pyquante2 import basisset,h2
    bfs = basisset(h2,'sto3g')
    orbs = np.array([[1.0,0.0],
                     [0.0,-1.0]],'d')

    vtk_orbs(h2,orbs,bfs)
    return

def plot_orb2():
    from pyquante2 import basisset,h2
    bfs = basisset(h2,'sto3g')
    orbs = np.array([[1.0,1.0],
                     [1.0,-1.0]],'d')

    vtk_orbs(h2,orbs,bfs)
    return

if __name__ == '__main__':
    plot_orb()
