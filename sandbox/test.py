import gmsh
import mocmg
import logging as log
import logging.config as log.config

lc=1e-1

log.config.fileConfig('setup.cfg')

#log.basicConfig(filename='myapp.log',\
#format='%(asctime)s:%(message)s',\
#        datefmt='%m/%d/%Y %I:%M:%S %p',\
#        level=log.DEBUG)

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
mocmg.addDiskLattice(3)
mocmg.overlayRectGrid(3,3)
gmsh.model.mesh.setSize(gmsh.model.getEntities(0), lc)
gmsh.model.mesh.generate(2)
#gmsh.fltk.run()
gmsh.finalize()
