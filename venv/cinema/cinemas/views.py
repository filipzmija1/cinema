from django.shortcuts import render
from django.views import View
from cinemas.models import ScreeningRoom, RoomReservation
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from datetime import datetime


def home_page(request):
    return render(request, 'base_template.html')


class AddRoom(View):
    """Class destined to adding screening rooms"""
    def get(self, request, *args, **kwargs):
        return render(request, 'add_room.html')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        try:
            places = int(request.POST.get('places'))
        except ValueError:
            return HttpResponse('Places must be number')
        projector_availability = request.POST.get('projector')
        data = ScreeningRoom.objects.all()
        room_names = []
        for room in data:
            room_names.append(f'{room.room_name}')
        if name and places and projector_availability:
            if name in room_names:
                return HttpResponse('Room with such name already exists')
            elif int(places) < 0:
                return HttpResponse('There cannot be less than 0 places')
            else:
                ScreeningRoom.objects.create(room_name=name, places=int(places), projector_availability=projector_availability)
                return HttpResponseRedirect('/home')
        else:
            return HttpResponse('You have to fill every field')


def show_rooms(request):
    data = ScreeningRoom.objects.all()
    current_date = datetime.now().date()
    reserve_data = RoomReservation.objects.get(date=current_date)
    for room in data:
        for date in room.roomreservation_set.all():
            hello = room.roomreservation_set.all()
            if current_date == date.date:
                available = 'available'
            else:
                available = 'not available'
    context = {
        'rooms': data,
        'current_date': current_date,
        'reservations': hello,
    }
    return render(request, 'show_rooms.html', context)


def delete_room(request, id_):
    room = ScreeningRoom.objects.get(id=id_)
    room.delete()
    return HttpResponseRedirect('/rooms')


class ModifyRoom(View):
    """Class destined to modify room"""
    def get(self, request, id_, *args, **kwargs):
        self.id_ = id_
        room = ScreeningRoom.objects.get(id=self.id_)
        context = {
            'room': room,
        }
        return render(request, 'modify_room.html', context)

    def post(self, request, *args, **kwargs):
        id_ = request.POST.get('id_')
        name = request.POST.get('name')
        try:
            places = int(request.POST.get('places'))
        except ValueError:
            return HttpResponse('Places must be number')
        projector_availability = request.POST.get('projector')
        data = ScreeningRoom.objects.all()
        room_names = []
        output_data = ScreeningRoom.objects.get(id=id_)
        for room in data:
            room_names.append(f'{room.room_name}')
        if name and places and projector_availability:
            room_names.remove(output_data.room_name)  # delete modifying room name
            if name in room_names:
                return HttpResponse('Room with such name already exists')
            elif int(places) < 0:
                return HttpResponse('There cannot be less than 0 places')
            else:
                output_data.room_name = name
                output_data.places = places
                output_data.projector_availability = projector_availability
                output_data.save()
                return HttpResponseRedirect('/rooms')
        else:
            return HttpResponse('You have to fill every field')


class RoomReserve(View):
    def get(self, request, id_, *args, **kwargs):
        data = ScreeningRoom.objects.get(id=id_)
        reserve_data = RoomReservation.objects.filter(room_id=id_)
        context = {
            'room': data,
            'reservations': reserve_data,
        }
        return render(request, 'reserve.html', context)

    def post(self, request, *args, **kwargs):
        date = request.POST.get('date')
        comment = request.POST.get('comment')
        room_id = request.POST.get('id_')
        room_object = ScreeningRoom.objects.get(id=room_id)
        current_date = str(datetime.now().date())
        if date >= current_date:
            if RoomReservation.objects.filter(Q(room_id=room_id) & Q(date=date)):   # statement to check if reservation on this day already exists
                return HttpResponse('The room is already reserved for this day')
            else:
                RoomReservation.objects.create(date=date, room_id=room_object, comment=comment)
                return HttpResponseRedirect('/rooms')
        else:
            return HttpResponse('You cannot reserve room on past days')


def room_details(request, id_):
    room_data = ScreeningRoom.objects.get(id=id_)
    reservation_data = RoomReservation.objects.filter(room_id=id_).order_by('-date')
    current_date = datetime.now().date()
    context = {
        'room': room_data,
        'reservations': reservation_data,
        'current_date': current_date,
    }
    return render(request, 'movie_detail.html', context)
