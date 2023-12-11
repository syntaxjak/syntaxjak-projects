import tkinter as tk
import urllib.request
import json
from tkinter import messagebox

# Set your alert thresholds here
PRICE_ALERT_THRESHOLD_HIGH = 0.05000000
PRICE_ALERT_THRESHOLD_LOW = 0.04500000

def get_bitcoin_price():
    # Using CoinGecko API to get the current Bitcoin price
    url = "https://api.coingecko.com/api/v3/simple/price?ids=grin&vs_currencies=usd"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    price = data['grin']['usd']
    return price

def update_price_label():
    price = get_bitcoin_price()
    price_label.config(text=f"Current Grin Price: ${price}")
    
    # Check for price threshold
    if price >= PRICE_ALERT_THRESHOLD_HIGH:
        messagebox.showinfo("Price Alert", f"Grin price is above ${PRICE_ALERT_THRESHOLD_HIGH}!")
    elif price <= PRICE_ALERT_THRESHOLD_LOW:
        messagebox.showwarning("Price Alert", f"Grin price is below ${PRICE_ALERT_THRESHOLD_LOW}!")
    
    # Schedule to update_price_label every minute
    root.after(60000, update_price_label)

# Create the main window
root = tk.Tk()
root.title("GRIN Price Ticker")

# Create a label to display the Bitcoin price
price_label = tk.Label(root, font=("Arial", 20), fg="green")
price_label.pack(pady=20)

# Update the label with the current price
update_price_label()

# Start the GUI event loop
root.mainloop()
