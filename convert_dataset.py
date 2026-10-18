
import csv
import re
import html
from pathlib import Path

folder = Path(__file__).resolve().parent
input_file = folder / "dataset.csv"
output_file = folder / "output.csv"


def clean_text(text):
    # Decode HTML entities such as &amp;
    text = html.unescape(text)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # Remove hashtags but keep the hashtag word
    text = re.sub(r"#(\w+)", r"\1", text)

    # Remove user mentions
    text = re.sub(r"@\w+", "", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def read_rows(path):
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            with path.open(
                "r", encoding=encoding, newline=""
            ) as f:
                return list(csv.reader(f))
        except UnicodeDecodeError:
            continue

    raise ValueError("Could not decode input CSV.")


try:
    rows = read_rows(input_file)

    if not rows:
        raise ValueError("dataset.csv is empty.")

    first = [x.strip().lower() for x in rows[0]]

    # Support a header if present
    if "text" in first:
        text_index = first.index("text")
        label_indexes = [
            first.index(x)
            for x in ("label", "label1", "label2")
            if x in first
        ]

        if not label_indexes:
            label_indexes = list(range(len(first) - 2, len(first)))

        data = rows[1:]
    else:
        # Sample format: ID, tweet_id, text, label1, label2
        text_index = 2
        label_indexes = [3, 4]
        data = rows

    count = 0
    skipped = 0

    with output_file.open(
        "w", encoding="utf-8-sig", newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])

        for row in data:
            if len(row) <= max([text_index] + label_indexes):
                skipped += 1
                continue

            text = clean_text(row[text_index])

            labels = {
                row[i].strip().upper()
                for i in label_indexes
            }

            if not text:
                skipped += 1
                continue

            # Any harmful category means 1
            if labels & {"HOF", "PRFN", "OFFN"}:
                label = 1
            elif labels & {"NOT", "NONE"}:
                label = 0
            else:
                skipped += 1
                continue

            writer.writerow([text, label])
            count += 1

    print("Dataset converted successfully!")
    print(f"Rows saved: {count}")
    print(f"Rows skipped: {skipped}")
    print(f"Output: {output_file}")

except (OSError, ValueError, csv.Error) as e:
    print(f"Error: {e}")
