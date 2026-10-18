import csv
from pathlib import Path

folder = Path(__file__).resolve().parent
input_file = folder / "hindi_dataset.tsv"
output_file = folder / "hindi_dataset_output_6.csv"

label_mapping = {
    "NOT": 0,
    "HOF": 1
}

saved = 0
skipped = 0

try:
    with input_file.open("r", encoding="utf-8-sig", newline="") as infile:
        reader = csv.DictReader(infile, delimiter="\t")

        required_columns = {"text", "task_1"}
        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                "Required columns missing. Expected at least: text, task_1"
            )

        with output_file.open(
            "w", encoding="utf-8-sig", newline=""
        ) as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["text", "label"])

            for row in reader:
                text = (row.get("text") or "").strip()
                task_label = (row.get("task_1") or "").strip().upper()

                if not text or task_label not in label_mapping:
                    skipped += 1
                    continue

                writer.writerow([text, label_mapping[task_label]])
                saved += 1

    print("Dataset conversion complete!")
    print(f"Rows saved: {saved}")
    print(f"Rows skipped: {skipped}")
    print(f"Output file: {output_file}")

except (OSError, ValueError, csv.Error) as error:
    print(f"Error: {error}")