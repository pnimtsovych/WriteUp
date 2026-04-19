from pathlib import Path
import unicodedata

filename = "txt (7)"

data = Path(filename).read_text()

# space = 0, tab = 1
bits = ''.join('0' if ch == ' ' else '1' for ch in data)

# Convert every 8 bits into ASCII
hex_text = ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

# Split hex tokens
tokens = hex_text.split()

# Convert hex -> Unicode characters
decoded = ''.join(chr(int(token, 16)) for token in tokens)

# Normalize fullwidth Unicode characters into normal ASCII
flag = unicodedata.normalize("NFKC", decoded)

print("Intermediate:", hex_text)
print("Decoded:", decoded)
print("Flag:", flag)
