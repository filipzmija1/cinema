from django.shortcuts import render
from django.views import View
from cinemas.models import ScreeningRoom


template = 'base_template.html'


def home_page(request):
    new_format = template.format('')
    return render(request, new_format)


class AddRoom(View):
    """Adding screening rooms class"""
    def get(self, request, *args, **kwargs):
        return render(request, 'add_room.html')
