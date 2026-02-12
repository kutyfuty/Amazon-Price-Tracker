# 📉 Amazon Price Tracker

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Scraping-green?style=for-the-badge)

An automated bot that monitors product prices on Amazon using Python. It sends an instant email notification when the price drops below a specified target.

## ⚙️ Features
* **Live Scraping:** Fetches real-time product data using `BeautifulSoup` and `Requests`.
* **Smart Parsing:** Handles currency formatting and HTML structure changes effectively.
* **Email Alerts:** Uses `smtplib` to send automated notifications via Gmail.
* **Environment Security:** Uses `.env` variables to keep credentials safe.

## 🚀 Setup & Usage

### 1. Clone the Repo
```bash
git clone [https://github.com/kutyfuty/Amazon-Price-Tracker.git](https://github.com/kutyfuty/Amazon-Price-Tracker.git)