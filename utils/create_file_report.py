import csv
import io

from models import api_models as am


def create_report_file(content: list[dict]) -> io.StringIO:
    """
    Create a report file based on the provided content.

    Parameters:
        content (list[am.Rate]): The list of Rate objects to be included in the report.

    Returns:
        memory_file (io.StringIO): The in-memory file containing the report data.
    """
    if not content:
        return None
    memory_file = io.StringIO()
    fieldnames = content[0]["properties"].keys()
    writer = csv.DictWriter(memory_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in content:
        writer.writerow(row)
    memory_file.seek(0)
    return memory_file
