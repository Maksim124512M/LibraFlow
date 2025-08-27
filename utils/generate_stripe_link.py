import stripe

from django.conf import settings


stripe.api_key = settings.STRIPE_API_KEY

def create_checkout_session(user, order):
    '''
    Create a Stripe checkout session for the given user and order.
    :param user:
    :param order:
    :return:
    '''

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Order #{order.id}'},
                    'unit_amount': int(order.total * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        customer_email=user.email,
        success_url=f'https://your.site/pay/success?session_id={{CHECKOUT_SESSION_ID}}',
        cancel_url='https://your.site/pay/cancel',
        metadata={'order_id': str(order.id), 'user_id': str(user.id)},
    )

    return session.url