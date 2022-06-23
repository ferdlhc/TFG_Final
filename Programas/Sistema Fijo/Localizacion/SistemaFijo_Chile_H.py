#---------------------------------------------------------#
#------------ Comparador Sistema Fijo Chile -------------#
#---------------------------------------------------------#

#------------------- RECURSOS EXTERNOS -------------------#

import os
import matplotlib.pyplot as plt
import pandas as pd
import bifacial_radiance
#import real_tracker_v1
import Create_columns

#---------------------------------------------------------#
#------------ CAMBIO DE DIRECTORIO DE TRABAJO ------------#
#---------------------------------------------------------#

#os.mkdir('C:/Users/ferdl/Documents/bifacial_radiance/TFG_Final/Sistemas_Fijos/Localizacion/Chile_Horizontal')
os.chdir('C:/Users/ferdl/Documents/bifacial_radiance/TFG_Final/Sistemas_Fijos/Localizacion/Chile_Horizontal')
path = os.getcwd()
print("Cambio de directorio de trabajo a:", path)

simulationName="Chile_Horizontal"


#---------------------------------------------------------#
#------------------ DATOS LOCALIZACION -------------------#
#---------------------------------------------------------#

#LOCALIZACIÓN: Antofagasta, Chile
latitude = -23.43
longitude = -70.43
albedo = 0.65

print('Datos localizacion inicializados:')
print('latitud: ',latitude)
print('longitud: ',longitude)


#---------------------------------------------------------#
#--------------------- FECHA EPWFILE ---------------------#
#---------------------------------------------------------#

starttime = '03_20'
endtime = '03_20'


#---------------------------------------------------------#
#---------------------- FECHA LOOP -----------------------#
#---------------------------------------------------------#

starttime_loop = pd.to_datetime('2021-03-20 7:0:0 -4')
endtime_loop =pd.to_datetime('2021-03-20 19:0:0 -4')


#---------------------------------------------------------#
#------------------- PARÁMETROS MÓDULO -------------------#
#---------------------------------------------------------#

module_type = 'real_tracker_v1'     # Nombre del módulo

"""
x_width = 2.076         #ANCHO DEL MÓDULO A LO LARGO DEL EJE DEL TORQUE TUBE O DE LA ESTRUCTURA
y_length = 2.094
z_thickness = 0.04
bifaciality = 1
torquetube = True
dim_torquetube = 0.12
tubetype = 'Square'
material_torquetube = 'Metal_Grey'
numpanels = 1
x_gap = 0.398
y_gap = 0
z_gap = 0.1545
axisofrotationTorqueTube = True
glass = False
tubeParams={'diameter':dim_torquetube,'tubetype':tubetype, 'material':material_torquetube,'axisofrotation':True}
"""


#---------------------------------------------------------#
#------------------- PARÁMETROS ESCENA -------------------#
#---------------------------------------------------------#

pitch = 6.2                 # m
albedo = 0.65                #'grass'(0,2) ground albedo
hub_height = 0.9            # m  
nMods = 6                   # six modules per row.
nRows = 3                   # 3 rows
azimuth_ang = 0            # Facing east (for N-S tracking)

tilt = 0


#---------------------------------------------------------#
#------------------ PARÁMETROS ANÁLISIS ------------------#
#---------------------------------------------------------#

modWanted = 2
rowWanted = 1
sensorsy = 3
sensorsx = 3

#---------------------------------------------------------#
#------------------------ PROGRAMA -----------------------#
#---------------------------------------------------------#


#--------------- CREACIÓN DE RADIANCEOBJ -----------------#

ObjRad = bifacial_radiance.RadianceObj(simulationName)
ObjRad.setGround(albedo)

print ("ObjRad creado: %s " % ObjRad.name)
print ("Suelo creado con albedo de valor ",albedo," con nombre de archivo ", ObjRad.ground.material_file)

#------------------ LECTURA DE EPWFILE -------------------#

#epwfile = ObjRad.getEPW(lat=latitude, lon=longitude)
epwfile = 'EPWs\\CHL_Antofagasta.854420_IWEC.epw'
metdata = ObjRad.readWeatherFile(weatherFile=epwfile, starttime=starttime, endtime=endtime) 
print ("EPWfile obtenido y datos guardados para las fechas: ", metdata.datetime)
 
#----------------- CREACIÓN DEL MÓDULO ------------------#

real_tracker_v1 = bifacial_radiance.RadianceObj().makeModule(name=module_type)

CW = real_tracker_v1.sceney # Collector Width
gcr = CW / pitch  

#---------------------- LOOP DIARIO ----------------------#

"""INICIO VARIABLE DE CONTROL DE LOOP"""
j=0

#----------------- INICIALIZACIÓN FECHA ------------------#

starttimeindex = metdata.datetime.index(starttime_loop)
endtimeindex = metdata.datetime.index(endtime_loop)

#----------------- DECLARACIÓN VECTORES ------------------#

sceneDict=[]
sceneObj=[]
octfile=[]
ObjAnalysis=[]
frontscan=[];backscan=[]
results=[]
results_df=[]
media_front=[]
media_back=[]

"""INICIO DE LOOP""" 
for timess in range (starttimeindex, endtimeindex+1):
    j+=1
    
    # Creación Cielo   
    ObjRad.gendaylit(timess, metdata, True) 

    # Creación de Escena
    sceneDict.append({'tilt':tilt,'pitch':pitch,'hub_height':hub_height,'azimuth':azimuth_ang, 
                  'nMods': nMods, 'nRows': nRows, 'appendRadfile':True})
    sceneObj.append(ObjRad.makeScene(module=module_type, sceneDict=sceneDict[j-1], radname=module_type+f'_{j}'))   #makeScene creates a .rad file with 6 modules per row, 3 rows.
    
    # Creación de Columnas
    if j==1:
        customObject = Create_columns.create_columns(name='Columns',sceneObj=sceneObj[j-1],ObjRad=ObjRad)
    
    # Adición de Columnas a la escena
    ObjRad.appendtoScene(radfile=sceneObj[j-1].radfiles, customObject=customObject, text="!xform -rz 0")
    
    # Creación de OctFile
    octfile.append(ObjRad.makeOct(filelist=[ObjRad.materialfiles[0], ObjRad.skyfiles[0],sceneObj[j-1].radfiles],
                                  octname=ObjRad.name+f'_{j}'))
    
    # Análisis
    ObjAnalysis.append(bifacial_radiance.AnalysisObj(octfile[j-1],name=ObjRad.basename))          
    aux_frontscan, aux_backscan = ObjAnalysis[j-1].moduleAnalysis(sceneObj[j-1],modWanted=modWanted,rowWanted=rowWanted,
                                                                  sensorsy=sensorsy, sensorsx=sensorsx)
    frontscan.append(aux_frontscan);backscan.append(aux_backscan)
    
    # Resultados
    results.append(ObjAnalysis[j-1].analysis(octfile[j-1], ObjAnalysis[j-1].name+f'_{j}',frontscan[j-1],backscan[j-1],False))
    results_df.append(bifacial_radiance.load.read1Result(f'results/irr_Chile_Horizontal_{j}.csv'))
    results_df[j-1]=bifacial_radiance.load.cleanResult(results_df[j-1])
    media_front.append(results_df[j-1]['Wm2Front'].mean())
    media_back.append(results_df[j-1]['Wm2Back'].mean())
    
    
"""FINAL DEL LOOP"""    

df_media_front=pd.DataFrame(data=media_front)
df_media_back=pd.DataFrame(data=media_back)

with pd.ExcelWriter('C:/Users/ferdl/Documents/bifacial_radiance/TFG_Final/Sistemas_Fijos/Localizacion/Resultados_Irradiancia/Chile_Horizontal.xlsx') as writer:
    df_media_front.to_excel(writer,sheet_name='Front_Irradiance')
    df_media_back.to_excel(writer,sheet_name='Back_Irradiance')


plt.plot(media_front)
plt.plot(media_back)

resultfolder = os.path.join(path, 'results')
writefiletitle = "Mismatch_Results.csv" 

portraitorlandscape='portrait' # Options are 'portrait' or 'landscape'
bififactor=1 # Bifaciality factor DOES matter now, as the rear irradiance values will be multiplied by this factor.
numcells= 72# Options are 72 or 96 at the moment.
downsamplingmethod = 'byCenter' # Options are 'byCenter' or 'byAverage'.
bifacial_radiance.mismatch.analysisIrradianceandPowerMismatch(testfolder=resultfolder,
                                                              writefiletitle=writefiletitle, 
                                                              portraitorlandscape=portraitorlandscape, 
                                                              bififactor=bififactor, 
                                                              numcells=numcells)

#--------------- OBTENCIÓN DE DATOS EN EXCEL -------------#

read_file = pd.read_csv(r'Mismatch_Results.csv')
read_file.to_excel('Mismatch_Results.xlsx')



#------------------ VISUALIZAR OCTFILE ------------------#
#!rvu -vf views\front.vp -e .01 -pe 0.3 -vp 1 -7.5 12 Tracker_1_1.oct	# Desde el Frente
#!rvu -vf views\side.vp -e .01 -pe 0.3 -vp 1 -7.5 12 Tracker_1_1.oct	# Desde el Lateral    
 
#!rvu -vf views\front.vp -e .01 -pe 0.3 -vp 1 -7.5 12 Tracker_1_2.oct	# Desde el Frente
#!rvu -vf views\side.vp -e .01 -pe 0.3 -vp 1 -7.5 12 Tracker_1_2.oct	# Desde el Lateral    
