import csv
import io

from models import api_models as am


def create_report_file(content: list[am.Rate]):
    if not content:
        return None
    memory_file = io.StringIO()
    fieldnames = content[0].schema()["properties"].keys()
    writer = csv.DictWriter(memory_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in content:
        writer.writerow(row.dict())
    memory_file.seek(0)
    return memory_file
