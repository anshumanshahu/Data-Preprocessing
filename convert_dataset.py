
import csv
import html
import re
from pathlib import Path

folder = Path(__file__).resolve().parent
input_file = folder / "train.csv"
output_file = folder / "jigsaw_output.csv"

label_columns = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate",
]

def clean_text(text):
    text = html.unescape(text)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove IP addresses
    text = re.sub(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b", " ", text
    )

    # Remove common leftover wiki navigation phrases
    text = re.sub(
        r"\b(?:talk|contribs)\b", " ", text, flags=re.IGNORECASE
    )

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


saved = 0
skipped = 0

try:
    with input_file.open(
        "r", encoding="utf-8-sig", newline=""
    ) as infile:
        reader = csv.DictReader(infile)

        if not reader.fieldnames:
            raise ValueError("Dataset header is missing.")

        columns = {
            name.strip().lower(): name
            for name in reader.fieldnames
            if name
        }

        text_column = (
            columns.get("comment_text")
            or columns.get("text")
            or columns.get("comment")
        )

        available_labels = [
            columns[name]
            for name in label_columns
            if name in columns
        ]

        if not text_column or not available_labels:
            raise ValueError(
                "Expected comment_text/text and toxicity label columns. "
                "Use the original dataset CSV with its header."
            )

        with output_file.open(
            "w", encoding="utf-8-sig", newline=""
        ) as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["text", "label"])

            for row in reader:
                text = clean_text(row.get(text_column) or "")

                if not text:
                    skipped += 1
                    continue

                values = [
                    str(row.get(col, "0")).strip()
                    for col in available_labels
                ]

                if any(value not in {"0", "1"} for value in values):
                    skipped += 1
                    continue

                label = int(any(value == "1" for value in values))

                writer.writerow([text, label])
                saved += 1

    print("Dataset cleaned successfully!")
    print(f"Rows saved: {saved}")
    print(f"Rows skipped: {skipped}")
    print(f"Output: {output_file}")

except (OSError, ValueError, csv.Error) as error:
    print(f"Error: {error}")
