from owlready2 import *
import random
import math
import csv

# Cargamos la ontología desde el archivo OWL
onto = get_ontology("/Users/juliosp/Desktop/TFG/onto.rdf").load()

factores_mitigacion = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
posibles_impactos = ["MB", "B", "M", "A", "MA"]

# Función para convertir letras a números
def letra_a_numero(letra):
    if letra == "MB":
        return 1
    elif letra == "B":
        return 2
    elif letra == "M":
        return 3
    elif letra == "A":
        return 4
    elif letra == "MA":
        return 5
    else:
        return 0  # En caso de que la letra no esté en la escala, devolvemos 0 como valor por defecto

# Función para convertir números a letras
def numero_a_letra(numero):
    if numero == 1:
        return "MB"
    elif numero == 2:
        return "B"
    elif numero == 3:
        return "M"
    elif numero == 4:
        return "A"
    elif numero == 5:
        return "MA"
    else:
        return "MB"  # En caso de que el número no esté en la escala, devolvemos una cadena vacía como valor por defecto

def calcular_riesgo_potencial(probabilidad, impacto):
    tabla_riesgo = {
        'MA': {'MA': 'MA', 'A': 'MA', 'M': 'MA', 'B': 'MA', 'MB': 'A'},
        'A': {'MA': 'MA', 'A': 'MA', 'M': 'A', 'B': 'A', 'MB': 'M'},
        'M': {'MA': 'A', 'A': 'A', 'M': 'M', 'B': 'M', 'MB': 'B'},
        'B': {'MA': 'M', 'A': 'M', 'M': 'B', 'B': 'B', 'MB': 'MB'},
        'MB': {'MA': 'B', 'A': 'B', 'M': 'MB', 'B': 'MB', 'MB': 'MB'}
    }
    
    return tabla_riesgo[impacto][probabilidad]

def calcular_riesgo_residual(factor_mitigacion, riesgo_potencial):
    
    if factor_mitigacion <= 0.2:
        factor_str = 'MB'
    elif factor_mitigacion <= 0.4:
        factor_str = 'B'
    elif factor_mitigacion <= 0.6:
        factor_str = 'M'
    elif factor_mitigacion <= 0.8:
        factor_str = 'A'
    else:
        factor_str = 'MA'
    
    tabla_riesgo = {
        'MA': {'MA': 'B', 'A': 'MB', 'M': 'MB', 'B': 'MB', 'MB': 'MB'},
        'A': {'MA': 'M', 'A': 'B', 'M': 'MB', 'B': 'MB', 'MB': 'MB'},
        'M': {'MA': 'A', 'A': 'M', 'M': 'B', 'B': 'MB', 'MB': 'MB'},
        'B': {'MA': 'MA', 'A': 'A', 'M': 'M', 'B': 'MB', 'MB': 'MB'},
        'MB': {'MA': 'MA', 'A': 'A', 'M': 'M', 'B': 'B', 'MB': 'MB'}
    }
    
    return tabla_riesgo[factor_str][riesgo_potencial]

# Función para calcular la media de los riesgos que afectan a un activo
def calcular_media_riesgos_para_activo(activo):
    # Inicializa la suma total de los riesgos
    suma_riesgos = 0
    # Inicializa el contador de los riesgos
    contador_riesgos = 0
    
    # Recorre la relación sonAfectadosPor para obtener los incidentes que afectan al activo
    for incidente in activo.sonAfectadosPor:
        # Obtén todas las amenazas generadas por el incidente
        amenazas = incidente.generan
        # Recorre las amenazas y suma los valores de riesgo
        for amenaza in amenazas:
            # Suma el valor del atributo Riesgo de la amenaza, convertido a número
            suma_riesgos += letra_a_numero(amenaza.Riesgo)
            # Incrementa el contador de riesgos
            contador_riesgos += 1
    
    # Calcula la media de los riesgos y conviértela de número a letra
    if contador_riesgos != 0:
        media_riesgos = suma_riesgos / contador_riesgos
        media_riesgos_letra = numero_a_letra(round(media_riesgos))  # Redondeamos antes de convertir a letra
    else:
        media_riesgos_letra = "MB"  # Si no hay riesgos, asignamos el valor mínimo
    
    return media_riesgos_letra
    
# Función para establecer el atributo "Riesgo" con el valor calculado para cada activo
def establecer_riesgo_para_todos_los_activos():
    # Recorre todas las instancias de la clase Activos
    for activo in onto.Activos.instances():
        # Calcula la media de los riesgos para el activo
        media_riesgos_letra = calcular_media_riesgos_para_activo(activo)
        # Establece el atributo "Riesgo" con el valor calculado para el activo
        activo.Riesgo = media_riesgos_letra
        
# Definimos las clases en la ontología
with onto:
    class Contramedidas(Thing):
        pass
    
    class Riesgos(Thing):
        pass

    class Riesgos_Potencial(Riesgos):
        pass

    class Riesgos_Residual(Riesgos):
        pass
    
    class Amenazas(Thing):
        pass
    
    class Incidentes(Thing):
        pass

    class Activos(Thing):
        pass
    
    class HW(Activos):
        pass
    
    class Asistentes_Virtuales(HW):
        pass
    
    class Bombillas(HW):
        pass
    
    class Camaras(HW):
        pass
    
    class Enchufes(HW):
        pass
    
    class Raspberry(HW):
        pass
    
    class Robots(HW):
        pass
    
    class Sensores(HW):
        pass
    
    class TVs(HW):
        pass
    
    class Timbres(HW):
        pass
    
    class Ventilador(HW):
        pass
    
    class Altavoces(HW):
        pass
    
    class Centro_Control(HW):
        pass

    # Definimos las propiedades de objeto para las relaciones
    # Riesgos es contrarrestado por Contramedidas
    class esContrarrestadoPor(ObjectProperty):
        domain = [onto.Riesgos]
        range = [onto.Contramedidas]

    # Contramedidas contrarrestan Riesgos
    class contrarrestan(ObjectProperty):
        domain = [onto.Contramedidas]
        range = [onto.Riesgos]

    # Amenazas provocan Riesgos
    class provocan(ObjectProperty):
        domain = [onto.Amenazas]
        range = [onto.Riesgos]

    # Riesgos sonProvocados por Amenazas
    class sonProvocadosPor(ObjectProperty):
        domain = [onto.Riesgos]
        range = [onto.Amenazas]

    # Incidentes generan Amenazas
    class generan(ObjectProperty):
        domain = [onto.Incidentes]
        range = [onto.Amenazas]

    # Amenazas sonGenerados por Incidentes
    class sonGenerados(ObjectProperty):
        domain = [onto.Amenazas]
        range = [onto.Incidentes]

    # Incidentes afectan Activos
    class afectan(ObjectProperty):
        domain = [onto.Incidentes]
        range = [onto.Activos]

    # Activos sonAfectadosPor Incidentes
    class sonAfectadosPor(ObjectProperty):
        domain = [onto.Activos]
        range = [onto.Incidentes]
        
    # Definimos las propiedades de datos
    class Header_Length(DataProperty, FunctionalProperty):
        namespace = onto

    class Protocol_Type(DataProperty, FunctionalProperty):
        namespace = onto

    class Srate(DataProperty, FunctionalProperty):
        namespace = onto

    class Tot_Sum(DataProperty, FunctionalProperty):
        namespace = onto

    class Min(DataProperty, FunctionalProperty):
        namespace = onto

    class Max(DataProperty, FunctionalProperty):
        namespace = onto

    class AVG(DataProperty, FunctionalProperty):
        namespace = onto

    class Tot_Size(DataProperty, FunctionalProperty):
        namespace = onto

    class IAT(DataProperty, FunctionalProperty):
        namespace = onto

    class Magnitue(DataProperty, FunctionalProperty):
        namespace = onto

    class Probabilidad(DataProperty, FunctionalProperty):
        namespace = onto

    class Impacto(DataProperty, FunctionalProperty):
        namespace = onto

    class Riesgo(DataProperty, FunctionalProperty):
        namespace = onto

    class Riesgo_Residual(DataProperty, FunctionalProperty):
        namespace = onto

    class Integridad(DataProperty, FunctionalProperty):
        namespace = onto

    class Confidencialidad(DataProperty, FunctionalProperty):
        namespace = onto

    class Disponibilidad(DataProperty, FunctionalProperty):
        namespace = onto

    class Factor_Mitigacion(DataProperty, FunctionalProperty):
        namespace = onto

#Creamos las instancias que se corresponden con los activos 
Amazon_Echo_Show = Asistentes_Virtuales("Amazon_Echo_Show")
AMCREST_WiFi_Camera = Camaras("AMCREST_WiFi_Camera")
DCS8000LHA1_D_Link_Mini_Camera = Camaras("DCS8000LHA1_D-Link_Mini_Camera")
Netatmo_Camera = Camaras("Netatmo_Camera")
Netatmo_Weather_Station = Sensores("Netatmo_Weather_Station")
Harman_Kardon = Altavoces("Harman_Kardon")
Philips_Hue_Bridge = Centro_Control("Philips_Hue_Bridge")
Raspberry1 = Raspberry("DC:A6:32:C9:E6:F4")
Raspberry2 = Raspberry("DC:A6:32:C9:E4:C6")
Raspberry3 = Raspberry("DC:A6:32:C9:E5:02")
TP_Link_Tapo_Camera = Camaras("TP-Link_Tapo_Camera")
AeoTec_Smart_Home_Hub = Centro_Control("AeoTec_Smart_Home_Hub")
Amazon_Alexa_Echo_Dot_1 = Asistentes_Virtuales("Amazon_Alexa_Echo_Dot_1")
Amazon_Alexa_Echo_Dot_2 = Asistentes_Virtuales("Amazon_Alexa_Echo_Dot_2")
Amazon_Alexa_Echo_Spot = Asistentes_Virtuales("Amazon_Alexa_Echo_Spot")
Borun_Sichuan_AI_Camera = Camaras("Borun/Sichuan-AI_Camera")
Google_Nest_Mini_Speaker = Asistentes_Virtuales("Google_Nest_Mini_Speaker")
Gosund_Power_Strip_1 = Enchufes("Gosund_Power_Strip_1")
Gosund_Power_Strip_2 = Enchufes("Gosund_Power_Strip_2")
Gosund_Bulb = Bombillas("Gosund_Bulb")
Gosund_Smart_Plug_WP2 = Enchufes("Gosund_Smart_Plug_WP2")
Gosund_Smart_Plug_WP3 = Enchufes("Gosund_Smart_Plug_WP3")
HeimVision_SmartLife_RadioLamp = Bombillas("HeimVision_SmartLife_RadioLamp")
HeimVision_Smart_WiFi_Camera = Camaras("HeimVision_Smart_WiFi_Camera")
Home_Eye_Camera = Camaras("Home_Eye_Camera")
LampUX_RGB = Bombillas("LampUX_RGB")
LIFX_Lightbulb = Bombillas("LIFX_Lightbulb")
Lumiman_bulb = Bombillas("Lumiman_bulb")
Luohe_Cam_Dog = Camaras("Luohe_Cam_Dog")
Rbcior_Camera = Camaras("Rbcior_Camera")
SmartThings_Hub = Centro_Control("SmartThings_Hub")
Teckin_Light_Strip = Bombillas("Teckin_Light_Strip")
Teckin_Plug_1 = Enchufes("Teckin_Plug_1")
Teckin_Plug_2 = Enchufes("Teckin_Plug_2")
Wemo_smart_plug_1 = Enchufes("Wemo_smart_plug_1")
Wemo_smart_plug_2 = Enchufes("Wemo_smart_plug_2")
Yutron_Plug_1 = Enchufes("Yutron_Plug_1")
Yutron_Plug_2 = Enchufes("Yutron_Plug_2")
Globe_Lamp_ESP_B1680C = Bombillas("Globe_Lamp_ESP_B1680C")
SIMCAM_1S  = Camaras("SIMCAM_1S")
Sonos_One_Speaker = Altavoces("Sonos_One_Speaker")
Amazon_Plug = Enchufes("Amazon_Plug")
Arlo_Q_Indoor_Camera = Camaras("Arlo_Q_Indoor_Camera")
Arlo_Base_Station = Centro_Control("Arlo_Base_Station")
Cocoon_Smart_HVAC_Fan = Ventilador("Cocoon_Smart_HVAC_Fan")
Govee_Smart_Humidifier = Ventilador("Govee_Smart_Humidifier")
Levoit_Air_Purifier = Ventilador("Levoit_Air_Purifier")
Wyze_Camera = Camaras("Wyze_Camera")
Yi_Indoor_Camera = Camaras("Yi_Indoor_Camera")
Yi_Indoor_2_Camera = Camaras("Yi_Indoor_2_Camera")
Yi_Outdoor_Camera = Camaras("Yi_Outdoor_Camera")
Amazon_Alexa_Echo_Studio = Asistentes_Virtuales("Amazon_Alexa_Echo_Studio")
Atomi_Coffee_Maker = Robots("Atomi_Coffee_Maker")
Eufy_HomeBase2 = Centro_Control("Eufy_HomeBase2")
Nest_Indoor_Camera = Camaras("Nest_Indoor_Camera")
Ring_Base_Station = Timbres("Ring_Base_Station")
Smart_Board = TVs("Smart_Board")
Fibaro_Home_Center_Lite = Centro_Control("Fibaro_Home_Center_Lite")
iRobot_Roomba = Robots("iRobot_Roomba")
LG_Smart_TV = TVs("LG_Smart_TV")
Whole_Network = HW("Whole_Network") 

dispositivos = [Amazon_Echo_Show, AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera, Netatmo_Camera, Netatmo_Weather_Station, Harman_Kardon, Philips_Hue_Bridge, Raspberry1, Raspberry2, Raspberry3, TP_Link_Tapo_Camera, AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Alexa_Echo_Dot_2, Amazon_Alexa_Echo_Spot, Borun_Sichuan_AI_Camera, Google_Nest_Mini_Speaker, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Bulb, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, HeimVision_SmartLife_RadioLamp, HeimVision_Smart_WiFi_Camera, Home_Eye_Camera, LampUX_RGB, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Rbcior_Camera, SmartThings_Hub, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wemo_smart_plug_2, Yutron_Plug_1, Yutron_Plug_2, Globe_Lamp_ESP_B1680C, SIMCAM_1S, Sonos_One_Speaker, Amazon_Plug, Arlo_Q_Indoor_Camera, Arlo_Base_Station, Cocoon_Smart_HVAC_Fan, Govee_Smart_Humidifier, Levoit_Air_Purifier, Wyze_Camera, Yi_Indoor_Camera, Yi_Indoor_2_Camera, Yi_Outdoor_Camera, Amazon_Alexa_Echo_Studio, Atomi_Coffee_Maker, Eufy_HomeBase2, Nest_Indoor_Camera, Ring_Base_Station, Smart_Board, Fibaro_Home_Center_Lite, iRobot_Roomba, LG_Smart_TV, Whole_Network]
# Asignamos valores aleatorios a las propiedades de confidencialidad, integridad y disponibilidad
for dispositivo in dispositivos:
    setattr(dispositivo, "Confidencialidad", random.randint(1, 10))
    setattr(dispositivo, "Integridad",random.randint(1, 10))
    setattr(dispositivo, "Disponibilidad", random.randint(1, 10))

#Creamos instancias de contramedidas
Copias_de_seguridad = Contramedidas("Copias_de_seguridad")
Identificacion_y_autenticacion = Contramedidas("Identificación_y_autenticación")
Cifrado_de_la_informacion = Contramedidas("Cifrado_de_la_información")
Perfiles_de_seguridad = Contramedidas("Perfiles_de_seguridad")
Aseguramiento_de_la_disponibilidad = Contramedidas("Aseguramiento_de_la_disponibilidad")
Actualizacion_y_mantenimiento = Contramedidas("Actualizacion_y_mantenimiento")
Herramienta_de_monitorizacion = Contramedidas("Herramienta_de_monitorización")
Proteccion_de_comunicaciones = Contramedidas("Proteccion_de_comunicaciones")
Herramienta_de_deteccion_de_intrusiones = Contramedidas("Herramienta_de_detección_de_intrusiones")

contramedidas = [Copias_de_seguridad, Identificacion_y_autenticacion, Cifrado_de_la_informacion, Perfiles_de_seguridad, Aseguramiento_de_la_disponibilidad, Actualizacion_y_mantenimiento, Herramienta_de_monitorizacion, Proteccion_de_comunicaciones, Herramienta_de_deteccion_de_intrusiones]
for contramedida in contramedidas:
    setattr(contramedida, "Factor_Mitigacion", random.choice(factores_mitigacion))

# Mapeo de los nombres de las propiedades a las posiciones de las columnas en el archivo CSV
propiedades = ["Header_Length", "Protocol_Type", "Srate", "Tot_Sum", "Min", "Max", "AVG", "Tot_Size", "IAT", "Magnitude"]

# Diccionario para contar cuántas veces aparece cada nombre de ataque
contador_ataques = {}

# Leemos el archivo CSV y creamos instancias de ataques
with open("resultado_porcentaje.csv", "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    next(reader, None)  # Saltar la primera fila (titulos)
    for row in reader:
        # Extraemos el nombre del ataque
        nombre_ataque = row[-1]
        
        # Verificamos si el nombre del ataque ya está en el contador de ataques
        if nombre_ataque not in contador_ataques:
            contador_ataques[nombre_ataque] = 1
        else:
            # Incrementamos el contador del ataque
            contador_ataques[nombre_ataque] += 1
        
        # Creamos una instancia de Ataque para cada fila del CSV
        ataque = Incidentes(f"{nombre_ataque}_{contador_ataques[nombre_ataque]:04d}")
        
        # Asignamos los valores de los parámetros a las propiedades correspondientes
        for propiedad, valor in zip(propiedades, row[:-1]):  # Ignoramos el último valor que es el nombre del ataque
            setattr(ataque, propiedad, float(valor))
        
    # Array de activos afectados por DoS
    activos_afectados_dos_http_flood = [Amazon_Echo_Show, AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera, Harman_Kardon, Netatmo_Camera, Philips_Hue_Bridge, Raspberry1, Raspberry2]
    activos_afectados_dos_syn_flood = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Alexa_Echo_Dot_2, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, AMCREST_WiFi_Camera, Borun_Sichuan_AI_Camera, DCS8000LHA1_D_Link_Mini_Camera, Google_Nest_Mini_Speaker, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Bulb, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, LampUX_RGB, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Rbcior_Camera, SmartThings_Hub, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_dos_tcp_flood = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Alexa_Echo_Spot, AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, iRobot_Roomba, LampUX_RGB, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, SIMCAM_1S, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Plug_1, Teckin_Light_Strip, Teckin_Plug_2, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_dos_udp_flood = [Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Q_Indoor_Camera, Borun_Sichuan_AI_Camera, Cocoon_Smart_HVAC_Fan, DCS8000LHA1_D_Link_Mini_Camera, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_2, Gosund_Power_Strip_1, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, HeimVision_Smart_WiFi_Camera, HeimVision_SmartLife_RadioLamp, Harman_Kardon, Home_Eye_Camera, LampUX_RGB, Levoit_Air_Purifier, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Rbcior_Camera, SIMCAM_1S, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wemo_smart_plug_2, Wyze_Camera, Yi_Indoor_Camera, Yi_Indoor_2_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]
   
    # Array de activos afectados por Web-Based
    activos_afectados_Backdoor_Malware = [Raspberry1, Raspberry2, Raspberry3]
    activos_afectados_Command_Injection = [Raspberry1, Raspberry2, Raspberry3]
    activos_afectados_SQL_Injection = [Raspberry1, Raspberry2, Raspberry3]
    activos_afectados_Uploading_Attack = [Raspberry1, Raspberry2, Raspberry3]
    activos_afectados_XSS = [Raspberry1, Raspberry2, Raspberry3]

    # Array de activos afectados por Recon
    activos_afectados_Host_Discoery = [Whole_Network]
    activos_afectados_Ping_Sweep = [Whole_Network]
    activos_afectados_Vulnerability_Scan = [Whole_Network]
    activos_afectados_OS_Scan = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, Amazon_Alexa_Echo_Studio, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Base_Station, Arlo_Q_Indoor_Camera, Atomi_Coffee_Maker, Borun_Sichuan_AI_Camera, Cocoon_Smart_HVAC_Fan, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Fibaro_Home_Center_Lite, Globe_Lamp_ESP_B1680C, Nest_Indoor_Camera, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, HeimVision_Smart_WiFi_Camera, Harman_Kardon, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, iRobot_Roomba, LampUX_RGB, Levoit_Air_Purifier, LG_Smart_TV, LIFX_Lightbulb, Lumiman_bulb, Netatmo_Camera, Netatmo_Weather_Station, Philips_Hue_Bridge, Raspberry1, Raspberry2, Raspberry3, Rbcior_Camera, Ring_Base_Station, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wemo_smart_plug_2, Wyze_Camera, Yi_Indoor_2_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_Port_Scan = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Alexa_Echo_Dot_2, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, Amazon_Alexa_Echo_Studio, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Base_Station, Arlo_Q_Indoor_Camera, Atomi_Coffee_Maker, Borun_Sichuan_AI_Camera, Cocoon_Smart_HVAC_Fan, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Fibaro_Home_Center_Lite, Globe_Lamp_ESP_B1680C, Nest_Indoor_Camera, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, Harman_Kardon, HeimVision_Smart_WiFi_Camera, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, iRobot_Roomba, LampUX_RGB, Levoit_Air_Purifier, LG_Smart_TV, LIFX_Lightbulb, Lumiman_bulb, Netatmo_Camera, Netatmo_Weather_Station, Philips_Hue_Bridge, Rbcior_Camera, Ring_Base_Station, Smart_Board, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wemo_smart_plug_2, Wyze_Camera, Yi_Indoor_2_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]

    # Array de activos afectados por Brute Force
    activos_afectados_Dictionary_Brute_Force = [HeimVision_Smart_WiFi_Camera, Luohe_Cam_Dog, Raspberry1, Raspberry2, Raspberry3]

    # Array de activos afectados por Spoofing
    activos_afectados_DNS_Spoofing = [Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, Amazon_Alexa_Echo_Studio, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Base_Station, Arlo_Q_Indoor_Camera, Atomi_Coffee_Maker, Cocoon_Smart_HVAC_Fan, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Nest_Indoor_Camera, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, HeimVision_Smart_WiFi_Camera, Harman_Kardon, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, iRobot_Roomba, LampUX_RGB, Levoit_Air_Purifier, LG_Smart_TV, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Netatmo_Weather_Station, Philips_Hue_Bridge, Raspberry1, Raspberry2, Raspberry3, Rbcior_Camera, Ring_Base_Station, SIMCAM_1S, Smart_Board, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wyze_Camera, Yi_Indoor_2_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ARP_Spoofing = [Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, Amazon_Alexa_Echo_Studio, Amazon_Plug, Arlo_Base_Station, Arlo_Q_Indoor_Camera, Atomi_Coffee_Maker, Borun_Sichuan_AI_Camera, Cocoon_Smart_HVAC_Fan, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Nest_Indoor_Camera, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, Harman_Kardon, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, iRobot_Roomba, LampUX_RGB, Levoit_Air_Purifier, LG_Smart_TV, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Weather_Station, Philips_Hue_Bridge, Rbcior_Camera, Ring_Base_Station, SIMCAM_1S, Smart_Board, SmartThings_Hub, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wyze_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]

    # Array de activos afectados por Mirai
    activos_afectados_GREETH = [Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Studio, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Base_Station, Arlo_Q_Indoor_Camera, Atomi_Coffee_Maker, Borun_Sichuan_AI_Camera, Cocoon_Smart_HVAC_Fan, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, HeimVision_Smart_WiFi_Camera, Harman_Kardon, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, iRobot_Roomba, LampUX_RGB, Levoit_Air_Purifier, LIFX_Lightbulb, Lumiman_bulb, Nest_Indoor_Camera, Netatmo_Camera, Philips_Hue_Bridge, Raspberry1, Raspberry2, Raspberry3, Rbcior_Camera, Ring_Base_Station, SIMCAM_1S, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wyze_Camera, Yi_Indoor_2_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_GREIP = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, Amazon_Alexa_Echo_Studio, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Base_Station, Arlo_Q_Indoor_Camera, Atomi_Coffee_Maker, Borun_Sichuan_AI_Camera, Cocoon_Smart_HVAC_Fan, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, HeimVision_Smart_WiFi_Camera, HeimVision_SmartLife_RadioLamp, Harman_Kardon, Home_Eye_Camera, iRobot_Roomba, LampUX_RGB, Levoit_Air_Purifier, LG_Smart_TV, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Nest_Indoor_Camera, Netatmo_Camera, Netatmo_Weather_Station, Philips_Hue_Bridge, Raspberry1, Raspberry2, Raspberry3, Rbcior_Camera, Ring_Base_Station, SIMCAM_1S, Smart_Board, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wyze_Camera, Yi_Indoor_2_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_UDPPLAIN = [Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Studio, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Base_Station, Arlo_Q_Indoor_Camera, Atomi_Coffee_Maker, Borun_Sichuan_AI_Camera, Cocoon_Smart_HVAC_Fan, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, HeimVision_Smart_WiFi_Camera, Harman_Kardon, Home_Eye_Camera, iRobot_Roomba, LampUX_RGB, Levoit_Air_Purifier, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Nest_Indoor_Camera, Netatmo_Camera, Philips_Hue_Bridge, Raspberry1, Raspberry2, Raspberry3, Rbcior_Camera, Ring_Base_Station, SIMCAM_1S, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wyze_Camera, Yi_Indoor_2_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]
    
    # Array de activos afectados por el ataque DDoS
    activos_afectados_ddos_ACK_Fragmentation = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, HeimVision_Smart_WiFi_Camera, Home_Eye_Camera, LampUX_RGB, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Philips_Hue_Bridge, Rbcior_Camera, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ddos_ICMP_Fragmentation = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, Amazon_Alexa_Echo_Studio, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Base_Station, Arlo_Q_Indoor_Camera, Atomi_Coffee_Maker, Borun_Sichuan_AI_Camera, Cocoon_Smart_HVAC_Fan, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Fibaro_Home_Center_Lite, Globe_Lamp_ESP_B1680C, Nest_Indoor_Camera, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, HeimVision_Smart_WiFi_Camera, Harman_Kardon, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, iRobot_Roomba, LampUX_RGB, Levoit_Air_Purifier, LG_Smart_TV, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Netatmo_Weather_Station, Philips_Hue_Bridge, Raspberry1, Raspberry2, Raspberry3, Rbcior_Camera, Ring_Base_Station, SIMCAM_1S, Smart_Board, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_2, Wyze_Camera, Yi_Indoor_2_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ddos_UDP_Fragmentation = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, Amazon_Alexa_Echo_Studio, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Q_Indoor_Camera, DCS8000LHA1_D_Link_Mini_Camera, Globe_Lamp_ESP_B1680C, Nest_Indoor_Camera, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, HeimVision_Smart_WiFi_Camera, Home_Eye_Camera, LampUX_RGB, Levoit_Air_Purifier, LG_Smart_TV, LIFX_Lightbulb, Luohe_Cam_Dog, Netatmo_Camera, Philips_Hue_Bridge, Rbcior_Camera, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wyze_Camera, Yi_Indoor_2_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ddos_HTTP_Flood = [AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera]
    activos_afectados_ddos_ICMP_Flood = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Alexa_Echo_Dot_2, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, Amazon_Alexa_Echo_Studio, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Base_Station, Arlo_Q_Indoor_Camera, Borun_Sichuan_AI_Camera, Cocoon_Smart_HVAC_Fan, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Fibaro_Home_Center_Lite, Globe_Lamp_ESP_B1680C, Nest_Indoor_Camera, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Harman_Kardon, HeimVision_Smart_WiFi_Camera, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, LampUX_RGB, Levoit_Air_Purifier, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Philips_Hue_Bridge, Rbcior_Camera, Ring_Base_Station, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wemo_smart_plug_2, Wyze_Camera, Yi_Indoor_2_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ddos_PSHACK_Flood = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, HeimVision_Smart_WiFi_Camera, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, LampUX_RGB, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Philips_Hue_Bridge, Rbcior_Camera, SIMCAM_1S, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ddos_RSTFIN_Flood = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, HeimVision_Smart_WiFi_Camera, Home_Eye_Camera, LampUX_RGB, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Philips_Hue_Bridge, Rbcior_Camera, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ddos_SynonymouosIP_Flood = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP3, HeimVision_Smart_WiFi_Camera, Home_Eye_Camera, LampUX_RGB, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Philips_Hue_Bridge, Rbcior_Camera, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ddos_TCP_Flood = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Alexa_Echo_Dot_2, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP3, Gosund_Smart_Plug_WP2, Harman_Kardon, HeimVision_SmartLife_RadioLamp, LampUX_RGB, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Philips_Hue_Bridge, Rbcior_Camera, SIMCAM_1S, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wemo_smart_plug_2, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ddos_SYN_Flood = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Alexa_Echo_Dot_2, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, HeimVision_Smart_WiFi_Camera, Harman_Kardon, HeimVision_SmartLife_RadioLamp, Home_Eye_Camera, LampUX_RGB, LIFX_Lightbulb, Lumiman_bulb, Luohe_Cam_Dog, Netatmo_Camera, Philips_Hue_Bridge, Rbcior_Camera, SIMCAM_1S, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wemo_smart_plug_2, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ddos_UDP_Flood = [AeoTec_Smart_Home_Hub, Amazon_Alexa_Echo_Dot_1, Amazon_Alexa_Echo_Dot_2, Amazon_Echo_Show, Amazon_Alexa_Echo_Spot, Amazon_Alexa_Echo_Studio, Amazon_Plug, AMCREST_WiFi_Camera, Arlo_Q_Indoor_Camera, DCS8000LHA1_D_Link_Mini_Camera, Globe_Lamp_ESP_B1680C, Google_Nest_Mini_Speaker, Gosund_Bulb, Gosund_Power_Strip_1, Gosund_Power_Strip_2, Gosund_Smart_Plug_WP2, Gosund_Smart_Plug_WP3, Govee_Smart_Humidifier, HeimVision_Smart_WiFi_Camera, Harman_Kardon, Home_Eye_Camera, LampUX_RGB, Levoit_Air_Purifier, LIFX_Lightbulb, Luohe_Cam_Dog, Nest_Indoor_Camera, Netatmo_Camera, Philips_Hue_Bridge, Rbcior_Camera, SIMCAM_1S, SmartThings_Hub, Sonos_One_Speaker, TP_Link_Tapo_Camera, Teckin_Light_Strip, Teckin_Plug_1, Teckin_Plug_2, Wemo_smart_plug_1, Wyze_Camera, Yi_Indoor_2_Camera, Yi_Indoor_Camera, Yi_Outdoor_Camera, Yutron_Plug_1, Yutron_Plug_2]
    activos_afectados_ddos_SlowLoris = [AMCREST_WiFi_Camera, DCS8000LHA1_D_Link_Mini_Camera, Eufy_HomeBase2, Google_Nest_Mini_Speaker, HeimVision_Smart_WiFi_Camera, Harman_Kardon, LIFX_Lightbulb, Netatmo_Camera, Philips_Hue_Bridge, Raspberry1, Raspberry2, Raspberry3, TP_Link_Tapo_Camera]

    # Iterar sobre todas las instancias de ataque y relacionarlas con activos según criterio proporcionado por el dataset
    for ataque_instancia in onto.Incidentes.instances():
        if "Backdoor_Malware" in ataque_instancia.name:
            for activo in activos_afectados_Backdoor_Malware:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "CommandInjection" in ataque_instancia.name:
            for activo in activos_afectados_Command_Injection:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "SqlInjection" in ataque_instancia.name:
            for activo in activos_afectados_SQL_Injection:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "Uploading_Attack" in ataque_instancia.name:
            for activo in activos_afectados_Uploading_Attack:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "XSS" in ataque_instancia.name:
            for activo in activos_afectados_XSS:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
                
        elif "Recon-HostDiscovery" in ataque_instancia.name:
            for activo in activos_afectados_Host_Discoery:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "Recon-PingSweep" in ataque_instancia.name:
            for activo in activos_afectados_Ping_Sweep:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "VulnerabilityScan" in ataque_instancia.name:
            for activo in activos_afectados_Vulnerability_Scan:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "Recon-OSScan" in ataque_instancia.name:
            for activo in activos_afectados_OS_Scan:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "Recon-PortScan" in ataque_instancia.name:
            for activo in activos_afectados_Port_Scan:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
                
        elif "DictionaryBruteForce" in ataque_instancia.name:
            for activo in activos_afectados_Dictionary_Brute_Force:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
                
        elif "DNS_Spoofing" in ataque_instancia.name:
            for activo in activos_afectados_DNS_Spoofing:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "MITM-ArpSpoofing" in ataque_instancia.name:
            for activo in activos_afectados_ARP_Spoofing:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
                
        elif "Mirai-greeth_flood" in ataque_instancia.name:
            for activo in activos_afectados_GREETH:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "Mirai-greip_flood" in ataque_instancia.name:
            for activo in activos_afectados_GREIP:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
        elif "Mirai-udpplain" in ataque_instancia.name:
            for activo in activos_afectados_UDPPLAIN:
                ataque_instancia.afectan.append(activo)
                activo.sonAfectadosPor.append(ataque_instancia)
            
    for ataque_instancia_denegacion in onto.Incidentes.instances():
        if ataque_instancia_denegacion.name.startswith("DoS"):
            if "DoS-HTTP_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_dos_http_flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)                 
            elif "DoS-SYN_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_dos_syn_flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DoS-TCP_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_dos_tcp_flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DoS-UDP_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_dos_udp_flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)

        elif ataque_instancia_denegacion.name.startswith("DDoS"):
            if "DDoS-ACK_Fragmentation" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_ACK_Fragmentation:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-HTTP_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_HTTP_Flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-ICMP_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_ICMP_Flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-ICMP_Fragmentation" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_ICMP_Fragmentation:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-PSHACK_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_PSHACK_Flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-RSTFINFlood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_RSTFIN_Flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-SYN_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_SYN_Flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-SynonymousIP_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_SynonymouosIP_Flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-TCP_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_TCP_Flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-UDP_Flood" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_UDP_Flood:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-UDP_Fragmentation" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_UDP_Fragmentation:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)
            elif "DDoS-SlowLoris" in ataque_instancia_denegacion.name:
                for activo in activos_afectados_ddos_SlowLoris:
                    ataque_instancia_denegacion.afectan.append(activo)
                    activo.sonAfectadosPor.append(ataque_instancia_denegacion)

# Definimos los contadores para cada tipo de amenaza
contador_amenazas_dos = 0
contador_amenazas_mirai = 0
contador_amenazas_bruteforce = 0
contador_amenazas_spoofing = 0
contador_amenazas_recon = 0
contador_amenazas_web = 0

for ataque_instancia in onto.Incidentes.instances():

    if "DoS" in ataque_instancia.name or "DDoS" in ataque_instancia.name:
        contador_amenazas_dos += 1
        numero_formateado = f"{contador_amenazas_dos:04d}" 
        # Crear el nombre de la instancia de amenaza con el número formateado
        nombre_amenaza = f"Denegacion_de_servicio-{numero_formateado}"
        # Crear una nueva instancia de la entidad correspondiente a Amenaza con el nombre especificado y relacionada al ataque
        nueva_amenaza = Amenazas(name=nombre_amenaza, ataque_relacionado=ataque_instancia)
        nueva_amenaza.sonGenerados.append(ataque_instancia)
        ataque_instancia.generan.append(nueva_amenaza)
        #Asignar las relaciones entre las instancias de Amenazas y los incidentes
        if contador_amenazas_dos > 0:
            # Asignar los riesgos potenciales y residuales a la amenaza
            Denegacion_de_servicio_Riesgo_Potencial = Riesgos_Potencial("Denegacion_de_servicio_Riesgo_Potencial")
            Denegacion_de_servicio_Riesgo_Residual = Riesgos_Residual("Denegacion_de_servicio_Riesgo_Residual")
            nueva_amenaza.provocan.append(Denegacion_de_servicio_Riesgo_Potencial)
            nueva_amenaza.provocan.append(Denegacion_de_servicio_Riesgo_Residual)
            Denegacion_de_servicio_Riesgo_Potencial.sonProvocadosPor.append(nueva_amenaza)
            Denegacion_de_servicio_Riesgo_Residual.sonProvocadosPor.append(nueva_amenaza)
            setattr(nueva_amenaza, "Probabilidad", "MA")  # Asignar probabilidad según corresponda
            setattr(nueva_amenaza, "Impacto", random.choice(posibles_impactos))  # Asignar impacto según corresponda
            setattr(nueva_amenaza, "Riesgo", calcular_riesgo_potencial(nueva_amenaza.Probabilidad, nueva_amenaza.Impacto))  # Calcular el riesgo

    elif "Mirai" in ataque_instancia.name:
        contador_amenazas_mirai += 1
        numero_formateado = f"{contador_amenazas_mirai:04d}"  
        nombre_amenaza = f"Difusion_SW_Dañino-{numero_formateado}"
        nueva_amenaza = Amenazas(name=nombre_amenaza, ataque_relacionado=ataque_instancia)
        nueva_amenaza.sonGenerados.append(ataque_instancia)
        ataque_instancia.generan.append(nueva_amenaza)
        if contador_amenazas_mirai > 0:
            Difusion_SW_Dañino_Riesgo_Residual = Riesgos_Residual("Difusion_SW_Dañino_Riesgo_Residual")
            Difusion_SW_Dañino_Riesgo_Potencial = Riesgos_Potencial("Difusion_SW_Dañino_Riesgo_Potencial")
            nueva_amenaza.provocan.append(Difusion_SW_Dañino_Riesgo_Potencial)
            nueva_amenaza.provocan.append(Difusion_SW_Dañino_Riesgo_Residual)
            Difusion_SW_Dañino_Riesgo_Potencial.sonProvocadosPor.append(nueva_amenaza)
            Difusion_SW_Dañino_Riesgo_Residual.sonProvocadosPor.append(nueva_amenaza)
            setattr(nueva_amenaza, "Probabilidad", "A")
            setattr(nueva_amenaza, "Impacto", random.choice(posibles_impactos))
            setattr(nueva_amenaza, "Riesgo",calcular_riesgo_potencial(nueva_amenaza.Probabilidad, nueva_amenaza.Impacto))
            
    elif "DictionaryBruteForce" in ataque_instancia.name:
        contador_amenazas_bruteforce += 1
        numero_formateado = f"{contador_amenazas_bruteforce:04d}"  
        nombre_amenaza = f"Modificacion_deliberada_de_informacion-{numero_formateado}"
        nueva_amenaza = Amenazas(name=nombre_amenaza, ataque_relacionado=ataque_instancia)
        nueva_amenaza.sonGenerados.append(ataque_instancia)
        ataque_instancia.generan.append(nueva_amenaza)
        if contador_amenazas_bruteforce > 0:
            Modificacion_deliberada_de_informacion_Riesgo_Residual = Riesgos_Residual("Modificacion_deliberada_de_informacion_Riesgo_Residual")
            Modificacion_deliberada_de_informacion_Riesgo_Potencial = Riesgos_Potencial("Modificacion_deliberada_de_informacion_Riesgo_Potencial")
            nueva_amenaza.provocan.append(Modificacion_deliberada_de_informacion_Riesgo_Potencial)
            nueva_amenaza.provocan.append(Modificacion_deliberada_de_informacion_Riesgo_Residual)
            Modificacion_deliberada_de_informacion_Riesgo_Potencial.sonProvocadosPor.append(nueva_amenaza)
            Modificacion_deliberada_de_informacion_Riesgo_Residual.sonProvocadosPor.append(nueva_amenaza)
            setattr(nueva_amenaza, "Probabilidad", "MB")
            setattr(nueva_amenaza, "Impacto", random.choice(posibles_impactos))
            setattr(nueva_amenaza, "Riesgo",calcular_riesgo_potencial(nueva_amenaza.Probabilidad, nueva_amenaza.Impacto))

    elif "Spoofing" in ataque_instancia.name:
        contador_amenazas_spoofing += 1
        numero_formateado = f"{contador_amenazas_spoofing:04d}" 
        nombre_amenaza = f"Suplantacion_de_identidad-{numero_formateado}"
        nueva_amenaza = Amenazas(name=nombre_amenaza, ataque_relacionado=ataque_instancia)
        nueva_amenaza.sonGenerados.append(ataque_instancia)
        ataque_instancia.generan.append(nueva_amenaza)
        if contador_amenazas_spoofing > 0:
            Suplantacion_de_identidad_Riesgo_Potencial = Riesgos_Potencial("Suplantacion_de_identidad_Riesgo_Potencial")
            Suplantacion_de_identidad_Riesgo_Residual = Riesgos_Residual("Suplantacion_de_identidad_Riesgo_Residual")
            nueva_amenaza.provocan.append(Suplantacion_de_identidad_Riesgo_Potencial)
            nueva_amenaza.provocan.append(Suplantacion_de_identidad_Riesgo_Residual)
            Suplantacion_de_identidad_Riesgo_Potencial.sonProvocadosPor.append(nueva_amenaza)
            Suplantacion_de_identidad_Riesgo_Residual.sonProvocadosPor.append(nueva_amenaza)
            setattr(nueva_amenaza, "Probabilidad", "B")
            setattr(nueva_amenaza, "Impacto", random.choice(posibles_impactos))
            setattr(nueva_amenaza, "Riesgo",calcular_riesgo_potencial(nueva_amenaza.Probabilidad, nueva_amenaza.Impacto))
            
    elif "Recon" in ataque_instancia.name or "Vulnerability" in ataque_instancia.name:
        contador_amenazas_recon += 1
        numero_formateado = f"{contador_amenazas_recon:04d}" 
        nombre_amenaza = f"Acceso_no_autorizado-{numero_formateado}"
        nueva_amenaza = Amenazas(name=nombre_amenaza, ataque_relacionado=ataque_instancia)
        nueva_amenaza.sonGenerados.append(ataque_instancia)
        ataque_instancia.generan.append(nueva_amenaza)
        if contador_amenazas_recon > 0:
            Acceso_no_autorizado_Riesgo_Potencial = Riesgos_Potencial("Acceso_no_autorizado_Riesgo_Potencial")
            Acceso_no_autorizado_Riesgo_Residual = Riesgos_Residual("Acceso_no_autorizado_Riesgo_Residual")
            nueva_amenaza.provocan.append(Acceso_no_autorizado_Riesgo_Potencial)
            nueva_amenaza.provocan.append(Acceso_no_autorizado_Riesgo_Residual)
            Acceso_no_autorizado_Riesgo_Potencial.sonProvocadosPor.append(nueva_amenaza)
            Acceso_no_autorizado_Riesgo_Residual.sonProvocadosPor.append(nueva_amenaza)
            setattr(nueva_amenaza, "Probabilidad", "MB")
            setattr(nueva_amenaza, "Impacto", random.choice(posibles_impactos))
            setattr(nueva_amenaza, "Riesgo",calcular_riesgo_potencial(nueva_amenaza.Probabilidad, nueva_amenaza.Impacto))

    elif "Injection" in ataque_instancia.name or "Backdoor" in ataque_instancia.name or "Uploading" in ataque_instancia.name or "XSS" in ataque_instancia.name or "Hijacking" in ataque_instancia.name:
        contador_amenazas_web += 1
        numero_formateado = f"{contador_amenazas_web:04d}"  
        nombre_amenaza = f"Manipulacion_de_programas-{numero_formateado}"
        nueva_amenaza = Amenazas(name=nombre_amenaza, ataque_relacionado=ataque_instancia)
        nueva_amenaza.sonGenerados.append(ataque_instancia)
        ataque_instancia.generan.append(nueva_amenaza)
        if contador_amenazas_web > 0:
            Manipulacion_de_programas_Riesgo_Potencial = Riesgos_Potencial("Web-Manipulacion_de_programas_Riesgo_Potencial")
            Manipulacion_de_programas_Riesgo_Residual = Riesgos_Residual("Manipulacion_de_programas_Riesgo_Residual")
            nueva_amenaza.provocan.append(Manipulacion_de_programas_Riesgo_Potencial)
            nueva_amenaza.provocan.append(Manipulacion_de_programas_Riesgo_Residual)
            Manipulacion_de_programas_Riesgo_Potencial.sonProvocadosPor.append(nueva_amenaza)
            Manipulacion_de_programas_Riesgo_Residual.sonProvocadosPor.append(nueva_amenaza)
            setattr(nueva_amenaza, "Probabilidad", "MB")
            setattr(nueva_amenaza, "Impacto", random.choice(posibles_impactos))
            setattr(nueva_amenaza, "Riesgo",calcular_riesgo_potencial(nueva_amenaza.Probabilidad, nueva_amenaza.Impacto))

    # Iterar sobre las instancias de Riesgos
    for riesgo_instancia in onto.Riesgos_Potencial.instances():
        # Inicializar la suma total del riesgo para esta instancia de riesgo
        suma_riesgo_amenazas = 0
        # Contador para el número de amenazas asociadas a este riesgo
        contador_amenazas = 0
        
        # Iterar sobre las amenazas asociadas a este riesgo
        for amenaza_relacionada in riesgo_instancia.sonProvocadosPor:
            # Convertir la letra de riesgo a número y sumar
            suma_riesgo_amenazas += letra_a_numero(amenaza_relacionada.Riesgo)
            contador_amenazas += 1
        
        # Calcular el riesgo promedio generado por las amenazas asociadas a este riesgo
        if contador_amenazas != 0:
            riesgo_promedio_amenazas = suma_riesgo_amenazas / contador_amenazas
        else:
            riesgo_promedio_amenazas = 0
        
        # Convertir el número de riesgo promedio de nuevo a letra
        riesgo_instancia.Riesgo = numero_a_letra(math.ceil(riesgo_promedio_amenazas))

    # Iterar sobre las instancias de Riesgos
    for riesgo_instancia in onto.Riesgos_Residual.instances():
        # Inicializar la suma total del riesgo para esta instancia de riesgo
        suma_riesgo_amenazas = 0
        # Contador para el número de amenazas asociadas a este riesgo
        contador_amenazas = 0
        
        # Iterar sobre las amenazas asociadas a este riesgo
        for amenaza_relacionada in riesgo_instancia.sonProvocadosPor:
            # Convertir la letra de riesgo a número y sumar
            suma_riesgo_amenazas += letra_a_numero(amenaza_relacionada.Riesgo)
            contador_amenazas += 1
        
        # Calcular el riesgo promedio generado por las amenazas asociadas a este riesgo
        if contador_amenazas != 0:
            riesgo_promedio_amenazas = suma_riesgo_amenazas / contador_amenazas
        else:
            riesgo_promedio_amenazas = 0
        
        # Convertir el número de riesgo promedio de nuevo a letra
        riesgo_instancia.Riesgo = numero_a_letra(math.ceil(riesgo_promedio_amenazas))
        
    # Asignar valores de probabilidad e impacto a las instancias de Riesgos
    for riesgo in onto.Riesgos_Residual.instances():
        if "Denegacion_de_servicio" in riesgo.name:
            riesgo.esContrarrestadoPor.append(Copias_de_seguridad)
            riesgo.esContrarrestadoPor.append(Aseguramiento_de_la_disponibilidad)
            Copias_de_seguridad.contrarrestan.append(riesgo)
            Aseguramiento_de_la_disponibilidad.contrarrestan.append(riesgo)
        elif "Modificacion_deliberada_de_informacion" in riesgo.name:
            riesgo.esContrarrestadoPor.append(Cifrado_de_la_informacion)
            riesgo.esContrarrestadoPor.append(Copias_de_seguridad)
            Cifrado_de_la_informacion.contrarrestan.append(riesgo)
            Copias_de_seguridad.contrarrestan.append(riesgo)
        elif "Acceso_no_autorizado" in riesgo.name:
            riesgo.esContrarrestadoPor.append(Proteccion_de_comunicaciones)
            riesgo.esContrarrestadoPor.append(Identificacion_y_autenticacion)
            Proteccion_de_comunicaciones.contrarrestan.append(riesgo)
            Identificacion_y_autenticacion.contrarrestan.append(riesgo)
        elif "Difusion_SW_Dañino" in riesgo.name:
            riesgo.esContrarrestadoPor.append(Cifrado_de_la_informacion)
            riesgo.esContrarrestadoPor.append(Herramienta_de_deteccion_de_intrusiones)
            riesgo.esContrarrestadoPor.append(Actualizacion_y_mantenimiento)
            Cifrado_de_la_informacion.contrarrestan.append(riesgo)
            Herramienta_de_deteccion_de_intrusiones.contrarrestan.append(riesgo)
            Actualizacion_y_mantenimiento.contrarrestan.append(riesgo)
        elif "Suplantacion_de_identidad" in riesgo.name:
            riesgo.esContrarrestadoPor.append(Identificacion_y_autenticacion)
            riesgo.esContrarrestadoPor.append(Perfiles_de_seguridad)
            Identificacion_y_autenticacion.contrarrestan.append(riesgo)
            Perfiles_de_seguridad.contrarrestan.append(riesgo)
        elif "Manipulacion_de_programas" in riesgo.name:
            riesgo.esContrarrestadoPor.append(Herramienta_de_monitorizacion)
            riesgo.esContrarrestadoPor.append(Actualizacion_y_mantenimiento)
            Herramienta_de_monitorizacion.contrarrestan.append(riesgo)
            Actualizacion_y_mantenimiento.contrarrestan.append(riesgo) 
            
    #Calculamos el mayor factor de mitigacion a aplicar
    for riesgo_instancia in onto.Riesgos_Residual.instances():
        # Inicializar la suma total del riesgo para esta instancia de riesgo
        suma_riesgo_amenazas = 0
        # Contador para el número de amenazas asociadas a este riesgo
        contador_amenazas = 0
        
        n = 0
        # Iterar sobre las amenazas asociadas a este riesgo
        for amenaza_relacionada in riesgo_instancia.esContrarrestadoPor:
            # Convertir la letra de riesgo a número y sumar
            if amenaza_relacionada.Factor_Mitigacion > n:
                n = amenaza_relacionada.Factor_Mitigacion
     
        # Convertir el número de riesgo promedio de nuevo a letra
        riesgo_instancia.Factor_Mitigacion = n
        setattr(riesgo_instancia, "Riesgo_Residual" ,calcular_riesgo_residual(riesgo_instancia.Factor_Mitigacion, riesgo_instancia.Riesgo))

    # Establece el atributo "Riesgo" con el valor calculado para cada activo
    establecer_riesgo_para_todos_los_activos()

#CALCULO DEL RIESGO POTENCIAL TOTAL DEL SISTEMA    
    # Inicializar la suma total de riesgos y el contador de instancias de riesgo
    suma_riesgo_total = 0
    contador_instancias_riesgo = 0

# Iterar sobre las instancias de la clase Riesgo
for riesgo_instancia in onto.Riesgos_Potencial.instances():
    # Convertir la letra de riesgo a número y sumar al total
    suma_riesgo_total += letra_a_numero(riesgo_instancia.Riesgo)
    contador_instancias_riesgo += 1

# Calcular el promedio de los riesgos
if contador_instancias_riesgo != 0:
    promedio_riesgo_total = suma_riesgo_total / contador_instancias_riesgo
    # Convertir el promedio de riesgo de número a letra
    promedio_riesgo_letra = numero_a_letra(round(promedio_riesgo_total))
else:
    promedio_riesgo_total = 0
    promedio_riesgo_letra = ""
    
print(f"El riesgo potencial total del sistema es: {promedio_riesgo_letra}")


#CALCULO DEL RIESGO RESIDUAL TOTAL DEL SISTEMA    
# Inicializar la suma total de riesgos y el contador de instancias de riesgo
suma_riesgo_total = 0
contador_instancias_riesgo = 0

# Iterar sobre las instancias de la clase Riesgo
for riesgo_instancia in onto.Riesgos_Residual.instances():
    # Convertir la letra de riesgo a número y sumar al total
    suma_riesgo_total += letra_a_numero(riesgo_instancia.Riesgo_Residual)
    contador_instancias_riesgo += 1

# Calcular el promedio de los riesgos
if contador_instancias_riesgo != 0:
    promedio_riesgo_total = suma_riesgo_total / contador_instancias_riesgo
    # Convertir el promedio de riesgo de número a letra
    promedio_riesgo_letra = numero_a_letra(round(promedio_riesgo_total))
else:
    promedio_riesgo_total = 0
    promedio_riesgo_letra = ""

print(f"El riesgo residual total del sistema es: {promedio_riesgo_letra}")

# Guardamos la ontología con las nuevas instancias de amenazas
onto.save("/Users/juliosp/Desktop/TFG/onto.rdf", format="rdfxml")