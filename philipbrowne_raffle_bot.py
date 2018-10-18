from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException  
import datetime
from selenium.webdriver.common.keys import Keys
import csv
import random
import string


def check_exists_by_css_selector(css_selector):
    try:
        browser.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True
	
def check_exists_by_link_text(link_text):
    try:
        browser.find_element_by_link_text(link_text)
    except NoSuchElementException:
        return False
    return True
	
def raffle_page_login(email, password):
	browser.get('https://www.philipbrownemenswear.co.uk/account/login?checkout_url=/products/yeezy-yeezy-boost-350-v2-white-cblack-red-aw-2017')
	browser.find_element_by_css_selector('#CustomerEmail').send_keys(email)
	browser.find_element_by_css_selector('#CustomerPassword').send_keys(password)	
	browser.find_element_by_css_selector('#customer_login > p:nth-child(8) > input').click()	
	
def size_selection_then_submit(uk_size):
	web_size = int((uk_size - 2.5)*2)
	if(check_exists_by_css_selector('#size')):
		browser.find_element_by_css_selector('#size > option:nth-child({})'.format(web_size)).click()	
# Need to activate the line below for the real submission
		#browser.find_element_by_css_selector('#raffleform > button').click()
	else: 
		print('Something went wrong. Please investigate into it.')
	


size_start = 3.5

size_end = 12

uk_size = [x*0.5 for x in range(int(2*size_start), int(2*size_end+1))]

counter = 0


# Read in the reference IP, which is the IP of my host computer
with open('proxy_list.txt') as fp:
    PROXY = fp.read().split("\n")

print(PROXY)

browser = webdriver.Chrome()
browser.get("https://www.ipchicken.com/")
reference_content = browser.find_element_by_css_selector('body > table:nth-child(2) > tbody > tr > td:nth-child(3) > p:nth-child(2) > font > b').text
reference_IP = reference_content.split("\n")[0]
browser.close()
browser.quit()



chrome_options = webdriver.ChromeOptions()

## It is best to read in a csv; we can edit the csv easily with excel
## Basically we can read in a version of csv, add password to it after done with registration, and save it as a new version
with open('US_address_info.csv', newline='') as csvfile:
	address_list = csv.reader(csvfile, delimiter=',', quotechar='|')
	for address in address_list:
	#for counter in range(1,10):	
		counter = counter+1

		chrome_options.add_argument('--proxy-server={}'.format(PROXY[counter]))

		browser = webdriver.Chrome(chrome_options=chrome_options)
		browser.get("https://www.ipchicken.com/")
		content = browser.find_element_by_css_selector('body > table:nth-child(2) > tbody > tr > td:nth-child(3) > p:nth-child(2) > font > b').text
		intelligent_IP = content.split("\n")[0]
		print (intelligent_IP)
		
		browser.close()
		browser.quit()
		
		# Deal with IPs. If it matches my own IP, then stop the program; if it matches the previous appeared IPs, break and stop the program as well. Otherwise, go ahead and move on
		
		if(intelligent_IP==reference_IP):
			print("Proxies are not working or something is wrong with the code. Please debug!")
			break
		else:
			with open('IP_in_use.txt', 'r+') as f:
				found = False
				for line in f:
					if intelligent_IP in line:
						found = True
						print('Duplicated IPs. Please investigate into it.')
						break
				if not found:
					# save the intelligent_IP into IP_in_use.text
					f.write(intelligent_IP)
		
					# First check whether this user name and password has been registered. If the answer is yes, check whether the shipping address is added. If yes, go ahead to submission; otherwise, register and add shipping address
					# Updated strategy: check whether the password for this entry is empty. If it is empty, register a new account; if it is not empty,  login and submit
				
					if(address[10]==''):
						browser.get('https://www.philipbrownemenswear.co.uk/account/register')
						browser.find_element_by_css_selector('#FirstName').send_keys(address[0])
						browser.find_element_by_css_selector('#LastName').send_keys(address[1])
						browser.find_element_by_css_selector('#Email').send_keys(address[9])
						random_password = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=8))
						print("{} - {}".format(address[9], random_password))
						with open("philipbrowne_accounts.txt", "a") as text_file:
							print("{} - {}".format(address[9], random_password), file=text_file)		
						browser.find_element_by_css_selector('#CreatePassword').send_keys(random_password)	
						browser.find_element_by_css_selector('#create_customer > p > input').click()
					

						browser.get('https://www.philipbrownemenswear.co.uk/account/login')
						browser.find_element_by_css_selector('#CustomerEmail').send_keys(address[9])
						browser.find_element_by_css_selector('#CustomerPassword').send_keys(random_password)	
						browser.find_element_by_css_selector('#customer_login > p:nth-child(8) > input').click()		
						browser.find_element_by_css_selector('#PageContainer > main > div > div > header > ul > li:nth-child(2) > a').click()
						browser.find_element_by_css_selector('#PageContainer > main > div > div > div > div > a').click()
						browser.find_element_by_css_selector('#AddressFirstNameNew').send_keys(address[0])
						browser.find_element_by_css_selector('#AddressLastNameNew').send_keys(address[1])
						browser.find_element_by_css_selector('#AddressAddress1New').send_keys(address[2])
						if(address[3]!=''):
							browser.find_element_by_css_selector('#AddressAddress2New').send_keys(address[3])
						browser.find_element_by_css_selector('#AddressCityNew').send_keys(address[4])
						if(address[7]=='US'):
							browser.find_element_by_css_selector('#AddressCountryNew > option:nth-child(2)').click()
							if(address[5]=='NY'):
								browser.find_element_by_css_selector('#AddressProvinceNew > option:nth-child(40)').click()
							elif(address[5]=='MD'):
								browser.find_element_by_css_selector('#AddressProvinceNew > option:nth-child(28)').click()
							elif(address[5]=='MA'):
								browser.find_element_by_css_selector('#AddressProvinceNew > option:nth-child(29)').click()	
						elif(address[7]=='China'):
							browser.find_element_by_css_selector('#AddressCountryNew > option:nth-child(49)').click()
						else:
							print('Fix the code')
							break
						browser.find_element_by_css_selector('#AddressZipNew').send_keys(address[6])
						browser.find_element_by_css_selector('#AddressPhoneNew').send_keys(address[8])
						browser.find_element_by_css_selector('#address_default_address_new').click()
						browser.find_element_by_css_selector('#address_form_new > p:nth-child(13) > input[type="submit"]').click()
						
						time.sleep(10)
						
						raffle_page_login(address[9],random_password)
						
						time.sleep(10)
						
						size_selection_then_submit(uk_size[counter])

					elif(address[10]=='Password'):
						pass
					else:
						raffle_page_login(address[9], address[10])
						time.sleep(10)
						size_selection_then_submit(uk_size[counter])		
						time.sleep(10)
					
					
					
					


# Quit the browser after done

browser.close()

