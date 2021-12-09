# Load selenium components
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from pyvis.network import Network

c = webdriver.ChromeOptions()
c.add_argument("--incognito")
driver = webdriver.Chrome(ChromeDriverManager().install(),options=c)
driver.implicitly_wait(0.5)
url = "https://www.jotform.com/login/"
driver.get(url.format(q='Car'))
driver.maximize_window()

time.sleep(3)

usrName = 'archan****.com'
password = '******'
driver.find_element_by_name('email').send_keys(usrName)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_id('signinButton').click()

time.sleep(7)

driver.find_element_by_class_name('jfBasicModal-close').click()

time.sleep(6)
driver.find_element_by_class_name('lsApp-list-item-link').click()
time.sleep(6)

buttons = driver.find_elements_by_tag_name('button')
for b in buttons:
    val = b.get_attribute('aria-label')
    if val == "Download All":
        b.click()
        break

time.sleep(2)

dev = driver.find_element_by_class_name('jSheetDownload-links')
buttons = dev.find_elements_by_tag_name('button')
buttons[0].click()

time.sleep(15)
driver.quit()

fname = input("Enter the file name:")
abs_path = r"C:\Users\archanr\Downloads"

got_data = pd.read_csv(abs_path+fname)
got_data.columns = got_data.columns.str.replace(' ','_')
got_data.columns = got_data.columns.str.replace(':','')
got_data.columns= got_data.columns.str.lower()

columnNames = []
number_of_users = 0
UserName_to_index = {}
name_col_title = ""

for (columnName, columnData) in got_data.iteritems():
    if columnName == 'Date':
        continue
    columnNames.append(columnName)
    if columnName.find('name') != -1:
        name_col_title = columnName
        Users = list(set(columnData))
        Users.sort()
        number_of_users = len(Users)
        uindex = 0
        for user in Users:
            UserName_to_index[user] = uindex
            uindex += 1

#print(columnNames)
#print(UserName_to_index)

ValueBucket = dict()

#Building matrix
connection_matrix = []
for i in range(0,number_of_users):
    temp_array = []
    for j in range(0,number_of_users):
        temp_array.append(0)
    connection_matrix.append(temp_array)

for index, row in got_data.iterrows():
    for columnname1 in columnNames:
        if columnname1 == name_col_title:
            continue
        candidates_in_this_column_value = set()
        if row[columnname1] in ValueBucket:
            candidates_in_this_column_value = ValueBucket[row[columnname1]]
        candidates_in_this_column_value.add(row[name_col_title])
        ValueBucket[row[columnname1]] = candidates_in_this_column_value

#print(ValueBucket)

got_net = Network(height='100%', width='100%', bgcolor='#222222', font_color='white')
#got_net.force_atlas_2based()
got_net.barnes_hut()

for k,v in UserName_to_index.items():
    got_net.add_node(v, label=k, title=k)

for k,v in ValueBucket.items():
    for i in v:
        for j in v:
            if i != j:
                connection_matrix[UserName_to_index[i]][UserName_to_index[j]] += 1
                connection_matrix[UserName_to_index[j]][UserName_to_index[i]] += 1

for k,v in ValueBucket.items():
    for i in v:
        for j in v:
            if i != j:
                got_net.add_edge(UserName_to_index[i], UserName_to_index[j], value=connection_matrix[UserName_to_index[i]][UserName_to_index[j]]/2)
                got_net.add_edge(UserName_to_index[j], UserName_to_index[i], value=connection_matrix[UserName_to_index[j]][UserName_to_index[i]]/2)
got_net.show('nx.html')

#print(connection_matrix)
