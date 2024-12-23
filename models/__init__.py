from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection string format: postgresql://<username>:<password>@<host>:<port>/<database>
connection_string = "postgresql://admin:password@localhost:5433/svq"

# Create the engine
engine = create_engine(connection_string)
Base = declarative_base()


class Datasource(Base):
    __tablename__ = "datasources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
