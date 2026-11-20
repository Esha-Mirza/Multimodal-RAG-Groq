
from app.services.document_service import extract_pdf_content
from app.services.text_processor import split_text


pdf_path = input("Enter PDF path: ").strip().strip('"')

print("\nPDF CHUNKING TEST")
print("-----------------")

try:
    result = extract_pdf_content(
        file_path=pdf_path,
        source="pdf_chunking_test"
    )

    all_chunks = []

    for page in result["pages"]:

        page_chunks = split_text(
            page["text"],
            chunk_size=500,
            overlap=100
        )

        for chunk_index, chunk in enumerate(page_chunks):

            all_chunks.append({
                "page_number": page["page_number"],
                "chunk_index": chunk_index,
                "text": chunk
            })

    print("Total PDF pages:", result["total_pages"])
    print("Total text chunks:", len(all_chunks))

    print("\nFIRST 5 CHUNKS")
    print("--------------")

    for chunk in all_chunks[:5]:

        print("\nPage:", chunk["page_number"])
        print("Chunk:", chunk["chunk_index"])
        print("Characters:", len(chunk["text"]))
        print("Text:", chunk["text"])

except Exception as error:
    print("\nERROR:")
    print(error)
