from django.core.mail import send_mail
import os

def send_welcome_email(first_name, email):
    subject = "Welcome to CarHub!"
    sender_email = os.getenv("EMAIL_HOST_USER")  # Fetch from .env
    recipient_email = [email]

    message = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to CarHub</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f3f4f6; padding: 20px; text-align: center;">

    <div style="max-width: 600px; margin: auto; background: white; padding: 15px; border-radius: 10px; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        
        <!-- Logo -->
        <div style="font-size: 28px; font-weight: bold; margin-bottom: 20px;">
            <a href="" style="text-decoration: none;">
                <span style="background: linear-gradient(to right, #3b82f6, #2563eb); color: white; 
                            padding: 10px 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    Car<span style="color: #facc15;">Hub</span>
                </span>
            </a>
        </div>

        <!-- Welcome Message -->
        <h2 style="color: #1f2937; font-size: 24px; font-weight: bold; margin-bottom: 10px; text-transform: capitalize;">
            Welcome to CarHub, <span style="color: #3b82f6;">{first_name}</span>!
        </h2>

        <!-- Body Text -->
        <p style="color: #4b5563; font-size: 16px; margin-bottom: 20px;">
            Thank you for registering on our platform. We’re excited to have you on board! <br>
            Start exploring our cars and find the perfect ride for you.
        </p>

        <!-- Call-to-Action Button -->
        <a href="" 
            style="display: inline-block; background-color: #2563EB; color: white; padding: 12px 25px; 
            text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
            Log in to Your Account
        </a>

        <!-- Footer -->
        <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
            If you have any questions, feel free to contact us at 
            <a href="mailto:support@carhub.com" style="color: #3b82f6; text-decoration: none;">support@carhub.com</a>.
        </p>

        <p style="color: #6b7280; font-size: 14px; font-weight: bold;">Best Regards, <br> CarHub Team</p>
    </div>

</body>
</html>
"""

    try:
        send_mail(subject, "", sender_email, recipient_email, fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Email failed to send: {e}")


def send_payment_confirmation_email(first_name, email, car_name, amount):
    subject = "Your Payment has been Confirmed!"
    sender_email = os.getenv("EMAIL_HOST_USER")
    recipient_email = [email]

    # Format the amount with comma and dollar sign
    formatted_amount = "${:,.2f}".format(amount)

    message = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Payment Confirmation</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f9fafb; padding: 20px; text-align: center;">

    <div style="max-width: 600px; margin: auto; background: white; padding: 15px; border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        
        <!-- Logo -->
        <div style="font-size: 28px; font-weight: bold; margin-bottom: 20px;">
            <a href="" style="text-decoration: none;">
                <span style="background: linear-gradient(to right, #3b82f6, #2563eb); color: white; 
                            padding: 10px 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                    Car<span style="color: #facc15;">Hub</span>
                </span>
            </a>
        </div>

        <!-- Confirmation Message -->
        <h2 style="color: #1f2937; font-size: 22px; font-weight: bold; margin-bottom: 10px;">
            Hello {first_name.title()},
        </h2>

        <p style="color: #4b5563; font-size: 16px; margin-bottom: 20px;">
            Your payment of <strong>{formatted_amount}</strong> for the car <strong>{car_name}</strong> has been successfully confirmed!<br>
            Thank you for trusting CarHub.
        </p>

        <!-- Button -->
        <a href="#" 
        style="display: inline-block; background-color: #2563EB; color: white; padding: 12px 25px; 
        text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
        View Your Purchase
        </a>

        <!-- Footer -->
        <p style="color: #6b7280; font-size: 14px; margin-top: 30px;">
            Need help? Contact us at 
            <a href="mailto:support@carhub.com" style="color: #3b82f6; text-decoration: none;">support@carhub.com</a>
        </p>

        <p style="color: #6b7280; font-size: 14px; font-weight: bold;">
            Best Regards, <br> CarHub Team
        </p>
    </div>

</body>
</html>
"""

    try:
        send_mail(subject, "", sender_email, recipient_email, fail_silently=False, html_message=message)
    except Exception as e:
        print(f"Payment email failed to send: {e}")

