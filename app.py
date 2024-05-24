import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title='Strategy Monitoring (Novell)', page_icon='📈')
st.title('Strategy Monitoring (Novell)')

ASSETS = ['SHY', 'IEF', 'TLT', 'TIP', 'LQD', 'HYG', 'BWX', 'EMB', 'BIL']
# PERIODS = [3, 5, 8, 13, 21, 34, 55]
PERIODS = [5, 10, 20, 60, 120]

@st.cache_data(ttl='1m')
def get_data(ticker):
    return yf.Ticker(ticker).history(period='1y').Close

def get_score(ticker, period):
    data = get_data(ticker).tail(period)
    return data.iloc[-1] / data.iloc[0] - 1

def get_total_score(ticker):
    return sum([get_score(ticker, period) for period in PERIODS]) / len(PERIODS) * 252

def get_signal(df):
    BIL = df.loc['BIL', 'Score']
    top3 = df.iloc[2]['Score']
    handler = lambda x: '🤗' if x > BIL and x >= top3 else '🫠' if x < 0 else '🫥'
    return df['Score'].apply(handler)

def get_bond_col():
    scores = {ticker: get_total_score(ticker) for ticker in ASSETS}
    df = pd.DataFrame(scores.items(), columns=['Asset', 'Score'])
    df = df.set_index('Asset')
    df = df.sort_values('Score', ascending=False)
    df['Signal'] = get_signal(df)
    st.dataframe(df)

# cols = st.columns(2)
# with cols[0]:
get_bond_col()

# ASSETS2 = ['TQQQ', 'SOXL', 'FNGU', 'TECL', 'TNA', 'FAS', 'LABU', 'BULZ', 'DPST']

# def get_signal2(df):
#     TQQQ = df.loc['TQQQ', 'Score']
#     handler = lambda x: '🤗' if x > TQQQ else '🫠' if x < 0 else '🫥'
#     return df['Score'].apply(handler)

# def get_lev_col():
#     scores = {ticker: get_total_score(ticker) for ticker in ASSETS2}
#     df = pd.DataFrame(scores.items(), columns=['Asset', 'Score'])
#     df = df.set_index('Asset')
#     df = df.sort_values('Score', ascending=False)
#     df['Signal'] = get_signal2(df)
#     st.dataframe(df, use_container_width=True)


# with cols[1]:
#     st.header('Leveraged')
#     get_lev_col()