import bifacial_radiance
import math

name = 'mod_pvmismatch'

numpanels = 1   #Número de "paneles" que posee el ModuleObj

# Tamaño del Panel
"""
x_width = 2.076         #ANCHO DEL MÓDULO A LO LARGO DEL EJE DEL TORQUE TUBE O DE LA ESTRUCTURA
y_length = 2.094
"""

z_thickness = 0.04

# Separación en los ejes
x_gap = 0.398           # A lo largo del Eje X (Torque tube)
y_gap = 0               # A lo largo del Eje Y 
z_gap = 0.1545          # Respecto del EjeZ, es decir del centro del torquetube

# Factor de bifacialidad
bifaciality = 1

# Parámetros del TorqueTube (Barra de torsión)
torquetube = True       # No hace nada, es para que el lector sepa que existe barra de torsión
dim_torquetube = 0.12
tubetype = 'Square'
material_torquetube = 'Metal_Grey'
axisofrotationTorqueTube = True


# Parámetros de célula
numcellsx = 12
numcellsy = 8
# Células totales 8*12=96
cell_area=153.33/10000
xcell = math.sqrt(cell_area)
ycell = math.sqrt(cell_area)
xcellgap = 0.01
ycellgap = 0.01


glass = False



tubeParams={'diameter':dim_torquetube,'tubetype':tubetype, 'material':material_torquetube,'axisofrotation':True}
cellModule={'numcellsx':numcellsx,'numcellsy':numcellsy,'xcell':xcell,'ycell':ycell,'xcellgap':xcellgap,'ycellgap':ycellgap}

mod_pvmismatch = bifacial_radiance.RadianceObj().makeModule(name=name, z = z_thickness, bifi=bifaciality, 
                                                             tubeParams=tubeParams, cellModule=cellModule,
                                                             xgap=x_gap, ygap=y_gap, zgap=z_gap, 
                                                             numpanels=numpanels, rewriteModulefile=True,  
                                                             glass=glass)
mod_pvmismatch.showModule()



