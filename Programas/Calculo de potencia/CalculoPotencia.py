import os
import pandas as pd
import bifacial_radiance


os.chdir('C:/Users/ferdl/Documents/bifacial_radiance/TFG_Final/Seguimiento/Anual/Sudafrica_Diciembre')
path = os.getcwd()
print("Cambio de directorio de trabajo a:", path)

resultfolder = os.path.join(path, 'results')
writefiletitle = "Mismatch_Results_Diciembre_Estandar.csv" 

portraitorlandscape='portrait' 
bififactor=0
numcells= 96
downsamplingmethod = 'byCenter'
bifacial_radiance.mismatch.analysisIrradianceandPowerMismatch(testfolder=resultfolder,
                                                      writefiletitle=writefiletitle, 
                                              portraitorlandscape=portraitorlandscape, 
                                                              bififactor=bififactor, 
                                                              numcells=numcells)
read_file = pd.read_csv(r'Mismatch_Results_Diciembre_Estandar.csv')
read_file.to_excel('Mismatch_Results_Diciembre_Estandar.xlsx')