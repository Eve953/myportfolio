import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

st.title('Analysis')
st.divider()

col1, col2, col3 = st.columns(3) 

# intialize session state for user input
if 'portfolio' not in st.session_state:
    st.session_state['portfolio'] = []

if 'pe_score' not in st.session_state:
    st.session_state['pe_score'] = {}

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = set()
   

# user input in sidebar
with st.sidebar:
    st.title('Portfolio Information 💼')
    st.write('')
    st.divider()
    ticker = st.selectbox('Select a Stock Ticker:', ('AAPL', 'MSFT', 'NVDA', 'GOOG', 'META', 'AMZN', 'NFLX', 'ORCL', 'IBM'))

   

    st.write('')
    amount = st.number_input("Amount to invest in the stock")

    if st.button('Add to Portfolio'):
        if ticker == '' or amount <= 0:
            st.error("Please fill in empty fields", icon = '❌')        # makes sure user fills in all fields

        if ticker not in st.session_state['user_input']:
            st.session_state['user_input'].add(ticker)

        for i in st.session_state['user_input']:
            t = yf.Ticker(i)
            d_yield = t.info['dividendYield']

            st.metric(label="Dividend Yield for " + i, value=d_yield)


        #st.write(st.session_state['user_input'])

        st.session_state['portfolio'].append({"ticker": ticker, "amount": amount})  # session state for portfolio percetn breakdown
        df1 = pd.DataFrame(st.session_state['portfolio'])
        fig1 = px.pie(df1, 
                      values='amount', 
                      names='ticker', 
                      title = 'Portfolio Percent Breakdown',
        )
        col1.plotly_chart(fig1)

        ratio = yf.Ticker(ticker)
        st.session_state['pe_score'][ticker] = {"pe score": ratio.info['forwardPE']}            # keeps track of the pe score of the stocks the user selects
        df2 = pd.DataFrame.from_dict(st.session_state['pe_score'], orient='index')

        df2.index.name = 'ticker'           
        df2 = df2.reset_index()             # makes sure the index is ticker for x axis
        fig2 = px.bar(df2,                  # pe score chart criteria
                      x='ticker', 
                      y="pe score", 
                      color="ticker", 
                      text_auto=True)

        with col1:
            st.plotly_chart(fig2)

     
