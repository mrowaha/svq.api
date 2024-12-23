from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi import Depends
from io import BytesIO
from persistence.blob import IBlobPersistence
from persistence.injectors import getBlobStorage
from .exceptions import UnsupportedFileType, DatasourceNotFoundError
from models import engine, Datasource
allowed_types = ["application/pdf",
                 "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]


class DatasourceService:
    def __init__(self, blob_persistence: IBlobPersistence):
        self.blob_persistence = blob_persistence

    def create_datasource(self: "DatasourceService", datasource: str) -> int:
        with Session(engine) as s:
            datasource = Datasource(name=datasource)
            s.add(datasource)
            s.commit()
            s.refresh(datasource)
            print(f"Created Datasource with ID: {datasource.id}")
            created_id = int(datasource.id)
            return created_id

    def delete_datasource(self: "DatasourceService", datasource_id: int):
        # Delete the Datasource
        with Session(engine) as session:
            try:
                datasource = session.query(
                    Datasource).filter_by(id=datasource_id).one()
                session.delete(datasource)
                session.commit()
                print(f"Datasource with ID {datasource_id} has been deleted.")
            except NoResultFound:
                print(f"Datasource with ID {datasource_id} does not exist.")
                raise DatasourceNotFoundError()
            except Exception as e:
                session.rollback()
                print(f"An error occurred: {e}")
                raise e

    def upload_file(self: "DatasourceService", datasource: str, file: str, data: bytes, *, content_type: str = "application/pdf", enable_ocr: bool = False, extract_tables: bool = False):
        if content_type not in allowed_types:
            raise UnsupportedFileType()

        meta = {
            "enable_ocr": str(enable_ocr).lower(),
            "extract_tables": str(extract_tables).lower(),
            "original_filename": file,
            "content_type": content_type
        }

        bucket_name = f"docs-{datasource}"
        self.blob_persistence.createBucket(bucket_name)

        self.blob_persistence.uploadFile(
            file,
            bucket=bucket_name,
            size=len(data),
            data=BytesIO(data),
            type=content_type,
            metadata=meta
        )


def get_datasource_service(blob_persistence: IBlobPersistence = Depends(getBlobStorage)) -> DatasourceService:
    return DatasourceService(blob_persistence)
