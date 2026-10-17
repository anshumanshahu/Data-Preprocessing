
import csv
from pathlib import Path

folder = Path(__file__).resolve().parent
input_file = folder / "hate_speech.csv"
output_file = folder / "output_3.csv"


def read_csv_file(path):
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            with path.open(
                "r", encoding=encoding, newline=""
            ) as file:
                return list(csv.reader(file, delimiter="\t")), "\t"
        except UnicodeDecodeError:
            continue

    raise ValueError("Unable to read the input file.")


try:
    # Read file and detect its delimiter
    with input_file.open("r", encoding="utf-8-sig", errors="replace") as f:
        sample = f.read(8192)

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t;")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = "\t" if "\tyes" in sample or "\tno" in sample else ","

    with input_file.open(
        "r", encoding="utf-8-sig", errors="replace", newline=""
    ) as file:
        rows = list(csv.reader(file, delimiter=delimiter))

    if not rows:
        raise ValueError("hate_speech.csv is empty.")

    first_row = [col.strip().lower() for col in rows[0]]

    # Identify columns using header names when available
    if "text" in first_row and ("label" in first_row or "sentiment" in first_row):
        text_index = first_row.index("text")
        label_index = (
            first_row.index("label")
            if "label" in first_row
            else first_row.index("sentiment")
        )
        rows = rows[1:]
    else:
        # If no header: last column contains yes/no
        text_index = 0
        label_index = len(rows[0]) - 1

    converted = []
    skipped = 0

    for row in rows:
        if len(row) <= max(text_index, label_index):
            skipped += 1
            continue

        text = row[text_index].strip()
        original_label = row[label_index].strip().lower()

        if not text or original_label not in ("yes", "no"):
            skipped += 1
            continue

        label = 1 if original_label == "yes" else 0
        converted.append([text, label])

    if not converted:
        raise ValueError(
            "No valid rows found. Check the CSV delimiter and columns."
        )

    with output_file.open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["text", "label"])
        writer.writerows(converted)

    print("Dataset converted successfully!")
    print(f"Total rows: {len(converted)}")
    print(f"Skipped rows: {skipped}")
    print(f"Output: {output_file}")

except (OSError, ValueError, csv.Error) as error:
    print(f"Error: {error}")
