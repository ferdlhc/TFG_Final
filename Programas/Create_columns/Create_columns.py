
def create_columns(name='Columns',sceneObj=None,ObjRad=None):
    """
        Add columns of the desired height and radius to the SceneObj passed.
        Adds 1 more column than the number of modules in each row so that each
        module is between 2 columns.
        Azimuth possibilities for the module are 0, 90, 180 or 270 (deg)
        
        Parameters
        ----------
        module : str
            String name of the file .rad created without ".rad".
        column height : float
            Value of the column's height (DEPRECATED).
            It is also set in the function as the hub_height of the SceneObj passed.
        column radius : float
            Value of the column's radius (DEPRECATED).
            It is also set in the function with the value of the torquetube diameter
            of the Module Obj contained in the SceneObj passed.
        sceneObj : SceneObj
            The SceneObj passed is the one desired to have the columns attached to itself.
        ObjRad: RadianceObj
            The RadianceObj passed is the one in charge of running ObjRad.appendtoScene(),
            so the columns get attached to the SceneObj.
    
    """

    import math
    import bifacial_radiance
    
    module=sceneObj.module
    nMods=sceneObj.sceneDict['nMods']
    nRows=sceneObj.sceneDict['nRows']
    pitch=sceneObj.sceneDict['pitch']
    #If hub height is passed -> Columns' height = hub_height
    #If clearence_height is passed instead -> Columns' height is calculated  using trigonometry
    if 'hub_height' in sceneObj.sceneDict:
        column_height=sceneObj.sceneDict['hub_height']
    elif 'clearance_height' in sceneObj.sceneDict:
        column_height = round((module.sceney/2)*math.sin(sceneObj.sceneDict['tilt']*math.pi/180) + sceneObj.sceneDict['clearance_height'], 2)
    else: print('There is No clearance or hub height specified in the SceneObj´s dictionary passed\n')

    column_radius=module.torquetube.diameter/2
    torquetubelength= (module.x + 2*module.xgap)*nMods
    
    if sceneObj.sceneDict['azimuth'] == 90:
        column1y = torquetubelength/2.0
        column_sep = torquetubelength/(nMods+1)
        
        text=''
        for i in range (0, nMods+1):
            text += f'\r\n! genrev Metal_Grey tube{i+1}row0 t*{column_height} {column_radius} 32 | xform -t 0 {column1y-column_sep*i} 0'
            
            if nRows % 2 == 0:
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{-j} t*{column_height} {column_radius} 32 | xform -t {pitch*j} {column1y-column_sep*i} 0'
                for j in range (1, math.ceil(nRows/2)+1):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{j} t*{column_height} {column_radius} 32 | xform -t {-pitch*j} {column1y-column_sep*i} 0'
                                
            elif nRows % 2 != 0:
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{-j} t*{column_height} {column_radius} 32 | xform -t {pitch*j} {column1y-column_sep*i} 0'
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{j} t*{column_height} {column_radius} 32 | xform -t {-pitch*j} {column1y-column_sep*i} 0'
                    
    elif sceneObj.sceneDict['azimuth'] == 180:
        column1x = torquetubelength/2.0
        column_sep = torquetubelength/(nMods+1)
        
        text=''
        for i in range (0, nMods+1):
            text += f'\r\n! genrev Metal_Grey tube{i+1}row0 t*{column_height} {column_radius} 32 | xform -t {column1x-column_sep*i} 0 0'
            
            if nRows % 2 == 0:
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{-j} t*{column_height} {column_radius} 32 | xform -t {column1x-column_sep*i} {-pitch*j} 0'
                for j in range (1, math.ceil(nRows/2)+1):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{j} t*{column_height} {column_radius} 32 | xform -t {column1x-column_sep*i} {pitch*j} 0'
                                
            elif nRows % 2 != 0:
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{-j} t*{column_height} {column_radius} 32 | xform -t {column1x-column_sep*i} {-pitch*j} 0'
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{j} t*{column_height} {column_radius} 32 | xform -t {column1x-column_sep*i} {pitch*j} 0'          

    elif sceneObj.sceneDict['azimuth'] == 0:
        column1x = -torquetubelength/2.0
        column_sep = -torquetubelength/(nMods+1)
        
        text=''
        for i in range (0, nMods+1):
            text += f'\r\n! genrev Metal_Grey tube{i+1}row0 t*{column_height} {column_radius} 32 | xform -t {column1x-column_sep*i} 0 0'
            
            if nRows % 2 == 0:
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{-j} t*{column_height} {column_radius} 32 | xform -t {column1x-column_sep*i} {pitch*j} 0'
                for j in range (1, math.ceil(nRows/2)+1):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{j} t*{column_height} {column_radius} 32 | xform -t {column1x-column_sep*i} {-pitch*j} 0'
                                
            elif nRows % 2 != 0:
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{-j} t*{column_height} {column_radius} 32 | xform -t {column1x-column_sep*i} {-pitch*j} 0'
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{j} t*{column_height} {column_radius} 32 | xform -t {column1x-column_sep*i} {pitch*j} 0'     

    elif sceneObj.sceneDict['azimuth'] == 270:
        column1y = -torquetubelength/2.0
        column_sep = -torquetubelength/(nMods+1)
        
        text=''
        for i in range (0, nMods+1):
            text += f'\r\n! genrev Metal_Grey tube{i+1}row0 t*{column_height} {column_radius} 32 | xform -t 0 {column1y-column_sep*i} 0'
            
            if nRows % 2 == 0:
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{-j} t*{column_height} {column_radius} 32 | xform -t {-pitch*j} {column1y-column_sep*i} 0'
                for j in range (1, math.ceil(nRows/2)+1):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{j} t*{column_height} {column_radius} 32 | xform -t {pitch*j} {column1y-column_sep*i} 0'
                                
            elif nRows % 2 != 0:
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{-j} t*{column_height} {column_radius} 32 | xform -t {-pitch*j} {column1y-column_sep*i} 0'
                for j in range (1, math.ceil(nRows/2)):
                    text += f'\r\n! genrev Metal_Grey tube{i+1}row{j} t*{column_height} {column_radius} 32 | xform -t {pitch*j} {column1y-column_sep*i} 0'    
                    
    else: print("Choose one of this values of Azimuth: 0, 90, 180 or 270\n")
    
    
    customObject = ObjRad.makeCustomObject(name,text)
    
    return customObject

    
