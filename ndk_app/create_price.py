import stripe
stripe.api_key = "sk_test_51OdIttLGG1oSeNJNXQ4l7i8j8515gvV9ak53VonxToBLNAtZkYB3igmP90JhsnDiqmNZgjLm1aFKq83XmFSzcSsb00PCgHY7N0"

starter_subscription = stripe.Product.create(
  name="Jus Bokoko",
  description="Pour avoir beaucoup d'énergie et rester actif",
)

starter_subscription_price = stripe.Price.create(
  unit_amount=25,
  currency="usd",
  recurring={"interval": "month"},
  product=starter_subscription['id'],
)

# Save these identifiers
print(f"Success! Here is your starter subscription product id: {starter_subscription.id}")
print(f"Success! Here is your starter subscription price id: {starter_subscription_price.id}")