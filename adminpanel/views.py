from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Dish
from cart.models import MenuItem
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.views.decorators.http import require_POST
from urllib.request import urlopen
from django.core.files.base import ContentFile

# -------------------------
# ADMIN AUTHENTICATION
# -------------------------

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            return render(request, "adminpanel/login.html", {
                "error": "Invalid credentials or not an admin!"
            })

    return render(request, "adminpanel/login.html")


def admin_logout(request):
    logout(request)
    return redirect("admin_login")

# -------------------------
# PROTECTED ADMIN PAGES
# -------------------------

@login_required(login_url="admin_login")
def dashboard(request):
    return render(request, 'adminpanel/dashboard.html')


@login_required(login_url="admin_login")
def menu_list(request):
    dishes = MenuItem.objects.all()
    return render(request, 'adminpanel/menu_list.html', {"dishes": dishes})


@login_required(login_url="admin_login")
def add_dish(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        image_url = request.POST.get('image_url')

        item = MenuItem.objects.create(
            name=name,
            description=description,
            price=price,
            category=category
        )

        if image:
            item.image = image
            item.save()
        elif image_url:
            try:
                resp = urlopen(image_url)
                data = resp.read()
                filename = image_url.split('/')[-1].split('?')[0] or f"menu_{item.id}.jpg"
                item.image.save(filename, ContentFile(data))
            except Exception:
                pass

        return redirect('admin_menu')

    return render(request, 'adminpanel/add_dish.html')


@login_required(login_url="admin_login")
def edit_dish(request, id):
    dish = MenuItem.objects.get(id=id)
    if request.method == "POST":
        dish.name = request.POST.get('name')
        dish.description = request.POST.get('description')
        dish.price = request.POST.get('price')
        dish.category = request.POST.get('category')
        image = request.FILES.get('image')
        image_url = request.POST.get('image_url')
        if image:
            dish.image = image
        elif image_url:
            try:
                resp = urlopen(image_url)
                data = resp.read()
                filename = image_url.split('/')[-1].split('?')[0] or f"menu_{dish.id}.jpg"
                dish.image.save(filename, ContentFile(data))
            except Exception:
                pass
        dish.save()
        return redirect('admin_menu')

    return render(request, 'adminpanel/edit_dish.html', {"dish": dish})


# -------------------------
# EXTRA ADMIN PAGES
# -------------------------

@login_required(login_url="admin_login")
def orders(request):
    from cart.models import Order
    orders = Order.objects.all().order_by('-created_at')
    # provide status choices for template
    status_choices = Order.STATUS_CHOICES
    return render(request, "adminpanel/orders.html", {"orders": orders, 'status_choices': status_choices})


@login_required(login_url="admin_login")
@require_POST
def update_order_status(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "Permission denied")
        return redirect('admin_orders')
    from cart.models import Order
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    valid = [s[0] for s in Order.STATUS_CHOICES]
    if new_status in valid:
        order.status = new_status
        order.save()
        messages.success(request, f"Order {order.id} status updated to {new_status}")
    else:
        messages.error(request, "Invalid status")
    return redirect('admin_orders')


@login_required(login_url="admin_login")
def users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, "adminpanel/users.html", {"users": users})


@login_required(login_url="admin_login")
@require_POST
def assign_admin_assistant(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "Permission denied")
        return redirect('admin_users')
    user = get_object_or_404(User, id=user_id)
    group, _ = Group.objects.get_or_create(name='Admin Assistant')
    user.groups.add(group)
    user.is_staff = True
    user.save()
    messages.success(request, f"{user.username} is now Admin Assistant")
    return redirect('admin_users')


@login_required(login_url="admin_login")
@require_POST
def remove_admin_assistant(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "Permission denied")
        return redirect('admin_users')
    user = get_object_or_404(User, id=user_id)
    try:
        group = Group.objects.get(name='Admin Assistant')
        user.groups.remove(group)
    except Group.DoesNotExist:
        pass
    user.save()
    messages.success(request, f"Removed Admin Assistant role from {user.username}")
    return redirect('admin_users')


@login_required(login_url="admin_login")
@require_POST
def delete_dish(request, id):
    if not request.user.is_staff:
        # if AJAX request, return JSON error
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'permission_denied'}, status=403)
        messages.error(request, "Permission denied")
        return redirect('admin_menu')
    dish = get_object_or_404(MenuItem, id=id)
    dish.delete()
    # if AJAX request, return JSON for client-side handling
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'deleted', 'id': id})

    messages.success(request, "Dish deleted")
    return redirect('admin_menu')
