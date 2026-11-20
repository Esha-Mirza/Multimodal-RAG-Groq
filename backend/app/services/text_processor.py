
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

        if len(paragraph) > chunk_size:

            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            words = paragraph.split()
            word_chunks = []
            current_words = []
            current_length = 0

            for word in words:

                additional_length = len(word)

                if current_words:
                    additional_length += 1

                if current_length + additional_length > chunk_size:

                    word_chunks.append(" ".join(current_words))

                    overlap_words = []
                    overlap_length = 0

                    for previous_word in reversed(current_words):

                        required_length = len(previous_word)

                        if overlap_words:
                            required_length += 1

                        if overlap_length + required_length > overlap:
                            break

                        overlap_words.insert(0, previous_word)
                        overlap_length += required_length

                    current_words = overlap_words
                    current_length = overlap_length

                current_words.append(word)

                if current_length:
                    current_length += 1

                current_length += len(word)

            if current_words:
                word_chunks.append(" ".join(current_words))

            chunks.extend(word_chunks)

            continue

        if not current_chunk:
            current_chunk = paragraph

        elif len(current_chunk) + 2 + len(paragraph) <= chunk_size:

            current_chunk += "\n\n" + paragraph

        else:
            chunks.append(current_chunk)
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
