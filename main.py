import datetime
import time
from io import BytesIO

import pandas as pd
import requests
import streamlit as st


def fetch_csv(url):
    print(url)
    res = requests.get(url)
    df = pd.read_csv(BytesIO(res.content), sep=",")
    return df


def show_graph(df, options):
    time.sleep(0.1)
    for option in options:
        # st.dataframe(df)
        _df = df[option]

        st.title(option)
        col1, col2 = st.columns(2)
        col1.metric("新規感染者数(前日比)", f"{_df[-1]}人", f"{_df[-1] - _df[-2]}人")
        col2.metric(
            "7日平均(当日比)", f"{_df[-7:].mean():.1f}人", f"{_df[-7:].mean() - _df[-1]:.1f}人"
        )

        # st.dataframe(_df)
        st.bar_chart(_df)


if __name__ == "__main__":
    # コロナデータの読み込み
    df = fetch_csv(
        url="https://www3.nhk.or.jp/n-data/opendata/coronavirus/nhk_news_covid19_prefectures_daily_data.csv"
    )

    # 前処理
    df["日付"] = pd.to_datetime(df["日付"])
    df = df.rename(columns={"各地の感染者数_1日ごとの発表数": "感染者数"})
    df = df[df["日付"] >= df["日付"].max() - datetime.timedelta(100)]
    df = pd.pivot_table(df, index="日付", columns="都道府県名", values="感染者数")
    df["全国"] = df.sum(axis=1)

    # 画面作成
    options = st.sidebar.multiselect("都道府県を選択", tuple(df.columns), ["全国"])

    show_graph(df, options)
