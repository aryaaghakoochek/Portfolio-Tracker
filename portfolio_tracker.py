import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly_express as px

s_price = []
s_change = []
s_shares = []
mystock = []
buy_price = []
t_shares_x_b_price = []

num = int(input("How many stocks are in your portfolio?"))

for x in range(num):
    ticker_input = input(str('enter your ticker?'))
    num_shares = int(input('Number of shares?'))
    buy_in_price = int(input('What was the buy in price per share?'))
    H = num_shares * buy_in_price
    mystock.append(ticker_input)
    s_shares.append(num_shares)
    buy_price.append(buy_in_price)
    t_shares_x_b_price.append(H)

def getPrice(symbole):
    headers = {'user-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15'}
    url = f'https://ca.finance.yahoo.com/quote/{symbole}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    stock_price = {
    soup.find('div', {'class':'D(ib) Va(m) Maw(65%) Ov(h)'}).find_all('span')[0].text,
    }
    return stock_price


def getChange(symbole):
    headers = {'user-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15'}
    url = f'https://ca.finance.yahoo.com/quote/{symbole}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    stock_change = {
    soup.find('div', {'class':'D(ib) Va(m) Maw(65%) Ov(h)'}).find_all('span')[1].text,
    }
    return stock_change

for i in mystock:
    s_price.append(getPrice(i))
    print('getting', i)

for i in mystock:
    s_change.append(getChange(i))
    print('getting', i)

#s_price[1] = s_price[0].str.strip('[')

print(s_price)
print(s_change)

df = pd.DataFrame({'TICKER': mystock,'CURRENT PRICE': s_price, 'CHANGE': s_change, '# OF SHARES': s_shares, 'BUY IN PRICE': buy_price, 'ORIGINAL AMOUNT SPENT': t_shares_x_b_price})

df.to_excel('portfoliotracker.xlsx', index=False, encoding='utf-8')

excel_file_path = 'portfoliotracker.xlsx'
df = pd.read_excel(excel_file_path)
print(df.head(2))

df['CURRENT PRICE'] = df['CURRENT PRICE'].str.replace("{", "")
df['CURRENT PRICE'] = df['CURRENT PRICE'].str.replace("}", "")
df['CURRENT PRICE'] = df['CURRENT PRICE'].str.replace("'", "")
df['CURRENT PRICE'] = df['CURRENT PRICE'].str.replace("'", "")

df['CURRENT TOTAL PORTFOLIO PRICE'] = df['CURRENT PRICE'] * df['# OF SHARES']
df['ORIGINAL TOTAL PORTFOLIO PRICE'] = df['# OF SHARES'] * df['BUY IN PRICE']
print(df)

df.to_excel("removed_charecters.xlsx")

chart = px.pie(df[['CURRENT TOTAL PORTFOLIO PRICE', 'TICKER']], values='CURRENT TOTAL PORTFOLIO PRICE', names='TICKER')
chart.show()


