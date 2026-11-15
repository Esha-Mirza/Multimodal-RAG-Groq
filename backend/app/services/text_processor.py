
def split_text(
    text,
    chunk_size=500,
    overlap=100
):
    chunks = []

    # Clean unnecessary spaces
    text = text.replace("\r\n", "\n")
    paragraphs = text.split("\n\n")

    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Add paragraph to the current chunk
        if len(current_chunk) + len(paragraph) <= chunk_size:

            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

        else:

            if current_chunk:
                chunks.append(current_chunk.strip())

            # Keep some text from the previous chunk
            if overlap > 0 and current_chunk:

                overlap_text = current_chunk[-overlap:]

                current_chunk = overlap_text + "\n\n" + paragraph

            else:
                current_chunk = paragraph

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
