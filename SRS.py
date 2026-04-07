from datetime import datetime, timedelta
import random

# -----------------------------
# Models
# -----------------------------

class Plan:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class User:
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email


class Subscription:
    def __init__(self, user, plan):
        self.user = user
        self.plan = plan
        self.start_date = datetime.now()
        self.next_billing_date = self.start_date + timedelta(days=30)
        self.status = "Active"


class Invoice:
    def __init__(self, user, amount):
        self.user = user
        self.amount = amount
        self.due_date = datetime.now()
        self.status = "Pending"


class Payment:
    def __init__(self, invoice):
        self.invoice = invoice
        self.retry_count = 0
        self.status = "Pending"


# -----------------------------
# Services
# -----------------------------

class PaymentService:
    MAX_RETRIES = 3

    def process_payment(self, payment):
        while payment.retry_count < self.MAX_RETRIES:
            success = random.choice([True, False])

            if success:
                payment.status = "Success"
                payment.invoice.status = "Paid"
                print(f"✅ Payment successful for {payment.invoice.user.name}")
                return True
            else:
                payment.retry_count += 1
                print(f"❌ Payment failed (Retry {payment.retry_count})")

        payment.status = "Failed"
        payment.invoice.status = "Failed"
        print("⚠️ Max retries reached. Payment failed permanently.")
        return False


class BillingService:
    def __init__(self):
        self.payment_service = PaymentService()

    def generate_invoice(self, subscription):
        if subscription.status != "Active":
            print(f"⚠️ Subscription inactive for {subscription.user.name}")
            return None

        if subscription.plan.price == 0:
            print(f"ℹ️ Free plan - no billing for {subscription.user.name}")
            return None

        invoice = Invoice(subscription.user, subscription.plan.price)
        print(f"🧾 Invoice generated: ${invoice.amount} for {subscription.user.name}")

        payment = Payment(invoice)
        success = self.payment_service.process_payment(payment)

        if not success:
            subscription.status = "Overdue"
        else:
            subscription.next_billing_date += timedelta(days=30)

        return invoice


class SubscriptionService:
    def __init__(self):
        self.subscriptions = []

    def subscribe(self, user, plan):
        sub = Subscription(user, plan)
        self.subscriptions.append(sub)
        print(f"📌 {user.name} subscribed to {plan.name}")
        return sub

    def upgrade(self, subscription, new_plan):
        if subscription.status != "Active":
            print("⚠️ Cannot upgrade inactive subscription")
            return 0

        print(f"⬆️ Upgrading {subscription.user.name} to {new_plan.name}")

        remaining_days = (subscription.next_billing_date - datetime.now()).days
        total_days = 30

        prorated_amount = max(0, (remaining_days / total_days) * new_plan.price)
        print(f"💰 Prorated charge: ${round(prorated_amount, 2)}")

        subscription.plan = new_plan
        return prorated_amount

    def cancel(self, subscription):
        subscription.status = "Canceled"
        print(f"❌ Subscription canceled for {subscription.user.name}")


# -----------------------------
# Main Program (Menu Driven)
# -----------------------------

def main():
    # Plans
    free_plan = Plan("Free", 0)
    pro_plan = Plan("Pro", 10)
    enterprise_plan = Plan("Enterprise", 30)

    plans = {
        1: free_plan,
        2: pro_plan,
        3: enterprise_plan
    }

    # User
    user = User(1, "Bishwash", "bishwash@example.com")

    # Services
    sub_service = SubscriptionService()
    billing_service = BillingService()

    subscription = None

    while True:
        print("\n====== Subscription System ======")
        print("1. Subscribe")
        print("2. Generate Billing")
        print("3. Upgrade Plan")
        print("4. Cancel Subscription")
        print("5. View Subscription")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            print("\nChoose Plan:")
            print("1. Free ($0)")
            print("2. Pro ($10)")
            print("3. Enterprise ($30)")

            plan_choice = int(input("Enter plan: "))
            subscription = sub_service.subscribe(user, plans[plan_choice])

        elif choice == "2":
            if subscription:
                billing_service.generate_invoice(subscription)
            else:
                print("⚠️ No active subscription")

        elif choice == "3":
            if subscription:
                print("\nUpgrade To:")
                print("2. Pro ($10)")
                print("3. Enterprise ($30)")

                plan_choice = int(input("Enter plan: "))
                sub_service.upgrade(subscription, plans[plan_choice])
            else:
                print("⚠️ No active subscription")

        elif choice == "4":
            if subscription:
                sub_service.cancel(subscription)
            else:
                print("⚠️ No subscription to cancel")

        elif choice == "5":
            if subscription:
                print("\n--- Subscription Details ---")
                print(f"User: {subscription.user.name}")
                print(f"Plan: {subscription.plan.name}")
                print(f"Status: {subscription.status}")
                print(f"Next Billing: {subscription.next_billing_date}")
            else:
                print("⚠️ No subscription found")

        elif choice == "6":
            print("Exiting system...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()