## Para ejecutar

### Crear entonrno virtual 
python -m venv venv

### Activar entorno (Se debe ejecutar en una PowerSheel)
venv\Scripts\activate

### Actualizar pythom
python -m pip install --upgrade pip

### Intalar dependencias
pip install -r requirements.txt

### Levantar el servidor
uvicorn main:app --reload