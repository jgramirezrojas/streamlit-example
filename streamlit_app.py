import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# The sectors in the report
sectors = ['Apparel, Leather & Allied Products', 'Furniture & Related Products', 'Wood Products', 
           'Fabricated Metal Products', 'Machinery', 'Computer & Electronic Products', 'Transportation Equipment', 
           'Plastics & Rubber Products', 'Paper Products', 'Chemical Products', 'Petroleum & Coal Products', 
           'Primary Metals', 'Textile Mills', 'Electrical Equipment, Appliances & Components', 
           'Food, Beverage & Tobacco Products', 'Miscellaneous Manufacturing', 'Nonmetallic Mineral Products', 
           'Printing & Related Support Activities']

def process_text(text):
    growth_sectors = text.split("are:")[1].split("The")[0].split(';')
    contraction_sectors = text.split("contraction in")[1].split(", in the following order, are:")[1].split('.')
    contraction_sectors = contraction_sectors[0].split(';')

    growth_sectors = [s.strip() for s in growth_sectors]
    contraction_sectors = [s.strip() for s in contraction_sectors]

    # Remove 'and' from the last sector in both lists
    if growth_sectors[-1].startswith('and '):
        growth_sectors[-1] = growth_sectors[-1][4:]
    if contraction_sectors[-1].startswith('and '):
        contraction_sectors[-1] = contraction_sectors[-1][4:]

    # Remove trailing period from the last sector in both lists
    if growth_sectors[-1].endswith('.'):
        growth_sectors[-1] = growth_sectors[-1][:-1]
    if contraction_sectors[-1].endswith('.'):
        contraction_sectors[-1] = contraction_sectors[-1][:-1]

    ranks = {}
    # Search the sector name in the text and assign the rank
    for i, sector in enumerate(growth_sectors[::-1]):  # Reverse the list to give higher ranks to sectors mentioned first
        ranks[sector] = {'Rank': i + 1, 'Status': 'Growth'}

    for i, sector in enumerate(contraction_sectors[::-1]):  # Reverse the list
        ranks[sector] = {'Rank': i + 1, 'Status': 'Contraction'}

    for sector in sectors:
        if sector not in ranks:
            ranks[sector] = {'Rank': 0, 'Status': 'No Change'}

    return ranks

# The sectors in the New Orders Index
sectors_new_orders = ['Apparel, Leather & Allied Products', 'Wood Products', 'Furniture & Related Products', 
                      'Petroleum & Coal Products', 'Machinery', 'Computer & Electronic Products', 
                      'Fabricated Metal Products', 'Transportation Equipment', 'Plastics & Rubber Products', 
                      'Primary Metals', 'Chemical Products', 'Electrical Equipment, Appliances & Components', 
                      'Food, Beverage & Tobacco Products', 'Paper Products', 'Printing & Related Support Activities', 
                      'Miscellaneous Manufacturing', 'Textile Mills', 'Nonmetallic Mineral Products']

def process_text_new_orders(text):
    growth_sectors = text.split("are:")[1].split("Six")[0].split(';')
    contraction_sectors = text.split("decline in new orders in")[1].split(", in the following order:")[1].split('.')
    contraction_sectors = contraction_sectors[0].split(';')

    growth_sectors = [s.strip() for s in growth_sectors]
    contraction_sectors = [s.strip() for s in contraction_sectors]

    # Remove 'and' from the last sector in both lists
    if growth_sectors[-1].startswith('and '):
        growth_sectors[-1] = growth_sectors[-1][4:]
    if contraction_sectors[-1].startswith('and '):
        contraction_sectors[-1] = contraction_sectors[-1][4:]

    # Remove trailing period from the last sector in both lists
    if growth_sectors[-1].endswith('.'):
        growth_sectors[-1] = growth_sectors[-1][:-1]
    if contraction_sectors[-1].endswith('.'):
        contraction_sectors[-1] = contraction_sectors[-1][:-1]

    ranks = {}
    # Search the sector name in the text and assign the rank
    for i, sector in enumerate(growth_sectors[::-1]):  # Reverse the list to give higher ranks to sectors mentioned first
        ranks[sector] = {'Rank': i + 1, 'Status': 'Growth'}

    for i, sector in enumerate(contraction_sectors[::-1]):  # Reverse the list
        ranks[sector] = {'Rank': i + 1, 'Status': 'Contraction'}

    for sector in sectors_new_orders:
        if sector not in ranks:
            ranks[sector] = {'Rank': 0, 'Status': 'No Change'}

    return ranks



def plot_data(df):
    df['Color'] = df['Status'].apply(lambda x: 'green' if x == 'Growth' else ('red' if x == 'Contraction' else 'gray'))

    plt.figure(figsize=(8, 15))
    chart = sns.barplot(y='Sector', x='Rank', data=df, palette=df['Color'])
    return chart


    plt.figure(figsize=(15, 8))
    chart = sns.barplot(x='Sector', y='Rank', data=df, palette=df['Color'])
    chart.set_xticklabels(chart.get_xticklabels(), rotation=90)
    return chart

# Streamlit interface
st.title('ISM Manufacturing Index Dashboard')

# Text input for the ISM PMI Manufacturing Index
text_input = st.text_area("Enter text for the ISM PMI Manufacturing Index:", value='The five manufacturing industries that reported growth in April are: Printing & Related Support Activities; Apparel, Leather & Allied Products; Petroleum & Coal Products; Fabricated Metal Products; and Transportation Equipment. The 11 industries reporting contraction in April, in the following order, are: Furniture & Related Products; Wood Products; Nonmetallic Mineral Products; Electrical Equipment, Appliances & Components; Plastics & Rubber Products; Chemical Products; Machinery; Primary Metals; Computer & Electronic Products; Food, Beverage & Tobacco Products; and Miscellaneous Manufacturing.', height=200, max_chars=None, key=None)
if st.button('Process Text for ISM PMI Manufacturing Index'):
    ranks = process_text(text_input)
    df = pd.DataFrame.from_dict(ranks, orient='index')
    df = df.reset_index().rename(columns={'index': 'Sector'})
    chart = plot_data(df)
    st.pyplot(chart.figure)
    st.dataframe(df)

# Text input for the New Orders Index
text_input_new = st.text_area("Enter text for the New Orders Index:", value='The eight manufacturing industries that reported growth in new orders in April — in the following order — are: Printing & Related Support Activities; Paper Products; Fabricated Metal Products; Nonmetallic Mineral Products; Petroleum & Coal Products; Plastics & Rubber Products; Miscellaneous Manufacturing; and Transportation Equipment. Six industries reported a decline in new orders in April, in the following order: Furniture & Related Products; Electrical Equipment, Appliances & Components; Chemical Products; Computer & Electronic Products; Machinery; and Primary Metals.', height=200, max_chars=None, key=None)
if st.button('Process Text for New Orders Index'):
    ranks = process_text_new_orders(text_input_new)
    df_new_orders = pd.DataFrame.from_dict(ranks, orient='index')
    df_new_orders = df_new_orders.reset_index().rename(columns={'index': 'Sector'})
    chart_new_orders = plot_data(df_new_orders)
    st.pyplot(chart_new_orders.figure)
    st.dataframe(df_new_orders)
