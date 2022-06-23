#---------------------------------------------------------#
#-------- SISTEMA SEGUIDOR SUDÁFRICA ALBEDO = 0.12 -------#
#---------------------------------------------------------#

#------------------- RECURSOS EXTERNOS -------------------#

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import bifacial_radiance
#import real_tracker_v1

#---------------------------------------------------------#
#------------ CAMBIO DE DIRECTORIO DE TRABAJO ------------#
#---------------------------------------------------------#

os.mkdir('C:/Users/ferdl/Documents/bifacial_radiance/TFG_Final/Seguimiento/Anual/Sudafrica_Julio')
os.chdir('C:/Users/ferdl/Documents/bifacial_radiance/TFG_Final/Seguimiento/Anual/Sudafrica_Julio')
path = os.getcwd()
print("Cambio de directorio de trabajo a:", path)

simulationName="Sudafrica_Julio"


#---------------------------------------------------------#
#------------------ DATOS LOCALIZACION -------------------#
#---------------------------------------------------------#

#LOCALIZACIÓN: Ciudad del Cabo, Sudafrica
latitude = -33.925
longitude = 18.426

print('Datos localizacion inicializados:')
print('latitud: ',latitude)
print('longitud: ',longitude)


#---------------------------------------------------------#
#--------------------- FECHA EPWFILE ---------------------#
#---------------------------------------------------------#

starttime = '07_01'
endtime = '08_01'


#---------------------------------------------------------#
#------------------- PARÁMETROS MÓDULO -------------------#
#---------------------------------------------------------#

module_type = 'mod_pvmismatch'     # Nombre del módulo


#---------------------------------------------------------#
#------------------ PARÁMETROS SEGUIDOR ------------------#
#---------------------------------------------------------#
tracker_azimuth = 180       # Para tracker 180 es facing EAST porque se refiere a ángulo del torque tube no del módulo
tracker_angledelta = 2.5
tracker_limit_angle = 90    # Ángulo límite de subida y bajada
tracker_backtrack = True
tracker_cumulativesky = False


#---------------------------------------------------------#
#------------------- PARÁMETROS ESCENA -------------------#
#---------------------------------------------------------#

pitch = 6.2                 # m
albedo = 0.65               # Cemento con barniz
hub_height = 0.9            # m
nMods = 6                   # six modules per row.
nRows = 3                   # 3 rows
azimuth_ang = 90            # Facing east (for N-S tracking)


#---------------------------------------------------------#
#------------------ PARÁMETROS ANÁLISIS ------------------#
#---------------------------------------------------------#

modWanted = 3
rowWanted = 2
sensorsy = 12
sensorsx = 8

#---------------------------------------------------------#
#------------------------ PROGRAMA -----------------------#
#---------------------------------------------------------#


#--------------- CREACIÓN DE RADIANCEOBJ -----------------#

ObjRad = bifacial_radiance.RadianceObj(simulationName)
ObjRad.setGround(albedo)

print ("ObjRad creado: %s " % ObjRad.name)
print ("Suelo creado con albedo de valor ",albedo," con nombre de archivo ", ObjRad.ground.material_file)

#------------------ LECTURA DE EPWFILE -------------------#

epwfile = ObjRad.getEPW(lat=latitude, lon=longitude)
#epwfile = 'EPWs\\ZAF_Cape.Town.688160_IWEC.epw'
metdata = ObjRad.readWeatherFile(weatherFile=epwfile, starttime=starttime, endtime=endtime) 
print ("EPWfile obtenido y datos guardados para las fechas: ", metdata.datetime)
 
#----------------- CREACIÓN DEL MÓDULO ------------------#

real_tracker_v1 = ObjRad.makeModule(name=module_type)

CW = real_tracker_v1.sceney # Collector Width
gcr = CW / pitch  


#---------------- SETEO DE LA ESCENA -----------------#

sceneDict = {'pitch':pitch,'hub_height':hub_height,'azimuth':azimuth_ang, 'nMods': nMods, 'nRows': nRows}


#------------------ SETEO DEL TRACKER -------------------#

trackerdict=ObjRad.set1axis(metdata=metdata, azimuth=tracker_azimuth,
                            limit_angle = tracker_limit_angle,
                            angledelta=tracker_angledelta,
                            backtrack = tracker_backtrack, 
                            gcr = gcr, cumulativesky = tracker_cumulativesky)


#------------------ CREACIÓN DEL CIELO ------------------#

trackerdict=ObjRad.gendaylit1axis(metdata=metdata, trackerdict=trackerdict, debug=True)


#---------------- CREACIÓN DE LA ESCENA -----------------#

trackerdict=ObjRad.makeScene1axis(trackerdict=trackerdict,module=real_tracker_v1,
                                  sceneDict=sceneDict, cumulativesky=False)


#------------------ CREACIÓN DEL OCTFILE ------------------#

trackerdict=ObjRad.makeOct1axis(trackerdict=trackerdict)


#----------------- CREACIÓN DEL ANALISIS ------------------#

analisis=ObjRad.analysis1axis(trackerdict=trackerdict,
                              modWanted=modWanted,
                              rowWanted=rowWanted,
                              sensorsy = sensorsy,
                              sensorsx=sensorsx,
                              debug=False)

front=[]
back=[]

for key in analisis:
    front.append(numpy.mean(analisis[key]['Wm2Front']))
    back.append(numpy.mean(analisis[key]['Wm2Back']))

df_media_front=pd.DataFrame(data=front)
df_media_back=pd.DataFrame(data=back)


with pd.ExcelWriter('C:/Users/ferdl/Documents/bifacial_radiance/TFG_Final/Seguimiento/Anual/Resultados_Irradiancia/Sudafrica_Julio.xlsx') as writer:
    df_media_front.to_excel(writer,sheet_name='Front_Irradiance')
    df_media_back.to_excel(writer,sheet_name='Back_Irradiance')


plt.plot(front)
plt.plot(back)