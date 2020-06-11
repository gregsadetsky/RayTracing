import envexamples
from raytracing import *

nRays = 1000000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMin=minHeight, yMax=maxHeight)
path.append(Space(d=4))
path.append(Lens(f=4,diameter=2.5))
path.append(Space(d=4+25))
path.append(Lens(f=25, diameter=7.5))
path.append(Space(d=20+9+5))
path.append(Lens(f=9, diameter=8))
path.append(Space(d=9))
path.append(Aperture(diameter=2, label='Camera'))
path.display(onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=False)
 