import csv
from datetime import datetime
from decimal import Decimal

import pytest

from models import api_models as am
from utils.create_file_report import create_report_file


@pytest.mark.asyncio
async def test_create_rates_file():
    rates = [
        am.Rate(
            Cur_ID=1,
            Date=datetime(2022, 1, 1),
            Cur_Abbreviation="USD",
            Cur_Name="Доллар США",
            Cur_Scale=1,
            Cur_OfficialRate=Decimal(1.5),
        ),
        am.Rate(
            Cur_ID=1,
            Date=datetime(2022, 1, 2),
            Cur_Abbreviation="USD",
            Cur_Name="Доллар США",
            Cur_Scale=1,
            Cur_OfficialRate=Decimal(2.5),
        ),
    ]
    file = create_report_file(rates)
    assert file

    file_data = list(csv.DictReader(file))
    assert len(file_data) == 2
    assert file_data[0] == {
        "Cur_ID": "1",
        "Date": "2022-01-01 00:00:00",
        "Cur_Abbreviation": "USD",
        "Cur_Name": "Доллар США",
        "Cur_Scale": "1",
        "Cur_OfficialRate": "1.5",
    }

    assert file_data[1] == {
        "Cur_ID": "1",
        "Date": "2022-01-02 00:00:00",
        "Cur_Abbreviation": "USD",
        "Cur_Name": "Доллар США",
        "Cur_Scale": "1",
        "Cur_OfficialRate": "2.5",
    }
