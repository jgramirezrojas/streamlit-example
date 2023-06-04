import streamlit as st  # dashboard app
import pandas as pd
import seaborn as sns  # for nice plots
import gdown  # for drive acces to files
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup, Comment  # format html text
from dateutil import parser
import numpy as np
import matplotlib.colors as mcolors



def get_contents_from_html(file_id):    
    url = f"https://drive.google.com/uc?id={file_id}"
    output = 'temp.html'
    gdown.download(url, output, quiet=False)
    
    with open(output, 'r') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')    

    # extracting the title which is the month 
    title_tag = soup.title
    print('title_tag', title_tag)
    # extracting the title which is the month 
    title_tag = soup.title
    
    # Find the comment <!-- Paragraph Five -->
    # this corresponds to the listing of growth and contraction sectors for the general ISM index
    comments = soup.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        if "Paragraph Five" in comment:
            paragraph_five = comment.next_sibling
            # Check if it's really a paragraph, not a newline or other type of node
            while not (isinstance(paragraph_five, type(soup.new_tag("p")))):
                paragraph_five = paragraph_five.next_sibling
            #print(paragraph_five)    

    # find Production
    h3_prod = soup.find(lambda tag: tag.name=="h3" and tag.text.strip() == "Production") # line 882
    print(h3_prod)
    p_prod = h3_prod.find_next_siblings('p')
    p_prod_texts = [p.text for p in p_prod]
    #print(p_prod_texts) 
    #   
    tables_prod = h3_prod.find_next_sibling('table') # Find the next div tag in the HTML
    table_html_prod = str(tables_prod) # Get the HTML of the table as a string    
    df_prod = pd.read_html(str(table_html_prod))[0]  # Convert the HTML table to a DataFrame
    #print(df_prod)

    # find Employment
    h3_empl = soup.find(lambda tag: tag.name=="h3" and tag.text.strip() == "Employment") # line
    p_empl = h3_empl.find_next_siblings('p')
    p_empl_texts = [p.text for p in p_empl]
    #print(p_empl_texts) 
    #   
    tables_empl = h3_empl.find_next_sibling('table') # Find the next div tag in the HTML
    table_html_empl = str(tables_empl) # Get the HTML of the table as a string    
    df_empl = pd.read_html(str(table_html_empl))[0]  # Convert the HTML table to a DataFrame
    #print(df_empl)

    # find Supplier Deliveries*
    h3_supd = soup.find(lambda tag: tag.name=="h3" and tag.text.strip() == "Supplier Deliveries*") # line
    p_supd = h3_supd.find_next_siblings('p')
    p_supd_texts = [p.text for p in p_supd]
    #print(p_supd_texts) 
    #   
    tables_supd = h3_supd.find_next_sibling('table') # Find the next div tag in the HTML
    table_html_supd = str(tables_supd) # Get the HTML of the table as a string    
    df_supd = pd.read_html(str(table_html_supd))[0]  # Convert the HTML table to a DataFrame
    #print(df_supd)

    # find Inventories
    h3_inve = soup.find(lambda tag: tag.name=="h3" and tag.text.strip() == "Inventories") # line
    p_inve = h3_inve.find_next_siblings('p')
    p_inve_texts = [p.text for p in p_inve]
    #print(p_inve_texts) 
    #   
    tables_inve = h3_inve.find_next_sibling('table') # Find the next div tag in the HTML
    table_html_inve = str(tables_inve) # Get the HTML of the table as a string    
    df_inve = pd.read_html(str(table_html_inve))[0]  # Convert the HTML table to a DataFrame
    #print(df_inve)
    
    # find Customers' Inventories*
    h3_cust = soup.find(lambda tag: tag.name=="h3" and tag.text.strip() == "Customers' Inventories*") # line
    p_cust = h3_inve.find_next_siblings('p')
    p_cust_texts = [p.text for p in p_cust]
    #print(p_cust_texts) 
    #   
    tables_cust = h3_cust.find_next_sibling('table') # Find the next div tag in the HTML
    table_html_cust = str(tables_cust) # Get the HTML of the table as a string    
    df_cust = pd.read_html(str(table_html_cust))[0]  # Convert the HTML table to a DataFrame
    #print(df_cust)    

    # find Prices*
    h3_pric = soup.find(lambda tag: tag.name=="h3" and tag.text.strip() == "Prices*") # line
    p_pric = h3_pric.find_next_siblings('p')
    p_pric_texts = [p.text for p in p_pric]
    #print(p_pric_texts) 
    #   
    tables_pric = h3_pric.find_next_sibling('table') # Find the next div tag in the HTML
    table_html_pric = str(tables_pric) # Get the HTML of the table as a string    
    df_pric = pd.read_html(str(table_html_pric))[0]  # Convert the HTML table to a DataFrame
    #print(df_pric) 
    
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
        "paragraph_five": paragraph_five,
        "p_prod": p_prod,
        "p_empl": p_empl,
        "p_supd": p_supd,
        "p_inve": p_inve,
        "p_cust": p_cust,
        "p_pric": p_pric,
        "df_drive": df_drive,
        "df_drive_12months": df_drive_12months,
        "paragraphs_NewOrd": paragraphs_NewOrd,
        "df_NewOrd": df_NewOrd,
        "df_prod": df_prod,
        "df_empl": df_empl,
        "df_supd": df_supd,
        "df_inve": df_inve,
        "df_cust": df_cust,
        "df_pric": df_pric                
    }

# Initialize empty lists for each dataframe
df_drives = []
df_drive_12months = []
df_NewOrds = []
df_prods = []
df_empls = []
df_supds = []
df_inves = []
df_custs = []
df_prics = []

# Iterate over each document
#for month, html_doc in html_docs.items():
#    with open(html_doc, 'r') as f:
#        html = f.read()
#        contents = get_contents_from_html(html)

file_ids = {
    "March": "133WrwMCjKeUK_xlyYKcWZ0U_LVsRAjSH",
    "April": "1XwzKx7tOzQJ26-H7wST8s-Q2MzbEpq80",
    "May": "18UVJnM7ykFtHXa-j3ycTo_kXTlpz_UZu",
}


import requests


for month, file_id in file_ids.items():
    contents = get_contents_from_html(file_id)
    
    

# Append each dataframe to the corresponding list
df_drives.append(contents['df_drive'])
df_drive_12months.append(contents['df_drive_12months'])
df_NewOrds.append(contents['df_NewOrd'])
df_prods.append(contents['df_prod'])
df_empls.append(contents['df_empl'])
df_supds.append(contents['df_supd'])
df_inves.append(contents['df_inve'])
df_custs.append(contents['df_cust'])
df_prics.append(contents['df_pric'])

# Concatenate each list of dataframes into one large dataframe

#df_NewOrd_final = pd.concat(df_NewOrds)

#df_prod_final = pd.concat(df_prods)
#df_prod_final_column_name = df_prod_final.columns[0]
#df_prod_final.drop_duplicates(subset=df_prod_final_column_name, inplace=True)
# Convert to datetime format
#df_prod_final[df_prod_final_column_name] = df_prod_final[df_prod_final_column_name].apply(lambda x: parser.parse(x))
# Sort the DataFrame based on the date column
#df_prod_final = df_prod_final.sort_values(by=[df_prod_final_column_name], ascending=False)
# Convert to month-year format
#df_prod_final[df_prod_final_column_name] = df_prod_final[df_prod_final_column_name].dt.strftime('%b %Y')
# Reset the DataFrame index
#df_prod_final.reset_index(drop=True, inplace=True)

df_drive_final = pd.concat(df_drives, ignore_index=True)
df_drive_12months_final = pd.concat(df_drive_12months,ignore_index=True)
df_NewOrd_final = pd.concat(df_NewOrds,ignore_index=True)
df_prod_final = pd.concat(df_prods,ignore_index=True)
df_empl_final = pd.concat(df_empls,ignore_index=True)
df_supd_final = pd.concat(df_supds,ignore_index=True)
df_inve_final = pd.concat(df_inves,ignore_index=True)
df_cust_final = pd.concat(df_custs,ignore_index=True)
df_pric_final = pd.concat(df_prics,ignore_index=True)

# If you want to drop duplicates based on a specific column, you can do so by specifying the subset parameter

#---------#-----------
def process_df(df):
    column_name = df.columns[0]
    df.drop_duplicates(subset=column_name, inplace=True)
    # Convert to datetime format
    df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    # Sort the DataFrame based on the date column
    df = df.sort_values(by=[column_name], ascending=False)
    # Reset the DataFrame index after sorting
    df.reset_index(drop=True, inplace=True)
    print(df)
    print("")
    return df

df_list = [df_drive_12months_final,
           df_NewOrd_final,
           df_prod_final,           
           df_empl_final, 
           df_supd_final, 
           df_inve_final, 
           df_cust_final, 
           df_pric_final
          ]

for df in df_list:
    df = process_df(df)


    # Save the dataframes in a dictionary
df_dict = {
    'New Orders': df_NewOrd_final,
    'Production': df_prod_final,
    'Employment': df_empl_final,
    'Supplier Deliveries': df_supd_final,
    'Inventories': df_inve_final,
    'Customers\' Inventories': df_cust_final,
    'Prices': df_pric_final
}


st.header("ISM Indexes")

# Ask the user to select the DataFrame
df_to_print = st.selectbox('Select a index table to display', list(df_dict.keys()))

# Get the corresponding DataFrame
df_to_display = df_dict[df_to_print]

# Display the DataFrame
st.dataframe(df_to_display)


# Ask the user to select the index
index_to_plot = st.selectbox('Select an ISM Index to plot', list(df_dict.keys()))

# Get the corresponding dataframe
df_to_plot = df_dict[index_to_plot]

# Display the dataframe
#st.dataframe(df_to_plot)

# Ask the user if they want to add a comparison index
add_comparison = st.checkbox('Do you want to add a comparison index?')

if add_comparison:
    # Ask the user to select the comparison index
    comparison_index = st.selectbox('Select a comparison index', [i for i in df_dict.keys() if i != index_to_plot])
    df_to_compare = df_dict[comparison_index]
    
    print(df_to_plot.columns[0])
    print(df_to_compare.columns[0])

    # Renaming first column of both dataframes to "Date"
    df_to_plot = df_to_plot.rename(columns={df_to_plot.columns[0]: 'Date'})
    df_to_compare = df_to_compare.rename(columns={df_to_compare.columns[0]: 'Date'})

    # Now, merge on 'Date'
    df_to_plot = df_to_plot.merge(df_to_compare, on='Date', how='outer', suffixes=('', '_compare'))


# Create the plot
fig, ax = plt.subplots()
sns.lineplot(data=df_to_plot, x=df_to_plot.columns[0], y=df_to_plot.columns[5], ax=ax)
if add_comparison:
    sns.lineplot(data=df_to_plot, x=df_to_plot.columns[0], y=df_to_plot.columns[-1], ax=ax)
plt.xticks(rotation=45)

# Display the plot
st.pyplot(fig)

### plotting the correlattions

# First, we rename the index column in each dataframe to "Date" and only keep the 'Date' and last column
for key in df_dict:
    df_dict[key] = df_dict[key].rename(columns={df_dict[key].columns[0]: 'Date', df_dict[key].columns[-1]: key})

# Then we merge all dataframes
from functools import reduce
dfs = [df[['Date', list(df.columns)[-1]]] for df in list(df_dict.values())]
df_all = reduce(lambda left,right: pd.merge(left,right,on='Date', how='outer'), dfs)

if st.checkbox('Do you want to display the correlation plot among ISM indexes?'):
    # Compute the correlation matrix
    corr = df_all.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    #cmap = sns.diverging_palette(230, 20, as_cmap=True)
    cmap = mcolors.LinearSegmentedColormap.from_list("n",['red','green'])


    # Draw the heatmap with the mask and correct aspect ratio
    #sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
    #            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)
    sns.heatmap(corr, annot=True, cmap=cmap)
    st.pyplot(f)



# Define the colormap

# Create the plot

