# FastAPI + PostgreSQL - API REST

API REST desarrollada con FastAPI y PostgreSQL, utilizando SQLAlchemy como ORM y Alembic para migraciones de base de datos. El proyecto está completamente dockerizado para facilitar el desarrollo y despliegue.

## 🚀 Tecnologías

- **FastAPI** - Framework web moderno y rápido para construir APIs
- **PostgreSQL 16** - Base de datos relacional
- **SQLAlchemy** - ORM para Python con soporte async
- **Alembic** - Herramienta de migraciones de base de datos
- **Docker & Docker Compose** - Containerización
- **Pytest** - Framework de testing con soporte async
- **Pydantic** - Validación de datos

## 📁 Estructura del Proyecto

```
FastAPISQL/
├── app/
│   ├── crud/           # Operaciones CRUD
│   ├── models/         # Modelos SQLAlchemy
│   ├── routers/        # Endpoints de la API
│   ├── schemas/        # Esquemas Pydantic
│   ├── database.py     # Configuración de base de datos
│   └── main.py         # Aplicación principal
├── alembic/
│   └── versions/       # Migraciones de base de datos
├── tests/              # Tests unitarios e integración
├── docker-compose.yml  # Orquestación de servicios
├── Dockerfile          # Imagen de la aplicación
├── requirements.txt    # Dependencias Python
├── pytest.ini          # Configuración de pytest
└── .env                # Variables de entorno
```

## 🔧 Requisitos Previos

- Docker Desktop instalado
- Docker Compose

## ⚙️ Configuración

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd FastAPISQL
```

2. **Configurar variables de entorno**

El archivo `.env` ya contiene la configuración por defecto:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app_db
```

## 🐳 Ejecución con Docker

### Iniciar los servicios

**Modo normal (con logs en consola):**
```bash
docker-compose up
```

**Modo detached (en segundo plano):**
```bash
docker-compose up -d
```

**Reconstruir imágenes:**
```bash
docker-compose up --build
```

### Ver logs
```bash
docker-compose logs -f
docker-compose logs -f api  # Solo API
docker-compose logs -f db   # Solo PostgreSQL
```

### Detener servicios
```bash
docker-compose down
```

### Detener y eliminar volúmenes (⚠️ BORRA DATOS)
```bash
docker-compose down -v
```

## 🌐 Endpoints

La API estará disponible en: **http://localhost:8000**

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Mensaje de bienvenida |
| POST | `/users/` | Crear un nuevo usuario |
| GET | `/users/` | Listar todos los usuarios |
| GET | `/users/{user_id}` | Obtener un usuario por ID |
| PUT | `/users/{user_id}` | Actualizar un usuario |
| DELETE | `/users/{user_id}` | Eliminar un usuario |

### Ejemplo de uso

**Crear usuario:**
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "age": 30,
    "cellphone": "555-1234"
  }'
```

## 🧪 Testing

### Ejecutar todos los tests
```bash
pytest -v
```

### Ejecutar tests con coverage
```bash
pytest --cov=app
```

### Ejecutar tests dentro del contenedor
```bash
docker-compose exec api pytest -v
```

## 🗄️ Migraciones de Base de Datos

### Crear una nueva migración
```bash
docker-compose exec api alembic revision --autogenerate -m "descripción del cambio"
```

### Aplicar migraciones
```bash
docker-compose exec api alembic upgrade head
```

### Revertir última migración
```bash
docker-compose exec api alembic downgrade -1
```

### Ver historial de migraciones
```bash
docker-compose exec api alembic history
```

## 💾 Backup y Restauración

### Crear backup
```bash
docker-compose exec db pg_dump -U postgres app_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restaurar backup
```bash
docker-compose exec -T db psql -U postgres app_db < backup.sql
```

## 📊 Base de Datos

### Conexión directa a PostgreSQL
```bash
docker-compose exec db psql -U postgres -d app_db
```

### Credenciales por defecto
- **Usuario**: postgres
- **Contraseña**: postgres
- **Base de datos**: app_db
- **Puerto**: 5432

## 🔄 Recarga Automática

El proyecto está configurado con volúmenes de Docker que permiten la recarga automática de código:
- Cualquier cambio en archivos `.py` se refleja automáticamente
- No es necesario reconstruir la imagen para cambios de código
- Solo reconstruye si cambias `requirements.txt`

## 🛠️ Desarrollo Local (sin Docker)

Si prefieres ejecutar sin Docker, necesitarás:

1. **Instalar PostgreSQL localmente**
2. **Crear un entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Actualizar DATABASE_URL en .env**
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/app_db
```

5. **Ejecutar migraciones**
```bash
alembic upgrade head
```

6. **Iniciar servidor**
```bash
uvicorn app.main:app --reload
```

## 📝 Notas Importantes

- Los datos persisten en volúmenes de Docker, no se pierden al reconstruir imágenes
- Solo usa `docker-compose down -v` si quieres eliminar los datos
- Las migraciones se ejecutan automáticamente al iniciar el contenedor
- El código se recarga automáticamente gracias a `--reload` de uvicorn

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
