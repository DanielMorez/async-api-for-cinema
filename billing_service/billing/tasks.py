from app.celery import app


@app.task
def auto_payment():
    # TODO: find subscriptions and create a payment
    print("working")
