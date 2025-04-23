import requests
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd


def date_time(table_cells):
    """
    Returns the date and time from the HTML table cell.
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """
    Returns the booster version from the HTML table cell.
    """
    out=''.join([booster_version for i,booster_version in enumerate(table_cells.strings) if i%2==0][0:-1])
    return out

def landing_status(table_cells):
    """
    Returns the landing status from the HTML table cell.
    """
    out=[i for i in table_cells.strings][0]
    return out

def get_mass(table_cells):
    """
    Returns the payload mass from the HTML table cell.
    """
    mass=unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass=mass[0:mass.find("kg")+2]
    else:
        new_mass=0
    return new_mass

def extract_column_from_header(row):
    """
    Extracts column name from the HTML table header.
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
    colunm_name = ' '.join(row.contents)
    if not(colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name


def task1_get_soup():
    static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
    response = requests.get(static_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
  
    print("Page Title:", soup.title.string)
    return soup


def task2_extract_columns(soup):
    html_tables = soup.find_all('table')
    first_launch_table = html_tables[2]  # Third table contains launch records
    
    column_names = []
    for th in first_launch_table.find_all('th'):
        name = extract_column_from_header(th)
        if name is not None and len(name) > 0:
            column_names.append(name)
    
    print("Extracted Column Names:", column_names)
    return column_names


def task3_create_dataframe(soup, column_names):
  
    launch_dict = dict.fromkeys(column_names)
    del launch_dict['Date and time ( )']
    launch_dict['Flight No.'] = []
    launch_dict['Launch site'] = []
    launch_dict['Payload'] = []
    launch_dict['Payload mass'] = []
    launch_dict['Orbit'] = []
    launch_dict['Customer'] = []
    launch_dict['Launch outcome'] = []
    launch_dict['Version Booster'] = []
    launch_dict['Booster landing'] = []
    launch_dict['Date'] = []
    launch_dict['Time'] = []

   
    extracted_row = 0
    for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
        for rows in table.find_all("tr"):
            if rows.th:
                if rows.th.string:
                    flight_number = rows.th.string.strip()
                    flag = flight_number.isdigit()
                else:
                    flag = False
            else:
                flag = False
            row = rows.find_all('td')
            if flag:
                extracted_row += 1
              
                launch_dict['Flight No.'].append(flight_number)
                
               
                datatimelist = date_time(row[0])
                date = datatimelist[0].strip(',')
                time = datatimelist[1]
                launch_dict['Date'].append(date)
                launch_dict['Time'].append(time)
                
            
                bv = booster_version(row[1])
                if not bv:
                    bv = row[1].a.string if row[1].a else 'N/A'
                launch_dict['Version Booster'].append(bv)
                
             
                launch_site = row[2].a.string if row[2].a else 'N/A'
                launch_dict['Launch site'].append(launch_site)
                
           
                payload = row[3].a.string if row[3].a else 'N/A'
                launch_dict['Payload'].append(payload)
                
               
                payload_mass = get_mass(row[4])
                launch_dict['Payload mass'].append(payload_mass)
                
              
                orbit = row[5].a.string if row[5].a else 'N/A'
                launch_dict['Orbit'].append(orbit)
                
               
                customer = row[6].a.string if row[6].a else 'N/A'
                launch_dict['Customer'].append(customer)
                
               
                launch_outcome = list(row[7].strings)[0]
                launch_dict['Launch outcome'].append(launch_outcome)
                
               
                booster_landing = landing_status(row[8])
                launch_dict['Booster landing'].append(booster_landing)
    
   
    df = pd.DataFrame({key: pd.Series(value) for key, value in launch_dict.items()})
    
 
    df.to_csv('spacex_web_scraped.csv', index=False)
    print("DataFrame created and exported to 'spacex_web_scraped.csv'")
    return df


if __name__ == "__main__":
    print("=== Starting TASK 1 ===")
    soup = task1_get_soup()
    
    print("\n=== Starting TASK 2 ===")
    column_names = task2_extract_columns(soup)
    
    print("\n=== Starting TASK 3 ===")
    df = task3_create_dataframe(soup, column_names)
    
    
    print("\nFirst 5 rows of the DataFrame:")
    print(df.head())