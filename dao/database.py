from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Datos de conexión a MySQL
DATABASE_URL = "mysql+pymysql://root:JvtT6kDS2dcSlDL@localhost:3306/gym"

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear la clase SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una sesión de la base de datos
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
