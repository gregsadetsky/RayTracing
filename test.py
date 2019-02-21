from raytracing import *
import raytracing.thorlabs as th
import raytracing.edmundoptics as eo
import raytracing.olympus as olymp

lens = Lens(f=5)
path = MatrixGroup()
path.append(lens)
path.append(Space(3))
path.append(lens)
path.append(Space(0.1))
path.append(lens)
path.append(Space(3))

print("EFL", path.effectiveFocalLengths())
print("PP1 PP2", path.principalPlanePositions(z=0))
print("BFL", path.backFocalLength())
print("FFL", path.frontFocalLength())
print("V1", path.frontVertex)
print("V2", path.backVertex)



obj = olymp.LUMPLFL40X()
print("EFL", obj.effectiveFocalLengths())
print("PP1 PP2" , obj.principalPlanePositions(z=0))
print("BFL", obj.backFocalLength())
print("FFL", obj.frontFocalLength())


lens = eo.EO_33_921()
print("EFL", lens.effectiveFocalLengths())
print("PP1 PP2" , lens.principalPlanePositions(z=0))
print("BFL", lens.backFocalLength())
print("FFL", lens.frontFocalLength())
