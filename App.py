from flask import Flask, request
import google.generativeai as genai
import os
import yfinance as yf
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables!")

genai.configure(api_key=GEMINI_API_KEY)

def get_stock_price(symbol):
    """Fetch stock price from Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        price = data['Close'].iloc[-1]
        return f"{symbol} current price: ₹{price:.2f}"
    except:
        return "Stock symbol not found."

@app.route("/", methods=["GET"])
def home():
    return "WhatsApp Chatbot is Running!"

@app.route("/bot", methods=["POST"])
def bot():
    """Handle incoming WhatsApp messages."""
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Stock Price Query
    if incoming_msg.startswith("stock "):
        stock_symbol = incoming_msg.split(" ")[1].upper() + ".NS"  # Default to NSE
        reply = get_stock_price(stock_symbol)
    
    # Finance Advice using Gemini AI
    else:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(incoming_msg)
        reply = response.text

    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
