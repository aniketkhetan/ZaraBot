from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import schedule
import time
import os
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys


# Path to the chromedriver
  # Update this path

# Initialize the Chrome driver
driver = webdriver.Chrome()


def send_email(subject, body, to_email):
    from_email = 'zarasizechecker@gmail.com'
    from_password = 'muwb bqnn neyu elqn'
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add the email body
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        
        # Send the email
        server.send_message(msg)
        server.quit()
        
        st.write(f'Email sent to {to_email}')
    except Exception as e:
        print(f'Failed to send email: {e}')

def check_size_availability(driver, url, size):
    print(url)
    driver.get(url[0])
    
    try:
        # Construct XPath to locate the size button based on the size text
        size_button_path = 'size-selector-list__item-button'
        size_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, size_button_path))
        )
        for size_button in size_buttons:
            if size in size_button.text:
                m_size_button = size_button
        # Check if the button is disabled
        if m_size_button.get_attribute("data-qa-action") == "size-out-of-stock":
            return False
        else:
            return True

    except Exception as e:
        print(f"Exception: {e}")
        return False

def job():
    product_urls = [
        ['https://www.zara.com/in/en/stretch-knit-top-p05584169.html?v1=362609453&utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil','362609453'],
        ['https://www.zara.com/in/en/interlock-halter-dress-p03253362.html?v1=358935737&utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil','358935737'],
        ['https://www.zara.com/in/en/high-waist-trousers-p09929132.html?v1=378718807','378718807'],
        ['https://www.zara.com/share/-p02618321.html?v1=336468933&utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil','336468933'],
        ['https://www.zara.com/share/-p02298025.html?v1=353914855&utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil','353914855'],
        ['https://www.zara.com/share/-p02105454.html?v1=351799087&utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil','351799087'],
        ['https://www.zara.com/share/-p04676041.html?v1=322972465&utm_campaign=productShare&utm_medium=mobile_sharing_iOS&utm_source=red_social_movil','322972465'],
        ['https://www.zara.com/in/en/zw-collection-jacquard-dress-with-fringe-p02919196.html?v1=346601520&v2=2417457','346601520'],
        ['https://www.zara.com/in/en/embroidered-short-dress-p07521303.html?v1=363121036&v2=2417457','363121036'],

    ]
      # Update with actual size
    
    results = []
    
    email_recipient = 'anikhetan03@gmail.com'

    for url in product_urls:
        # size = f'{url[1]}-item-1'
        size ='M'
        in_stock = check_size_availability(driver, url, size)
        results.append({'url': url, 'size': size, 'in_stock': in_stock})
        print(f'Product URL: {url}, Size {size} in stock: {in_stock}')

        if in_stock:
            subject = 'Product in Stock'
            body = f'The following product is in stock in size {size}:\n{url[0]}'
            send_email(subject, body, email_recipient)

    # Save results to a CSV file
    df = pd.DataFrame(results)
    df.to_csv('zara_stock_report.csv', index=False)



def main():
    runner = True
    while runner:


        if st.button('End'):
            runner = False
            driver.quit()
            st.write('stopping check')
            time.sleep(10)
            sys.exit()
            
        
        else:

            st.write('Starting check')
            job()
            time.sleep(3600)

   

    # Close the driver after completing the checks
    driver.quit()

if __name__ == '__main__':
    main()