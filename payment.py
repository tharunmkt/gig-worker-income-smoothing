import razorpay
from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)

def create_payment_order(amount):

    order = client.order.create({
        "amount": int(float(amount) * 100),
        "currency": "INR"
    })

    return order
