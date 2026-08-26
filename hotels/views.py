import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import ContactMessage, MenuItem, Order



def home(request):
    specials = MenuItem.objects.filter(is_chef_special=True)[:3]
    return render(request, "home.html", {"specials": specials})


def about(request):
    return render(request, "about.html")


def menu(request):
    items = MenuItem.objects.all()
    category = request.GET.get("category")
    if category:
        items = items.filter(category=category)

    categories = MenuItem.CATEGORY_CHOICES
    return render(
        request,
        "menu.html",
        {"items": items, "categories": categories, "active_category": category},
    )


def food_detail(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    return render(request, "food_detail.html", {"item": item})


@require_POST
def place_order(request, pk):
    """Dummy order endpoint: records the order and confirms placement.
    Actual 'delivery' is simulated client-side with JS for this demo."""
    item = get_object_or_404(MenuItem, pk=pk)
    order = Order.objects.create(item=item)
    return JsonResponse(
        {
            "success": True,
            "order_id": order.pk,
            "item_name": item.name,
            "message": f"Your order for {item.name} has been placed!",
        }
    )


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message_text = request.POST.get("message", "").strip()

        if name and email and message_text:
            ContactMessage.objects.create(name=name, email=email, message=message_text)
            messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
            return redirect("contact")
        else:
            messages.error(request, "Please fill in all fields before sending.")

    return render(request, "contact.html")