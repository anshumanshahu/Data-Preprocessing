import csv
from pathlib import Path

folder = Path(__file__).resolve().parent
input_file = folder / "Hate_Hindi.csv"
output_file = folder / "Hate_Hindi_output.csv"

label_mapping = {
    "not offensive": 0,
    "offensive": 1
}

total = 0
skipped = 0

try:
    with input_file.open("r", encoding="utf-8-sig") as file, \
         output_file.open("w", encoding="utf-8-sig", newline="") as out:

        writer = csv.writer(out)
        writer.writerow(["text", "label"])

        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                row = next(csv.reader([line], skipinitialspace=True))

                if len(row) != 2:
                    skipped += 1
                    print(f"Skipping line {line_number}: invalid format")
                    continue

                text = row[0].strip()
                label_text = row[1].strip().lower()

                if not text or label_text not in label_mapping:
                    skipped += 1
                    print(f"Skipping line {line_number}: invalid text or label")
                    continue

                writer.writerow([text, label_mapping[label_text]])
                total += 1

            except csv.Error:
                skipped += 1
                print(f"Skipping line {line_number}: CSV parsing error")

    print("\nDataset conversion complete!")
    print(f"Rows saved: {total}")
    print(f"Rows skipped: {skipped}")
    print(f"Output file: {output_file}")

except FileNotFoundError:
    print(f"Error: {input_file} not found. Create Hate_Hindi.csv first.")
except OSError as error:
    print(f"File error: {error}")