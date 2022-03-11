import csv
import os

from django.core.files import File

from fakeCSV.celery import app

from .models import Dataset, Schema
from .services import get_fake_field


def generate_csv_file(
    filename: str, rows_num: int, schema_id: int, dataset_id: int
) -> None:
    schema = Schema.objects.get(pk=schema_id)
    columns = schema.schema_columns.order_by("order")

    with open(filename, "w") as file:
        writer = csv.writer(
            file, delimiter=schema.column_separator, quotechar=schema.string_character
        )

        # write headers
        writer.writerow([column.name for column in columns])

        # write fake data
        for row_num in range(rows_num):
            row = []
            for column_num, column in enumerate(columns):
                fake_field = get_fake_field(
                    columns[column_num].type,
                    columns[column_num].start_value,
                    columns[column_num].end_value,
                )
                row.append(fake_field)
            writer.writerow(row)

    dataset = Dataset.objects.get(pk=dataset_id)
    with open(filename, "rb") as file:
        dataset.csv_file = File(file)
        dataset.status = Dataset.READY
        dataset.save()

    # Delete excess csv_file
    if os.path.exists(filename):
        print("REMOVED")
        os.remove(filename)