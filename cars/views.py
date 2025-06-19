from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from .utils import send_welcome_email
from .utils import send_payment_confirmation_email
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime
from .models import *
from .forms import *




def logout_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")  # Redirect logged-in users to home
        return view_func(request, *args, **kwargs)
    return wrapper


# Register view
@logout_required
def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect("register")

        # Create and save the user
        user = User.objects.create_user(
            username=email,  # Using email as the username
            email=email,
            password=password,
            first_name=first_name.title(),
            last_name=last_name,
        )
        user.save()


        try:
            send_welcome_email(first_name, email)  # Send welcome email
            messages.success(request, "Account created successfully! A welcome email has been sent.")
        except Exception:
            messages.warning(request, "Account created successfully, but the email could not be sent.")

        return redirect("login")

    return render(request, "car/register.html")


# Login view
@logout_required
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)  # Authenticate user

        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, "Login successful!")
            return redirect("home")  # Redirect to homepage
        else:
            messages.error(request, "Invalid email or password.")  # Show error message

    return render(request, "car/login.html")  # Render login page


# Logout view
@login_required(login_url='login')
def user_logout(request):
    logout(request)  # Log the user out
    messages.success(request, "Logged out successfully!")
    return redirect("home")  # Redirect to homepage


# Home view
def home(request):
    # Fetch the last 6 cars uploaded, marked as available
    featured_cars = (
        Car.objects.filter(is_available=True, quantity__gte=1)
        .select_related('brand')  # Optimize related model access
        .order_by('-created_at')[:6]
    )

    context = {
        'featured_cars': featured_cars,
        'total_cars': Car.objects.filter(is_available=True).count(),  # Total available cars
    }

    return render(request, 'car/home.html', context)


# Car list view
@login_required(login_url='login')
def car_list(request):
    cars = Car.objects.filter(is_available=True).order_by('-created_at')  # Order by latest

    # Filters
    brand = request.GET.get('brand')
    year = request.GET.get('year')
    condition = request.GET.get('condition')
    fuel_type = request.GET.get('fuel_type')
    transmission = request.GET.get('transmission')

    # Apply filters
    if brand:
        cars = cars.filter(brand__name__icontains=brand)
    if year:
        cars = cars.filter(year_of_manufacture=year)
    if condition:
        cars = cars.filter(condition=condition)
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    if transmission:
        cars = cars.filter(transmission=transmission)

    # Search
    search_query = request.GET.get('search')
    if search_query:
        cars = cars.filter(name__icontains=search_query)

    # Pagination
    paginator = Paginator(cars, 10)  # Show 10 cars per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'car/car_list.html', {'page_obj': page_obj, 'query': search_query})


# Car detail view
@login_required(login_url='login')
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car/car_detail.html', {'car': car})


# Add car view
@login_required(login_url='login')
def add_car(request):
    if request.method == "POST":
        name = request.POST.get("name")
        brand_name = request.POST.get("brand")
        price = request.POST.get("price")
        description = request.POST.get("description")
        year_of_manufacture = request.POST.get("year_of_manufacture")
        mileage = request.POST.get("mileage")
        condition = request.POST.get("condition")
        transmission = request.POST.get("transmission")
        fuel_type = request.POST.get("fuel_type")
        engine_capacity = request.POST.get("engine_capacity")
        color = request.POST.get("color")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("image")
        is_available = request.POST.get("is_available") == "on"

        brand = Brand.objects.get(id=brand_name)

        car = Car.objects.create(
            name=name,
            brand=brand,
            price=price,
            description=description,
            year_of_manufacture=year_of_manufacture,
            mileage=mileage,
            condition=condition,
            transmission=transmission,
            fuel_type=fuel_type,
            engine_capacity=engine_capacity,
            color=color,
            quantity=quantity,
            image=image,
            is_available=is_available
        )

        messages.success(request, "Car added successfully!")
        return redirect("home")  # Redirect to the form or another page

    brands = Brand.objects.all()
    return render(request, "car/add_car.html", {"brands": brands})


# Edit car view
@login_required(login_url='login')
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    all_brands = Brand.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")  
        brand_id = request.POST.get("brand")
        price = request.POST.get("price")
        description = request.POST.get("description")
        year_of_manufacture = request.POST.get("year_of_manufacture")
        mileage = request.POST.get("mileage")
        condition = request.POST.get("condition")
        transmission = request.POST.get("transmission")
        fuel_type = request.POST.get("fuel_type")
        engine_capacity = request.POST.get("engine_capacity")
        color = request.POST.get("color")
        quantity = request.POST.get("quantity")
        image = request.FILES.get("image")
        is_available = request.POST.get("is_available") == "on"

        brand = get_object_or_404(Brand, id=brand_id)

        car.name = name
        car.brand = brand
        car.price = price
        car.description = description
        car.year_of_manufacture = year_of_manufacture
        car.mileage = mileage
        car.condition = condition
        car.transmission = transmission
        car.fuel_type = fuel_type
        car.engine_capacity = engine_capacity
        car.color = color
        car.quantity = quantity
        
        if image:
            car.image = image  # Only update if a new image is uploaded
        
        car.is_available = is_available
        car.save()

        messages.success(request, "Car updated successfully!")
        return redirect("car_list")

    return render(request, "car/edit_car.html", {"car": car, "brands": all_brands})


# Delete car view
@login_required(login_url='login')
def delete_car(request, car_id):
    car = Car.objects.get(id=car_id)
    car.delete()
    messages.success(request, "Car deleted successfully!")
    return redirect("car_list")



# About us view
def about(request):
    return render(request, 'car/about.html')


# Contact us view
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "car/contact.html", {"form": form})


# Delete message view
@login_required(login_url='login')
def delete_message(request, message_id):
    message = get_object_or_404(Contact, id=message_id)
    message.delete()
    messages.success(request, "Message deleted successfully!")
    return redirect('admin_dashboard')


# Admin dashboard view
@login_required(login_url='login')
def admin_dashboard(request):
    total_cars = Car.objects.count()
    total_users = User.objects.filter(is_superuser=False).count()
    total_brands = Brand.objects.count()
    total_messages = Contact.objects.count()
    recent_messages = Contact.objects.order_by('-created_at')[:5]  # Show latest 5 messages

    pending_payments = Purchase.objects.filter(status='Pending').order_by('-date_purchased')
    count_pending_payments = pending_payments.count()

    completed_payments = Purchase.objects.filter(status='Completed').order_by('-date_purchased')

    # ========== NEW ADMIN ANALYTICS ==========
    today = timezone.now()
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    # Total cars sold this month
    cars_sold_this_month = Purchase.objects.filter(status='Completed', date_purchased__gte=start_of_month).aggregate(total_sold=Count('id'))['total_sold'] or 0

    # Total sales amount this year
    total_sales_this_year = Purchase.objects.filter(status='Completed', date_purchased__gte=start_of_year).aggregate(total_sales=Sum('price'))['total_sales'] or 0


    # Best selling brand
    best_brand = Purchase.objects.filter(status='Completed') \
                .values('car__brand__name') \
                .annotate(brand_count=Count('car__brand')) \
                .order_by('-brand_count') \
                .first()

    # Most purchased car
    best_car = Purchase.objects.filter(status='Completed') \
              .values('car__name') \
              .annotate(car_count=Count('car')) \
              .order_by('-car_count') \
              .first()

    # New users this month
    new_users_this_month = User.objects.filter(is_superuser=False, date_joined__gte=start_of_month).count()

    context = {
        'total_cars': total_cars,
        'total_brands': total_brands,
        'total_messages': total_messages,
        'total_users': total_users,
        'recent_messages': recent_messages,
        'completed_payments': completed_payments,
        'count_pending_payments': count_pending_payments,

        # New Admin Analytics
        'cars_sold_this_month': cars_sold_this_month,
        'total_sales_this_year': total_sales_this_year,
        'best_brand': best_brand,
        'best_car': best_car,
        'new_users_this_month': new_users_this_month,
    }
    return render(request, 'car/admin_dashboard.html', context)


# Car image upload view
@login_required(login_url='login')
def add_car_image(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        images = request.FILES.getlist("images")  # Get multiple uploaded images
        for image in images:
            CarImage.objects.create(car=car, image=image)

        return redirect('car_detail', car_id=car.id) 

    return render(request, 'car/add_car_image.html', {'car': car})


# Cart view
@login_required(login_url='login')
def add_to_cart(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the car is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, car=car)

    if not created:  # If the car is already in the cart, just increase the quantity
        cart_item.quantity += 1
    cart_item.price = car.price * cart_item.quantity  # Update price
    cart_item.save()

    # Recalculate total price
    cart.total_price = sum(item.price for item in cart.items.all())
    cart.save()

    messages.success(request, f"{car.name} has been added to your cart.")
    return redirect("car_list")


# View cart
@login_required(login_url='login')
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "car/cart.html", {"cart": cart})


# Remove item from cart
@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()

    # Recalculate total price
    cart = cart_item.cart
    cart.total_price = sum(item.price for item in cart.items.all())
    cart.save()

    messages.success(request, "Item has been removed from your cart.")
    return redirect("cart")


@login_required
def cart_items(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        cart_number = cart_items.count()
    except Cart.DoesNotExist:
        cart_number = 0

    return JsonResponse({'cart_number': cart_number})


# Checkout view
@login_required(login_url='login')
def checkout(request):
    total_amount = 0
    car_id = request.GET.get('car_id')  # Get from query params for initial GET request

    if request.method == 'POST':
        form = PurchaseForm(request.POST, request.FILES)
        if form.is_valid():
            transaction_id = form.cleaned_data['transaction_id']
            full_name = form.cleaned_data['full_name']
            proof = form.cleaned_data['proof_of_payment']

            car_id = request.POST.get('car_id')  # Get again from POST data

            if car_id:  
                car = get_object_or_404(Car, id=car_id)
                Purchase.objects.create(
                    user=request.user,
                    car=car,
                    full_name=full_name,
                    transaction_id=transaction_id,
                    proof_of_payment=proof,
                    price=car.price,
                    quantity=1
                )
                messages.success(request, "Purchase successful for 1 car.")
                return redirect('home')

            else:
                cart = get_object_or_404(Cart, user=request.user)
                items = CartItem.objects.filter(cart=cart)

                if not items.exists():
                    messages.warning(request, "Cart is empty.")
                    return redirect('cart')

                for item in items:
                    Purchase.objects.create(
                        user=request.user,
                        car=item.car,
                        full_name=full_name,
                        transaction_id=transaction_id,
                        proof_of_payment=proof,
                        price=item.car.price,
                        quantity=item.quantity
                    )

                items.delete()
                messages.success(request, "Purchase completed for all items in your cart.")
                return redirect('home')
    else:
        form = PurchaseForm()

        if car_id:
            # If coming from a single car page
            car = get_object_or_404(Car, id=car_id)
            total_amount = car.price
        else:
            # If coming from the cart page
            cart = get_object_or_404(Cart, user=request.user)
            items = CartItem.objects.filter(cart=cart)
            total_amount = sum(item.car.price * item.quantity for item in items)

    return render(request, 'car/checkout.html', {
        'form': form,
        'total_amount': total_amount,
        'car_id': car_id  # So template knows what kind of purchase this is
    })


# Pending payment list view (Admin only)
@login_required(login_url='login')
def pending_payment_list(request):
    pending_payments = Purchase.objects.filter(status='Pending').order_by('-date_purchased')
    return render(request, 'car/pending_payment.html', {'pending_payments': pending_payments})



# Confirm payment view (Admin only)
@require_POST
@login_required(login_url='login')
def confirm_payment(request, payment_id):
    if request.method == "POST":
        payment = get_object_or_404(Purchase, id=payment_id)
        payment.status = "Completed"
        payment.save()

        car = payment.car
        car.quantity -= 1  # Decrease car quantity by 1
        car.save()

        try:
            send_payment_confirmation_email(
                first_name=payment.user.first_name,
                email=payment.user.email,
                car_name=payment.car.name,
                amount=payment.price,
            )
            messages.success(request, f"Payment confirmed and email has been sent to customer.")
        except Exception as e:
            messages.warning(request, f"Payment confirmed, but failed to send confirmation email: {str(e)}")

        return redirect("pending_payments")


# All cars view (Admin only)
@login_required(login_url='login')
def all_cars(request):
    cars = Car.objects.all().order_by('-created_at')
    return render(request, 'car/all_cars.html', {'cars': cars})


# All brands view (Admin only)
@login_required(login_url='login')
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'car/brand_list.html', {'brands': brands})


# edit brand view (Admin only)
@login_required(login_url='login')
def edit_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('brand_list')  # Redirect to the brand list after saving
    else:
        form = BrandForm(instance=brand)
    
    return render(request, 'car/edit_brand.html', {'form': form, 'brand': brand})


# Delete brand view (Admin only)
@login_required(login_url='login')
def delete_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)

    if request.method == 'POST':
        brand.delete()
        messages.success(request, f'Brand "{brand.name}" has been successfully deleted.')
        return redirect('all_brands')

    return render(request, 'brands/delete_brand.html', {'brand': brand})


def make_admin(request):

    user  = get_object_or_404(User, username='sonmikeagudozie@gmail.com')

    if not user.is_superuser:
        user.is_superuser = True
        user.is_staff = True
        user.save()
        messages.success(request, "User has been made an admin successfully.")


    return redirect('home')


def add_multiple_brands(request):
    brand_names = [
        "Toyota", "Honda", "BMW", "Mercedes-Benz", "Ford",
        "Hyundai", "Kia", "Nissan", "Chevrolet", "Volkswagen"
    ]
    
    created_count = 0
    for name in brand_names:
        obj, created = Brand.objects.get_or_create(name=name)
        if created:
            created_count += 1

    return HttpResponse(f"{created_count} brands added successfully.")


