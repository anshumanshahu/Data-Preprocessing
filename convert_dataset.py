
import csv
from pathlib import Path

folder = Path(__file__).resolve().parent
input_file = folder / "dataset.csv"
output_file = folder / "output.csv"

def read_csv(path):
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            with path.open(
                "r", encoding=encoding, newline=""
            ) as f:
                return list(csv.reader(f))
        except UnicodeDecodeError:
            continue

    raise ValueError("Unable to read CSV encoding.")

try:
    rows = read_csv(input_file)
    output_words = []

    for index, row in enumerate(rows):
        if len(row) < 2:
            continue

        # Skip header if present
        if index == 0 and row[0].strip().lower() in (
            "word", "text", "term"
        ):
            continue

        original_word = row[0].strip()
        english_word = row[1].strip()

        if original_word:
            output_words.append([original_word, 1])

        if english_word:
            output_words.append([english_word, 1])

    with output_file.open(
        "w", encoding="utf-8-sig", newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(output_words)

    print("Conversion successful!")
    print(f"Total words: {len(output_words)}")
    print(f"Saved to: {output_file}")

except (OSError, ValueError, csv.Error) as error:
    print(f"Error: {error}")
