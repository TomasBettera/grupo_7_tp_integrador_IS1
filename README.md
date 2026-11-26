# grupo_7_tp_integrador_IS1
## Integrantes
| Nombre y Apellido | DNI | Correo Electrónico |
| :--- | :--- | :--- |
| **Tomás Bettera** | 45.938.735 | [tomasbettera10@gmail.com](mailto:tomasbettera10@gmail.com) |
| **Aldo Maximiliano Martinez** | 46.174.656 | [maximiliano10439@gmail.com](mailto:maximiliano10439@gmail.com) |
| **Ignacio Talio Liseno** | 46.397.648 | [ignacioliseno@gmail.com](mailto:ignacioliseno@gmail.com) |
| **Joaquín Mateo Dutto** | 46.660.718 | [joaquinduttoo@gmail.com](mailto:joaquinduttoo@gmail.com) |

## Estructura del proyecto
```
grupo_7_tp_integrador_IS1/
├── README.md
├── diagrama.pdf                # Diagrama de clases
├── .gitignore
└── tp-integrador/
    ├── run.py                  # Arranque de la aplicación
    ├── requirements.txt        # Dependencias
    ├── tests/                  # Pruebas automáticas (pytest)
    └── src/
        ├── __init__.py         # create_app()
        ├── extensions.py       # db = SQLAlchemy()
        ├── models/             # Clases que se guardan en la base de datos
        ├── estrategia/         # Patrón Strategy (modelos de IA)
        ├── factories/          # Patrón Factory Method (autores)
        └── services/           # Generador de respuestas y monitor
```

    
## Stack tecnológico utilizado
- **Lenguaje:** Python 3.15
- **Backend:** Flask
- **Persistencia:** Flask-SQLAlchemy con SQLite
- **Dependencias:** pip (`requirements.txt`)

## Ejecución del Proyecto
 
**Requisito:** tener Python instalado.
 
1. Clonar el repositorio y entrar a la carpeta del proyecto:
```bash
git clone https://github.com/TomasBettera/grupo_7_tp_integrador_IS1.git
cd grupo_7_tp_integrador_IS1
```
 
2. Crear un entorno virtual y activarlo:
```bash
python -m venv venv
venv\Scripts\activate
```
 
3. Instalar las dependencias:
```bash
python -m pip install -r requirements.txt
```
 
4. Ejecutar el programa:
```bash
python run.py
```

## Justificación del Diagrama de Clases
 
### Patrón Strategy
 
Se utilizó Strategy porque cada modelo de IA (OpenAI, Gemini y local) cumple el mismo contrato: recibe un prompt y devuelve una respuesta. Esto permite tratarlos como opciones intercambiables, sin modificar el resto del sistema. Para agregar una opción nueva, simplemente se crea otra clase que implemente `EstrategiaLLM`.
 
### Patrón Factory Method

Se utilizó Factory Method porque no se necesita construir familias de objetos distintos que deban combinarse entre ellos: solo se fabrica una única entidad, el `Autor`. Cada fábrica concreta (`FabricaUsuario` y `FabricaAgenteIA`) decide qué subclase crear, y así el resto del código trabaja con `Autor` sin depender de las clases concretas.

 ---

