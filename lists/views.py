from django.shortcuts import render, redirect
from lists.models import Item

# Create your views here.
def home_page(request):
    # TODO: Display multiple items in the table
    # TODO: Support more than one list
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/lists/theone/")
    items = Item.objects.all()
    return render(request, "home.html")


def view_list(request):
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})
