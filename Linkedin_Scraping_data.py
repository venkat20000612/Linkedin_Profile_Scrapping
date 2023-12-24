import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

username=" "
passw=" "
profile_urls = ["https://www.linkedin.com/in/nagendra-annam-16683b266/",
                "https://www.linkedin.com/in/shashwat-hirapure-18042000/",
                "https://www.linkedin.com/in/bharath-k-807a61145/",
                "https://www.linkedin.com/in/kamalkalyan/",
                "https://www.linkedin.com/in/bandla-mahendra-358201235/"
                ]
driver = webdriver.Chrome()
driver.get("https://linkedin.com/login")
time.sleep(5)
user_name = driver.find_element(By.ID, "username")
user_name.send_keys(username)
password = driver.find_element(By.ID, "password")
password.send_keys(passw)
driver.find_element(By.XPATH, "//button[@type='submit']").click()

time.sleep(20)

def get_data(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    name = soup.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').text
    title = soup.find('div', class_='text-body-medium break-words').text
    location = soup.find('span', class_='text-body-small inline t-black--light break-words').text

    current_company_element = soup.find('button', class_='ySLwRThaaUSynscHmTvTsldyehHhrVrFAqug text-align-left')
    current_company = current_company_element.text if current_company_element else " "

    about_element = soup.find('div',class_='pv-shared-text-with-see-more full-width t-14 t-normal t-black display-flex align-items-center')
    about = about_element.text if about_element else " "

    driver.get(url + "details/education")
    edu_soup = BeautifulSoup(driver.page_source, 'html.parser')

    education = edu_soup.find_all('span', class_='t-14 t-normal')
    course_list = [edu.find('span', class_='visually-hidden').text.strip() for edu in education]

    college = edu_soup.find_all('div', class_='display-flex flex-wrap align-items-center full-height')
    college_list = [cl.find('span', class_='visually-hidden').text.strip() for cl in college]

    duration = edu_soup.find_all('span', class_='t-14 t-normal t-black--light')
    duration_list = [du.find('span', class_='visually-hidden').text.strip() for du in duration]

    driver.get(url + "details/skills")
    skill_soup = BeautifulSoup(driver.page_source, 'html.parser')

    skills = skill_soup.find_all('div', class_='display-flex flex-wrap align-items-center full-height')
    skills_list = [ski.find('span', class_='visually-hidden').text.strip() for ski in skills]

    name = name.strip()
    title = title.strip()
    location = location.strip()
    current_company = current_company.strip()
    about = about.strip()
    # print(name)
    # print(title)
    # print(location)
    # print(current_company)
    # print(about)

    combinedlist = "\n".join(f"{item1}\n{item2}\n{item3}" for item1, item2, item3 in zip(college_list, course_list, duration_list))
    skillstr="\n".join(skills_list)
    return [name, title, location, current_company, combinedlist, about, skillstr]

csv_file_path = "linkedin_data.csv"
csv_headers = ["Name", "Title", "Location", "Current Company", "Education", "About", "Skills"]

with open(csv_file_path, mode='w', encoding='utf-8', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_headers)

    for profile_url in profile_urls:
        profile_data = get_data(profile_url)
        csv_writer.writerow(profile_data)

driver.quit()

print(f"Data has been scraped and saved to {csv_file_path}.")
