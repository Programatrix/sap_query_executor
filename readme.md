# SAP SQL Executor

Microservicio desarrollado con **FastAPI** para ejecutar consultas SQL de forma segura contra bases de datos **SAP HANA** o **SQL Server**, con soporte multiusuario y gestión de conexiones.

---

## 🚀 Características principales

- 🔒 Ejecución segura de consultas (`SELECT` solamente)
- 👤 Multiusuario (conexiones asociadas a cada usuario)
- 💾 Almacenamiento de conexiones por usuario
- 📡 Soporte para SAP HANA y SQL Server
- 🧩 API REST compatible con Swagger / OpenAPI

---

## 📦 Requisitos

- Python 3.10+
- SAP HANA Client (`hdbcli`)
- Driver ODBC para SQL Server (`pyodbc`)

---

## 📁 Instalación

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API estará disponible en:
```
http://localhost:8000/docs
```

---

## 🔧 Estructura básica del proyecto

```
sap_query_executor/
├── app/
│   ├── main.py
│   ├── models.py
│   └── db/
│       ├── hana.py
│       ├── sql.py
│       └── storage.py
├── connections/        # Archivos JSON por usuario
├── requirements.txt
└── README.md
```

---

## 🔐 Headers necesarios

Cada petición debe incluir:

```http
X-User-Id: <nombre_usuario>
```

---

## 🔄 Endpoints disponibles

### `POST /connections`
Crea una nueva conexión para un usuario.

### `GET /connections`
Devuelve una lista de conexiones registradas para el usuario.

### `PUT /connections/{connection_id}`
Actualiza una conexión existente.

### `DELETE /connections/{connection_id}`
Elimina una conexión del usuario.

### `POST /execute_query`
Ejecuta una consulta sobre una conexión válida del usuario.

---

## 🧪 Ejemplo de ejecución de consulta

```json
{
  "engine": "hana",
  "query": "SELECT * FROM \"OITM\" LIMIT 5",
  "connection_id": "hana_local"
}
```

Header:
```
X-User-Id: user1
```

---

## ✅ Próximas mejoras sugeridas

- Middleware para validación de tokens (autenticación real)
- Endpoint `/test_connection`
- Soporte para otras bases de datos (PostgreSQL, MySQL)
- Auditoría de consultas por usuario

---

## 🧠 Licencia
Uso interno / proyecto privado. Adaptable a entornos empresariales.

