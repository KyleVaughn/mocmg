import mocmg
import sys

pi = 3.141592653589793

mocmg.initialize()
nodes, elements, elsets = mocmg.readAbaqusINP(sys.argv[1])
# Give mesh info
num_elem = 0
for e in elements:
    num_elem = num_elem + len(e[1])
print("\nElements: ", num_elem)

mesh = mocmg.Mesh(nodes, elements, elsets)
total_area = mesh.getSetArea("GRID_L1_001_001")
uo2 = mesh.getSetArea("MATERIAL_UO2-3.3")
mox70 = mesh.getSetArea("MATERIAL_MOX-7.0")
mox43 = mesh.getSetArea("MATERIAL_MOX-4.3")
mox87 = mesh.getSetArea("MATERIAL_MOX-8.7")
fis = uo2 + mox70 + mox43 + mox87
print(f"Total mesh area: {total_area}")
print("Total mesh area error: ", total_area - 64.26 ** 2)
print(f"Fissile mesh area: {fis}")
print("Fissile mesh area error: ", fis - pi * 0.54 ** 2 * (17 ** 2 - 25) * 4, "\n")

del mesh
mocmg.writeXDMF("c5g7.xdmf", nodes, elements, elsets)
mocmg.finalize()
