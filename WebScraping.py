# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re

school_dictionary = {}
school_file = open("schools.txt")
for line in school_file:
    key, value = line.rstrip('\n').split(",")
    school_dictionary[key] = value

# print(school_dictionary)

options = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
options.add_argument('user-agent={0}'.format(user_agent))
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--incognito')
options.add_argument('--disable-web-security')
options.add_argument('--allow-running-insecure-content')

keylist = list(school_dictionary)
results_dict = []
for i in range(1,len(keylist)):
    name = keylist[i]
    link = "https://www.usnews.com" + school_dictionary[name]
    print(i, 'getting {0}: {1}'.format(name, link));
    driver = webdriver.Chrome("C:\\Users\\Admin\\PycharmProjects\\pythonProject1\\chromedriver", options=options)
    driver.get(link)
    time.sleep(5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    previous = " "

    file = open('300.txt', 'w')
    for p in soup.find_all('p'):
        print(p.text, file = file)
    file.close()
    for p in soup.find_all('p'):

        if ("School Type" in previous):
            schoolType = p.text
            print(schoolType)
        if ("Year Founded" in previous):
            yearFounded = p.text
            print(yearFounded)
        if ("Religious Affiliation" in previous):
            religiousAff = p.text
            print(religiousAff)
        if ("Academic Calendar" in previous):
            academicCal = p.text
            print(academicCal)
        if (previous == "Setting"):
            setting = p.text
            print(setting)
        if ("Endowment" in previous):
            endowment = p.text
            print(endowment)

        previous = p.text
        #rows.append(rank,schoolType,yearFounded,religiousAff,academicCal,setting,endowment)

        #print(previous)

    for a in soup.find_all('a', href=True):
        if ("Website" in a.text):
            website = a['href']

    #file.close()
    driver.quit()

    def getDescription(file):
        Dlist = []
        #filepath = "harvardtext.txt"
        with open(file) as fp:
            line = fp.readline()
            found = False
        # count = 0
            while line:
            # print("Line {}: {}".format(cnt, line.strip()))
                line = fp.readline()
                if "ranking in the 2021 edition of Best Colleges is National Universities" in line:
                # count += 1
                    found = True
                # continue

                # if "Beginning of dialog" in line:
                #   count +=1
                if "School Type" in line:
                    break
                if found == True:
                    Dlist.append(line)
        return (Dlist[0:min(len(Dlist),2)])
    descriptionlist = getDescription('300.txt')
    str1 = " "
    description = (str1.join(descriptionlist))
    regex = "#(\w+)"

    hashtag_list = re.findall(regex, description)
    intlist =[]
    for i in hashtag_list:
        if i.isdigit():
            intlist.append(i)

    rank = "-".join(str(y) for y in intlist)
    print(rank)
    elements = {
        'name': name,
        'ranking': rank,
        'description': description,
        'type': schoolType,
        'year': yearFounded,
        'religious': religiousAff,
        'calendar': academicCal,
        'setting': setting,
        'Endowment': endowment,
        'website': website
    }
    results_dict.append(elements)
df = pd.DataFrame(data = results_dict)
df.columns = ['Name', 'Ranking', 'Description', 'School Type', 'Year Founded', 'Religious Affliation',
                'Academic Calendar', 'Setting', '2019 Endowment', 'School Website']
df.to_csv("dataAll.csv", index=False)


#try:
   #target = driver.find_element_by_xpath('//button[normalize-space()="Load More"]')
   #print("the target is: ", target)
#except Exception as e:
    #print(e)
# print("hello")

#page_source = driver.page_source
#soup = BeautifulSoup(page_source, 'lxml')

#formatted_elems = []
#for i in range(0, 20):
    #temp_string = 'school-' + str(i)
    #results = soup.find('li', id=temp_string)

    # print (results.prettify())

    #result = results.find('h3')
    #slink = result.find('a')

   # data = {
     #   'name': result.text,
      #  'link': slink['href']
   # }
   # print(temp_string + ":", data)
   # formatted_elems.append(data)

# print(formatted_elems)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
