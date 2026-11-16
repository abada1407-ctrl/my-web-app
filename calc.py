"""장비 가동률 계산 함수."""

import pandas as pd


def load_readiness(path) -> pd.DataFrame:
    """가동 현황 CSV를 UTF-8 BOM 인코딩으로 읽는다."""
    return pd.read_csv(path, encoding="utf-8-sig")


def total_rate(df: pd.DataFrame) -> float:
    """전체 가동률(%)을 계획시간과 가동시간의 합계로 계산한다."""
    planned = df["계획시간(h)"].sum()
    operating = df["가동시간(h)"].sum()
    if planned == 0:
        return 0.0
    return round(float(operating / planned * 100), 1)


def rate_by_equipment(df: pd.DataFrame) -> pd.DataFrame:
    """장비별 계획시간, 가동시간, 가동률을 반환한다."""
    result = (
        df.groupby(["장비코드", "장비명"], as_index=False)[["계획시간(h)", "가동시간(h)"]]
        .sum()
        .rename(columns={"계획시간(h)": "계획시간", "가동시간(h)": "가동시간"})
    )
    result["가동률"] = result.apply(
        lambda row: round(float(row["가동시간"] / row["계획시간"] * 100), 1)
        if row["계획시간"] != 0
        else 0.0,
        axis=1,
    )
    return result[["장비코드", "장비명", "계획시간", "가동시간", "가동률"]]


def compare_weeks(prev: pd.DataFrame, cur: pd.DataFrame) -> pd.DataFrame:
    """두 주의 장비별 가동률과 증감을 증감 내림차순으로 반환한다."""
    prev_rates = rate_by_equipment(prev)[["장비코드", "장비명", "가동률"]].rename(
        columns={"가동률": "가동률_이전"}
    )
    cur_rates = rate_by_equipment(cur)[["장비코드", "장비명", "가동률"]].rename(
        columns={"가동률": "가동률_이번"}
    )
    result = prev_rates.merge(cur_rates, on=["장비코드", "장비명"], how="inner")
    result["증감"] = (result["가동률_이번"] - result["가동률_이전"]).round(1)
    return result[
        ["장비코드", "장비명", "가동률_이전", "가동률_이번", "증감"]
    ].sort_values("증감", ascending=False, kind="stable", ignore_index=True)
