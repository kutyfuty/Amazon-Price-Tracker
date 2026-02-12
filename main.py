import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv


load_dotenv()

URL = "https://www.amazon.pl/dp/B0FQF32239"
TARGET_PRICE = 930.0
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def send_email(current_price):
    """Sends an email notification when the price drops."""
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            
            subject = "Amazon Price Drop Alert!"
            body = f"Good news! The product price is now {current_price} PLN.\nCheck it here: {URL}"
            
            msg = f"Subject: {subject}\n\n{body}".encode("utf-8")
            
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=msg
            )
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

try:
    response = requests.get(url=URL, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    price_span = soup.find("span", class_="a-price-whole")
    price_fraction = soup.find("span", class_="a-price-fraction")

    if price_span:
        raw_price = price_span.getText()
        

        clean_price = raw_price.replace(",", ".").replace("\xa0", "").replace(" ", "").replace(".", "")
        

        if price_fraction:
            final_price = float(clean_price + "." + price_fraction.getText())
        else:
            final_price = float(clean_price)

        print(f"Current Price: {final_price} PLN")

        if final_price < TARGET_PRICE:
            send_email(final_price)
        else:
            print(f"Price ({final_price} PLN) is not below the target ({TARGET_PRICE} PLN) yet.")
            
    else:
        print("Error: Price element not found. Amazon might have changed the HTML structure or detected a bot.")

except Exception as e:
    print(f"An error occurred: {e}")