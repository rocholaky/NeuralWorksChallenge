# NeuralWorksChallenge
Este repositorio se creo para la postulación en la empresa Neural Works. 
## Contextualización del problema: 
La predicción de retrasos en aviones es de suma importancia en la industria de la aviación. Con numerosos factores que afectan los horarios de vuelo, predecir con precisión los retrasos permite a las aerolíneas gestionar proactivamente las interrupciones, optimizar los recursos y mejorar la satisfacción de los pasajeros. Al aprovechar datos históricos, información en tiempo real y modelos predictivos, las aerolíneas pueden mitigar el impacto de los retrasos, ajustar los horarios y proporcionar notificaciones oportunas a los pasajeros. Esto no solo mejora la eficiencia operativa, sino que también permite a los viajeros hacer arreglos alternativos, reduciendo las molestias. La predicción de retrasos en aviones desempeña un papel vital en la optimización de recursos, mejora de la experiencia del cliente y garantía de un viaje aéreo seguro y eficiente para todos.

## El Repositorio: 
Dentro del repositorio encontrará lo siguiente: 
### FlightPredictor: 
El packete flight predictor contiene las clases que permiten entrenar modelos de manera simple y sin mayor uso de código, este permite no solamente crear distintos modelos con una sola clase, sino que encapsula toda la lógica de splitting de datos y las transformaciones de datos que permiten que el modelo entrene. En específico, si se quiere buscar de mejor manera como utilizar dicho notebook se recomienda revisar el archivo mlapi.ipynb. 

## API: 
Dentro de esta carpeta encontrará la api que permite predecir atrasos de vuelos entregandole al modelo la siguiente información:
<ul>
  <li>Aerolínea: Aerolinea con la que se viajó <span id="aerolinea"></span></li>
  <li>TIPO VUELO: Si el vuelo es internacional<span id="tipo_vuelo"></span></li>
  <li>MES: Mes del viaje<span id="mes"></span></li>
  <li>temporada alta: Si el viaje fue en temporada alta <span id="temporada_alta"></span></li>
  <li>DIA: El día del mes en el que se viajó<span id="dia"></span></li>
  <li>DIANOM: El día de la semana en el que se viajó<span id="dianom"></span></li>
  <li>periodo_dia: Si se viajó en mañana, tarde o noche<span id="periodo_dia"></span></li>
  <li>FECHA: La fecha del viaje <span id="fecha"></span></li>
  <li>SIGLADES: Nombre de la ciudad de destino <span id="siglades"></span></li>
  <li>SIGLAORI: Nombre de la ciudad de origen<span id="siglaori"></span></li>
</ul>

# Instalación: 
Además, se recomienda fuertemente inicializar otro ambiente de python (este documento se encuentra en python 3.8), para realizar dicha inicialización en caso de contar con anaconda, se proporciona un archivo environment.yml, el cual puede ser corrido utilizando el siguiente comando: 

1. instalar anaconda: https://dev.to/waylonwalker/installing-miniconda-on-linux-from-the-command-line-4ad7
2. instalar el ambiente: 
```bash
conda env create -f environment.yml
```
