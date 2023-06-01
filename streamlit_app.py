import streamlit as st  # dashboard app
import pandas as pd
import seaborn as sns  # for nice plots
import gdown  # for drive acces to files
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup  # format html text

# Assume these are your loaded html documents for each month
html_docs = {
    "March": "march_2023.html",
    "April": "april_2023.html",
}

def get_contents_from_html(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    # extracting the title which is the month 
    title_tag = soup.title

    # find New Orders and Production Contracting ....
    h3_0 = soup.find(lambda tag: tag.name=="h3" and "New Orders and Production Contracting" in tag.text)
    # Find the next p tags (paragraphs) in the HTML after h3 new orders
    paragraphs_0 = h3_0.find_next_siblings('p')

    # find Production
    h3_prod = soup.find(lambda tag: tag.name=="h3" and tag.text.strip() == "Production") # line 882
    p_prod = h3_prod.find_next_siblings('p')
    p_prod_texts = [p.text for p in p_prod]
    print(p_prod_texts) 
    #   
    tables_prod = h3_prod.find_next_sibling('table') # Find the next div tag in the HTML
    table_html_prod = str(tables_prod) # Get the HTML of the table as a string    
    df_prod = pd.read_html(str(table_html_prod))[0]  # Convert the HTML table to a DataFrame
    print(df_prod)
    
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
    h3_NewOrd  = soup.find(lambda tag: tag.name=="h3" and tag.text.strip() == "New Orders")

    # Find the first 'p' tag that immediately follows the 'h3' tag
    first_paragraph = h3_NewOrd.find_next('p')
    # Then find the remaining 'p' tags
    paragraphs_NewOrd = h3_NewOrd.find_all_next('p')

    # Find the next table tag in the HTML
    table_NewOrd = h3_NewOrd.find_next('table')

    # Convert the HTML table to a DataFrame
    df_NewOrd = pd.read_html(str(table_NewOrd))[0]

    return {
        "title_tag": title_tag,
        "paragraphs_0": paragraphs_0,
        "p_prod": p_prod,
        "df_drive": df_drive,
        "df_drive_12months": df_drive_12months,
        "paragraphs_NewOrd": paragraphs_NewOrd,
        "df_NewOrd": df_NewOrd
    }


######### process text functtions #########

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

    for i, sector in enumerate(contraction_sectors):  # Do not reverse the list
        ranks[sector] = {'Rank': -(i + 1), 'Status': 'Contraction'}

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
    # Split the text to isolate growth and contraction sectors
    parts = text.split(", in the following order:")
    growth_part = parts[0].split("are:")[1] if "are:" in parts[0] else parts[0]
    contraction_part = parts[1] if len(parts) > 1 else ''

    # Extract growth sectors
    growth_sectors = growth_part.split(';')
    growth_sectors = [s.strip() for s in growth_sectors]

    # Extract contraction sectors
    contraction_sectors = contraction_part.split('.')[0].split(';') if contraction_part else []
    contraction_sectors = [s.strip() for s in contraction_sectors]

    # Remove any trailing sentence after the sector name in the last growth sector
    if len(growth_sectors) > 0:
        growth_sectors[-1] = growth_sectors[-1].split(".")[0]

    # Clean the sector lists
    growth_sectors = clean_sector_list_newOrders(growth_sectors)
    contraction_sectors = clean_sector_list_newOrders(contraction_sectors)

    ranks = {}
    # Assign ranks
    for i, sector in enumerate(growth_sectors):  # No need to reverse as we want to give higher ranks to sectors mentioned first
        ranks[sector] = {'Rank': i + 1, 'Status': 'Growth'}

    for i, sector in enumerate(contraction_sectors):  # No need to reverse
        ranks[sector] = {'Rank': - (i + 1), 'Status': 'Contraction'}

    # Assign rank 0 to sectors not mentioned in the text
    for sector in sectors_new_orders:
        if sector not in ranks:
            ranks[sector] = {'Rank': 0, 'Status': 'No Change'}

    return ranks


def clean_sector_list_newOrders(sectors):
    clean_sectors = []
    for s in sectors:
        if s.startswith('and '):
            s = s[4:]
        if s.endswith('.'):
            s = s[:-1]
        clean_sectors.append(s)
    return clean_sectors




##### end process text functions ##############


### production text function 

# The sectors in the Production Index
sectors_production = ['Apparel, Leather & Allied Products', 'Printing & Related Support Activities', 'Wood Products', 
                      'Furniture & Related Products', 'Fabricated Metal Products', 'Primary Metals', 
                      'Computer & Electronic Products', 'Plastics & Rubber Products', 'Petroleum & Coal Products', 
                      'Machinery', 'Transportation Equipment', 'Electrical Equipment, Appliances & Components', 
                      'Chemical Products', 'Textile Mills', 'Paper Products', 'Food, Beverage & Tobacco Products', 
                      'Miscellaneous Manufacturing', 'Nonmetallic Mineral Products']

def process_text_production(text):
    growth_sectors = text.split("in order:")[1].split(". The")[0].split(';')
    contraction_sectors_split = text.split("are:")
    if len(contraction_sectors_split) > 1:
        contraction_sectors = contraction_sectors_split[1].split('.')[0].split(';')
    else:
        contraction_sectors = []

    growth_sectors = [s.strip() for s in growth_sectors]
    contraction_sectors = [s.strip() for s in contraction_sectors]

    # Remove 'and' from the last sector in both lists
    if growth_sectors[-1].startswith('and '):
        growth_sectors[-1] = growth_sectors[-1][4:]
    if len(contraction_sectors) > 0 and contraction_sectors[-1].startswith('and '):
        contraction_sectors[-1] = contraction_sectors[-1][4:]

    ranks = {}
    # Search the sector name in the text and assign the rank
    for i, sector in enumerate(growth_sectors):
        ranks[sector] = {'Rank': i + 1, 'Status': 'Growth'}

    for i, sector in enumerate(contraction_sectors):
        ranks[sector] = {'Rank': -(i + 1), 'Status': 'Contraction'}

    for sector in sectors_production:
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


# Sidebar
st.sidebar.title("Menu")
month = st.sidebar.selectbox("Choose a Month", list(html_docs.keys()))
page = st.sidebar.selectbox(
    "Choose a Index",
    ["ISM Index", "New Orders Index", "Production","Heatmap"]
)


# Load the data from the chosen month's HTML document
with open(html_docs[month], 'r') as file:
    html_doc = file.read()
data = get_contents_from_html(html_doc)

    ################# PAGE 1 #####################
if page == "ISM Index":
    st.header("ISM Index")
    st.title(f'ISM Manufacturing Index {data["title_tag"].string}')
     # Text input for the ISM PMI Manufacturing Index
    default_text_0 = data["paragraphs_0"][6].text if len(data["paragraphs_0"]) > 1 else ""
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
        st.dataframe(data["df_drive"])
        st.subheader('THE LAST 12 MONTHS')
        st.dataframe(data["df_drive_12months"])
elif page == 'New Orders Index':
        st.header(f'New Order Index {data["title_tag"].string}')
        default_text_1 = data["paragraphs_NewOrd"][1].text if len(data["paragraphs_NewOrd"]) > 1 else ''
        text_input_new = st.text_area("Text extracted from the New Orders Index:", value=default_text_1, height=200, max_chars=None, key=None)
        if st.button('Plot data for New Orders Index'):
            ranks = process_text_new_orders(text_input_new)
            df_new_orders = pd.DataFrame.from_dict(ranks, orient='index')
            df_new_orders = df_new_orders.reset_index().rename(columns={'index': 'Sector'})
            chart_new_orders = plot_data(df_new_orders)
            st.pyplot(chart_new_orders.figure)
            st.dataframe(df_new_orders)            
elif page == 'Production':
        st.header(f'Production Index {data["title_tag"].string}')
        default_text_2 = data["p_prod"][1].text if len(data["p_prod"]) > 1 else ''
        text_input_new = st.text_area("Text extracted from the Production Index:", value=default_text_2, height=200, max_chars=None, key=None)
        if st.button('Plot data for Production Index'):
            ranks = process_text_production(text_input_new)
            df_production = pd.DataFrame.from_dict(ranks, orient='index')
            df_production = df_production.reset_index().rename(columns={'index': 'Sector'})
            chart_production = plot_data(df_production)
            st.pyplot(chart_production.figure)
            st.dataframe(df_production)  
elif page == 'Heatmap':
        st.header('HeatMap')
