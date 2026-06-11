from __future__ import annotations

DEFAULT_ELO = 1500.0

TEAM_ELO: dict[str, float] = {
    "ARG": 1885,
    "ESP": 1875,
    "FRA": 1868,
    "ENG": 1825,
    "BRA": 1810,
    "POR": 1795,
    "NED": 1785,
    "BEL": 1765,
    "GER": 1750,
    "CRO": 1710,
    "URU": 1705,
    "COL": 1690,
    "MAR": 1685,
    "USA": 1660,
    "MEX": 1645,
    "SUI": 1640,
    "JPN": 1635,
    "SEN": 1620,
    "ECU": 1615,
    "IRN": 1600,
    "KOR": 1590,
    "AUS": 1580,
    "SWE": 1575,
    "CAN": 1565,
    "TUR": 1560,
    "CIV": 1555,
    "EGY": 1540,
    "NOR": 1535,
    "PAR": 1525,
    "AUT": 1520,
    "SCO": 1515,
    "QAT": 1495,
    "TUN": 1490,
    "GHA": 1485,
    "KSA": 1475,
    "RSA": 1460,
    "PAN": 1455,
    "BIH": 1450,
    "CZE": 1445,
    "UZB": 1440,
    "ALG": 1435,
    "IRQ": 1425,
    "JOR": 1415,
    "CPV": 1410,
    "NZL": 1400,
    "HAI": 1385,
    "CUW": 1375,
    "COD": 1370,
}


def expected_result(rating_a: float, rating_b: float) -> float:
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def get_team_elo(team_code: str) -> float:
    return TEAM_ELO.get(team_code.upper(), DEFAULT_ELO)
