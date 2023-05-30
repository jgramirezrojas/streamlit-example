import streamlit as st  # dashboard app
import pandas as pd
import seaborn as sns # for nice plots
import gdown # for drive acces to files
from bs4 import BeautifulSoup # format html text
import matplotlib.pyplot as plt

#-------reading file in drive--------
# Use the ID of the file (from the shareable link)
file_id = '1y0VK3L_GpvCNlBNq6JG33StJQVnYgllE'  # ID of the file in my google drive
url = f'https://drive.google.com/uc?id={file_id}'


output = 'output.html'  # name of the file to be downloaded
gdown.download(url, output, quiet=False)

#------- end reading file in drive------------


# --------reading output.html ----------------

# -------------reading ISM manufacturing --------------------

with open(output, "r") as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')

# find New Orders and Production Contracting ....
h3_0 = soup.find(lambda tag: tag.name=="h3" and "New Orders and Production Contracting" in tag.text)
# Find the next p tags (paragraphs) in the HTML after h3 new orders
paragraphs_0 = h3_0.find_next_siblings('p')

# Find the h3 tag containing the specified text
h3 = soup.find(lambda tag: tag.name=="h3" and "MANUFACTURING AT A GLANCE" in tag.text)
# Find the next table tag in the HTML
table = h3.find_next('table')
# Get the HTML of the table as a string
table_html = str(table)
# Convert the HTML table to a DataFrame
df_drive = pd.read_html(table_html)[0]

# Find the h3 tag containing the specified text
h3_1 = soup.find(lambda tag: tag.name=="h3" and "THE LAST 12 MONTHS" in tag.text)
# Find the next div tag in the HTML
div = h3_1.find_next('div')

# Find all table tags within the div
tables = div.find_all('table')
# Convert the HTML tables to DataFrames
df1 = pd.read_html(str(tables[0]))[0]
df2 = pd.read_html(str(tables[1]))[0]
# Concatenate the two DataFrames
df_drive_12months = pd.concat([df1, df2], ignore_index=True)

# -------------reading New orders --------------------
#h3_NewOrd = soup.find(lambda tag: tag.name=="h3" and "New Orders" in tag.text)
h3_NewOrd  = soup.find(lambda tag: tag.name=="h3" and tag.text.strip() == "New Orders")

# Find the first 'p' tag that immediately follows the 'h3' tag
first_paragraph = h3_NewOrd.find_next('p')
# Then find the remaining 'p' tags
paragraphs_NewOrd = h3_NewOrd.find_all_next('p')


# Find the next p tags (paragraphs) in the HTML after h3 new orders
#paragraphs_NewOrd = h3_NewOrd.find_next_siblings('p')


# Find the next table tag in the HTML
table_NewOrd = h3_NewOrd.find_next('table')

# Convert the HTML table to a DataFrame
df_NewOrd = pd.read_html(str(table_NewOrd))[0]


# --------end reading output.html ----------------


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

# Add a selectbox to the sidebar:
page = st.sidebar.selectbox(
    'Choose a Index',
    ['ISM Index', 'New Order Index']
)

################# PAGE 1 #####################
if page == 'ISM Index':
    st.header('ISM Index')
    st.title('ISM Manufacturing Index')
    # Text input for the ISM PMI Manufacturing Index
    default_text_0 = paragraphs_0[6].text if len(paragraphs_0) > 1 else ''
    text_input = st.text_area("Text extracted from the ISM PMI Manufacturing Index report:", value=default_text_0, height=200, max_chars=None, key=None)
    if st.button('Plot data for ISM PMI Manufacturing Index'):
        ranks = process_text(text_input)
        df = pd.DataFrame.from_dict(ranks, orient='index')
        df = df.reset_index().rename(columns={'index': 'Sector'})
        chart = plot_data(df)
        st.pyplot(chart.figure)
        st.dataframe(df)  
        #--------- for df from drive --------------
    st.subheader('MANUFACTURING AT A GLANCE')
    st.dataframe(df_drive)
    st.subheader('THE LAST 12 MONTHS')
    st.dataframe(df_drive_12months)
    ################# END PAGE 1 #####################
elif page == 'New Order Index':
    st.header('New Order Index')
    ################# PAGE 2 #####################
    # Text input for the New Orders Index
    default_text_1 = paragraphs_NewOrd[1].text if len(paragraphs_NewOrd) > 1 else ''
    text_input_new = st.text_area("Text extracted from the New Orders Index:", value=default_text_1, height=200, max_chars=None, key=None)
    if st.button('Plot data for New Orders Index'):
        ranks = process_text_new_orders(text_input_new)
        df_new_orders = pd.DataFrame.from_dict(ranks, orient='index')
        df_new_orders = df_new_orders.reset_index().rename(columns={'index': 'Sector'})
        chart_new_orders = plot_data(df_new_orders)
        st.pyplot(chart_new_orders.figure)
        st.dataframe(df_new_orders)


# Write out the text of each paragraph to the Streamlit app
#for i, paragraphs_NewOrd in enumerate(paragraphs_NewOrd, 1):
#    st.write(f"Paragraph {i}: {paragraphs_NewOrd.text}\n")

    
    
    
