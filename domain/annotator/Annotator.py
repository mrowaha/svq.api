import fitz  # PyMuPDF
from persistence.blob import IBlobPersistence
from dto.chunk import Chunk
from io import BytesIO


class Annotator:

    def __init__(self):
        ...

    def annotate(self, chunks: list[Chunk], blobPersistence: IBlobPersistence, *, bucket_name: str, file_name: str) -> bytes:
        temp_path = blobPersistence.load_pdf_temporarily(
            bucket_name, file_name)
        annotated_pagesteam = BytesIO()
        doc = fitz.open(temp_path)
        for chunk in chunks:
            pages = chunk.pages
            content = chunk.content

            for page_number in pages:
                page = doc[page_number-1]
                content_instances = page.search_for(
                    content, quads=True)
                if content_instances:
                    for inst in content_instances:
                        page.add_highlight_annot(inst)
                    single_page_doc = fitz.open()
                    single_page_doc.insert_pdf(
                        doc, from_page=page_number - 1, to_page=page_number - 1)
                    single_page_doc.save(annotated_pagesteam)
                    annotated_pagesteam.seek(0)
                    single_page_doc.close()
                    break
        doc.close()

        return annotated_pagesteam.getvalue()


def get_annotator() -> Annotator:
    return Annotator()
