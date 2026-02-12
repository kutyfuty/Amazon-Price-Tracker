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
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
}


def send_email(current_price):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)

        subject = "Amazon Fiyat Dusuş Alarmi!"
        body = f"Müjde! Urun fiyati {current_price} PLN seviyesine dustu.\nLink: {URL}"

        # utf-8 encoding ile Türkçe karakter sorununu çözeriz
        msg = f"Subject: {subject}\n\n{body}".encode("utf-8")

        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=msg
        )
        print("Mail başarıyla gönderildi!")



response = requests.get(url=URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

try:

    price_span = soup.find("span", class_="a-price-whole")
    price_fraction = soup.find("span", class_="a-price-fraction")

    if price_span:

        price_text = price_span.getText()

        clean_price = price_text.replace(",", ".").replace("\xa0", "").replace(" ", "").replace(".", "")

        if price_fraction:
            final_price = float(clean_price + "." + price_fraction.getText())
        else:
            final_price = float(clean_price)

        print(f"Güncel Fiyat: {final_price} PLN")

        if final_price < TARGET_PRICE:
            send_email(final_price)
        else:
            print("Fiyat henüz istediğimiz seviyede değil.")

    else:
        print("Fiyat elementi bulunamadı. HTML yapısı değişmiş olabilir.")

except Exception as e:
    print(f"Bir hata oluştu: {e}")