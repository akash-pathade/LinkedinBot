import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup

firstname='Vidhi'                        #Add your LastName
lastname='Lokhande'                         #Add your FirstName
keywords=['Java Spring Boot']                    #Add you list of role you want to apply
location = 'bangalore'                       #Add your location/city name for within India or remote
experience="2"






joblink=[]                          #Initialized list to store links
maxcount=50                         #Max daily apply quota for Naukri
applied =0                          #Count of jobs applied sucessfully
failed = 0                          #Count of Jobs failed
applied_list={
    'passed':[],
    'failed':[]
}                                   #Saved list of applied and failed job links for manual review
url=""
driver=None
try:
    profile = webdriver.FirefoxProfile("/Users/akash.pathade/Library/Application Support/Firefox/Profiles/bg2tdaad.testing") #Add your Root directory path
    driver = webdriver.Firefox(profile)
except Exception as e:
    print('Webdriver exception',e)
time.sleep(5)
for k in keywords:
    for i in range(2):
        if location=='':
            url = "https://www.naukri.com/"+k.lower().replace(' ','-')+"-"+str(i+1)+"?experience="+experience
        else: url = "https://www.naukri.com/"+k.lower().replace(' ','-')+"-jobs-in-"+location.lower().replace(' ','-')+"-"+str(i+1)+"?experience="+experience
        driver.get(url)
        print(url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source,'html5lib')
        results = soup.find(class_='list')
        job_elems = results.find_all('article',class_='jobTuple')
        print("FOUND JOB ELEMENS, ",job_elems)
        for job_elem in job_elems:
            joblink.append(job_elem.find('a',class_='title ellipsis').get('href'))
        print("ALL JOB LINKS : ", joblink)


for i in joblink:
    time.sleep(1)
    driver.get(i)   
    if applied <=maxcount:
        try:
            time.sleep(1)
            driver.find_element("xpath","//*[text()='Apply']").click()
            print("LINE 57")
            time.sleep(1)
            applied +=1
            applied_list['passed'].append(i)
            print('Applied for ',i, " Count", applied)

        except Exception as e: 
            failed+=1
            applied_list['failed'].append(i)
            print(e, "Failed " ,failed)
        try:    
            if driver.find_element("xpath","//*[text()='Your daily quota has been expired.']"):
                print('MAX Limit reached closing browser')
                driver.close()
                break
            if driver.find_element("xpath","//*[text()=' 1. First Name']"):
                driver.find_element("xpath","//input[@id='CUSTOM-FIRSTNAME']").send_keys(firstname)
            if driver.find_element("xpath","//*[text()=' 2. Last Name']"):
                driver.find_element("xpath","//input[@id='CUSTOM-LASTNAME']").send_keys(lastname);
            if driver.find_element("xpath","//*[text()='Submit and Apply']"):
                driver.find_element("xpath","//*[text()='Submit and Apply']").click()
        except:
            pass
            
    else:
        driver.close()
        break
print('Completed applying closing browser saving in applied jobs csv')
try:
    driver.close()
except:pass
csv_file = "naukriapplied.csv"
final_dict= dict ([(k, pd.Series(v)) for k,v in applied_list.items()])
df = pd.DataFrame.from_dict(final_dict)
df.to_csv(csv_file, index = False)
