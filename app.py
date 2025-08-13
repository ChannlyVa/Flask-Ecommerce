from flask import Flask, redirect, render_template, request
import json
from tabulate import tabulate
from telegram import sendMessage
from products import datas
from mail import init_mail, send_order_email
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
init_mail(app)  # Initialize mail config and load env

@app.route('/')
@app.route('/home')
def home():
    success_param = request.args.get('success', False)
    return render_template("front/pages/home.html", products=datas, success=success_param)

@app.route('/products')
def product():
    return render_template('front/pages/product.html', products=datas)

@app.route('/cart')
def cart():
    return render_template('front/pages/cart.html')

@app.route('/checkout')
def checkOut():
    return render_template('front/pages/checkout.html')

@app.route('/vue')
def vue():
    return render_template('front/pages/vue.html')

@app.route('/order', methods=['POST'])
def order():
    form = request.form
    fullName = form.get('fullname')
    email = form.get('email')
    phone = form.get('phone')
    address = form.get('address')
    cart_item_json = form.get('cart_item')
    cart_items = json.loads(cart_item_json)

    item_list = []
    total = 0
    for index, item in enumerate(cart_items):
        item_list.append([
            index + 1,
            f"{item['title'][0:10]}...",
            item['price'],
            item['qty'],
        ])
        total += item['price'] * item['qty']

    telegram_message = (
        f"<strong>Customer Name: {fullName}</strong>\n"
        f"<strong>Customer Phone: {phone}</strong>\n"
        f"<strong>Customer Email: {email}</strong>\n"
        f"<strong>Customer Address: {address}</strong>\n"
        f"<strong>-----------------------------------</strong>\n"
        f"<pre>{tabulate(item_list, headers=['No', 'Title', 'Price', 'QTY'], numalign='left', stralign='left', floatfmt='.2f')}</pre>"
        f"<strong>-----------------------------------</strong>\n"
        f"<strong>Total : ${total:.2f}</strong>\n"
    )

    # 1️⃣ Send to Telegram
    chat_id = "@channly_channel"
    telegram_status = sendMessage(chat_id, telegram_message)
    if not telegram_status.get("ok", False):
        return "There was a problem sending the order to Telegram. Please try again."

    # 2️⃣ Send confirmation email
    try:
        send_order_email(email, fullName, phone, address, item_list, total)
    except Exception as e:
        return f"Order saved, but email sending failed: {e}"

    return redirect('/home?success=true')


if __name__ == '__main__':
    app.run(debug=True)
