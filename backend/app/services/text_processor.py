
def split_text(text, chunk_size=500, overlap=100):

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size.")

    text = text.replace("\r\n", "\n").strip()

    if not text:
        return []

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # Split paragraphs that are larger than chunk_size
        if len(paragraph) > chunk_size:

            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            start = 0

            while start < len(paragraph):

                end = start + chunk_size
                chunk = paragraph[start:end]

                if chunk.strip():
                    chunks.append(chunk.strip())

                start += chunk_size - overlap

            continue

        # Add paragraph to the current chunk if it fits
        if not current_chunk:
            current_chunk = paragraph

        elif len(current_chunk) + 2 + len(paragraph) <= chunk_size:

            current_chunk += "\n\n" + paragraph

        else:
            chunks.append(current_chunk)

            # Start the next chunk with the new paragraph
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
