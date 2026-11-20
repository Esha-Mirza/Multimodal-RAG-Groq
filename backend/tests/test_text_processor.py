
from app.services.text_processor import split_text


print("\nTEXT PROCESSOR TEST")
print("-------------------")


# Test 1: Empty text
result = split_text("")
print("Empty text:", result)


# Test 2: Short text
result = split_text("This is a short paragraph.")
print("Short text:", result)


# Test 3: Long text
long_text = "Artificial intelligence is changing the world. " * 30

result = split_text(
    long_text,
    chunk_size=100,
    overlap=20
)

print("\nLong text chunks:", len(result))

for index, chunk in enumerate(result):
    print(f"\nChunk {index + 1}:")
    print(chunk)
    print("Characters:", len(chunk))


# Test 4: Invalid chunk size
try:
    split_text("Test text", chunk_size=0)
except ValueError as error:
    print("\nInvalid chunk size:", error)


# Test 5: Invalid overlap
try:
    split_text("Test text", chunk_size=100, overlap=100)
except ValueError as error:
    print("Invalid overlap:", error)


print("\nAll tests completed.")
