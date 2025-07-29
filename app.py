import streamlit as st
import pandas as pd

# タイトル
st.title("CSVデータの絞り込みアプリ")

# 事前に決まったCSVファイルを読み込む
DATA_FILE = "tanagyou_address.csv"  # ファイル名を指定
df = pd.read_csv(DATA_FILE)

st.write("データのプレビュー")
st.dataframe(df)

# 絞り込み条件の設定
st.sidebar.header("絞り込み条件")

filters = {}
for col in df.columns:
    if df[col].dtype == 'object':  # 文字列カラム
        options = df[col].dropna().unique()
        selected = st.sidebar.multiselect(f"{col} を選択", options)
        if selected:
            filters[col] = selected
    else:  # 数値カラム
        clean_col = df[col].dropna()
        if not clean_col.empty:
            min_val = float(clean_col.min())
            max_val = float(clean_col.max())
            selected_range = st.sidebar.slider(f"{col} の範囲", min_val, max_val, (min_val, max_val))
            filters[col] = selected_range

# データのフィルタリング
filtered_df = df.copy()
for col, condition in filters.items():
    if isinstance(condition, list):  # カテゴリ選択
        filtered_df = filtered_df[filtered_df[col].isin(condition)]
    else:  # 数値範囲
        filtered_df = filtered_df[(filtered_df[col] >= condition[0]) & (filtered_df[col] <= condition[1])]

st.write("絞り込み結果")
st.dataframe(filtered_df)
