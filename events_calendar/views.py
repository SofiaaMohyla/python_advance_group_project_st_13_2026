from sched import Event

from django.shortcuts import render

# Create your views here.

def view_events_calendar(request):
    return render(request, 'events-calendar.html')

def all_events(request):
    events = Event.objects.all()
    return render(request, 'events-calendar.html', {'events': events})
    events_list = []

    for event in events:
        events_list.append({
            'title': event.title,
            'start_time': event.start_time.isoformat(),
            'end_time': event.end_time.isoformat(),
            'description': event.description,
            'location': event.location,
        })
    return JsonResponse(events_list, safe=False)