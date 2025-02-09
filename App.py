from flask import Flask, request
import google.generativeai as genai
import yfinance as yf
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Configure Gemini AI
genai.configure(api_key="AIzaSyAQYsPS9FsxnxBver82y8-hrTDcCnNsQn8")

def get_stock_price(symbol):
    """Fetch stock price from Yahoo Finance."""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        price = data['Close'].iloc[-1]
        return f"{symbol} current price: ₹{price:.2f}"
    except:
        return "Stock symbol not found."

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
    app.run(port=5000, debug=True)
