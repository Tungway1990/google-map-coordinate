from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import re
import os
os.chdir(r'D:\Github\google-map-coordinate')

chrome_path=r'D:\Github\chromdriver\chromedriver.exe'
#your address file path
input_data=pd.read_excel(r'input.xlsx')
start_time = time.time()
raw=[]
driver = webdriver.Chrome(chrome_path)
driver.get(r'https://www.google.com.hk/maps')
for i in range(len(input_data)):
    if i ==0:
        tmp=''
    else:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tmp = soup.find("h1", jsan="7.section-hero-header-title-title,7.GLOBAL__gm2-headline-5").find(
                'span').get_text()
            
    search_input = driver.find_element_by_name("q")
    search_input.clear()
    search_input.send_keys(input_data.iloc[i, 0])
    search_btn = driver.find_element_by_id('searchbox-searchbutton')
    search_btn.click()
    while True:
        try:
            aa=BeautifulSoup(driver.page_source, 'html.parser').find("h1", jsan="7.section-hero-header-title-title,7.GLOBAL__gm2-headline-5").find('span').get_text()
            break
        except AttributeError:
            time.sleep(1)
            continue
    while tmp==aa:
        time.sleep(1)        
    else:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tmp1 = soup.find("h1", jsan="7.section-hero-header-title-title,7.GLOBAL__gm2-headline-5").find('span').get_text()
        coord= driver.current_url.split('!')[-2:]
        Latitude=re.findall(r'[a-z].+',coord[0])[0][1:]
        Longitude=re.findall(r'[a-z].+',coord[1])[0][1:]
        print(r'{} is {},{}'.format(input_data.iloc[i,0],Latitude,Longitude))
        raw.append([input_data.iloc[i,0],Latitude,Longitude])
driver.close()

data=pd.DataFrame(raw,columns=['addtess','Latitude','Longitude'])
data.to_excel('output.xlsx',index=False,encoding='utf-8')

#Plot points to map
import folium

m = folium.Map(location=[22.3158517, 114.174841],tiles="Stamen Toner", zoom_start=12)

'''
Downloaded Hong Kong polygon
from https://data.gov.hk/en-data/dataset/hk-had-json1-hong-kong-administrative-boundaries/resource/3c99bfe3-3164-4ef7-a710-5d94499eb4fc
'''
with open(r'D:\Github\google-map-coordinate\maps\Hong Kong ploygon.txt',encoding='utf-8') as f:
    polygon=json.load(f)
    
folium.GeoJson(polygon).add_to(m)

for i in range(len(data)):
    folium.CircleMarker([data.iloc[i,1], data.iloc[i,2]], 
                        radius=10, popup=data.iloc[i,0],
                        color='#3186cc',
                        fill_color='#3186cc', 
                        fill=True).add_to(m)
m.save('maps/Hong Kong map.html')
print('Program run time: {} seconds'.format(round(time.time()-start_time),2))

