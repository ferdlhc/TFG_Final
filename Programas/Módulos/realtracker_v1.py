
import bifacial_radiance

"""
Defines parameters of real_tracker_v1 module
        
"""
name = 'real_tracker_v1'

numpanels = 1      # NÚMERO DE PANELES QUE POSEE EL MODULEOBJ

# DIMENSIONES DEL PANEL
x_width = 2.076/2  # ANCHO DEL PANEL A LO LARGO DEL EJE X, COINCIDENTE CON EJE DE GIRO
y_length = 2.094   # LARGO DEL PANEL A LO LARGO DEL EJE Y
z_thickness = 0.04 # ESPESOR DEL PANEL

# SEPARACIÓN EN CADA EJE
x_gap = 0.398
y_gap = 0
z_gap = 0.1545

# FACTOR DE BIFACIALIDAD DEL MÓDULO
bifaciality = 1    # SELECCIONADO 1 PERO MODIFICADO A POSTERIORI EN CÁLCULOS


# PARAMETROS DEL TORQUETUBE (BARRA DE TORSIÓN)
torquetube = True
dim_torquetube = 0.12
tubetype = 'Square'
material_torquetube = 'Metal_Grey'
axisofrotationTorqueTube = True

# MÓDULO CON CRISTAL
glass = False

# DICCIONARIO PASADO POR PARÁMETRO DEL TORQUETUBE
tubeParams={'diameter':dim_torquetube,'tubetype':tubetype, 'material':material_torquetube,'axisofrotation':True}

# CREACIÓN DEL MODULEOBJ
real_tracker_v1 = bifacial_radiance.RadianceObj().makeModule(name=name, x=x_width,
                                                             z = z_thickness, y=y_length,
                                                             bifi=bifaciality, 
                                                             tubeParams=tubeParams,
                                                             xgap=x_gap, ygap=y_gap,
                                                             zgap=z_gap, 
                                                             numpanels=numpanels,
                                                             rewriteModulefile=True,
                                                             glass=glass)

#real_tracker_v1.showModule()

"""
pitch = 6.2                 # m
albedo = 0.65                #'grass'(0,2) ground albedo
hub_height = 0.9            # m  
nMods = 2                   # Two modules per row.
nRows = 1                   # 1 rows
azimuth_ang = 90            # Facing east (for N-S tracking)
tilt=35

ObjRad = bifacial_radiance.RadianceObj("real_tracker_v1")

sceneDict={'tilt':tilt,'pitch':pitch,'hub_height':hub_height,'azimuth':azimuth_ang, 
              'nMods': nMods, 'nRows': nRows, 'appendRadfile':True}
SceneObj=ObjRad.makeScene(module=name, sceneDict=sceneDict)

SceneObj.showScene()

"""




    