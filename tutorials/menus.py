from menu import Menu, MenuItem
from django.urls import reverse
from . import views


# add items to the menu
Menu.add_item("tutorials", MenuItem("My Portfolio", url="/", weight=10))
Menu.add_item("tutorials", MenuItem("Tutorials README", reverse(views.project_markdown), weight=10))
Menu.add_item("tutorials", MenuItem("My Tutorials", reverse(views.list_tutorials), weight=10))
