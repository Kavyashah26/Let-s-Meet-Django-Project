from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.utils.crypto import get_random_string
import uuid
from .models import VideoCall,Participant


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'name': request.user.first_name})

@login_required
def videocall(request):
    room_id = request.GET.get('roomID')  # Check if roomID is passed in the URL
    if room_id:
        # If roomID is provided in the URL, use it directly without creating a new room or saving it to the database
        video_call = VideoCall.objects.filter(meeting_id=room_id).first()
        if not video_call:
            return redirect('/joinroom/')  # Redirect to join room page if roomID does not exist
    else:
        # If roomID is not provided in the URL, generate a new random room ID
        room_id = get_random_string(length=8)  # You can adjust the length as needed
        # Create a new VideoCall object with the generated room ID and the logged-in user
        video_call = VideoCall.objects.create(meeting_id=room_id, user=request.user)

    # Render the template with the user's name and the room ID
    return render(request, 'videocall.html', {'name': request.user.first_name + " " + request.user.last_name, 'id': room_id})
@login_required
def join_room(request):
    if request.method == 'POST':
        room_id = request.POST.get('roomID')
        # Check if the room ID exists in the VideoCall model
        video_call = VideoCall.objects.filter(meeting_id=room_id).first()
        if video_call:
            # Create a Participant instance for the user joining the room
            participant = Participant.objects.create(user=request.user, video_call=video_call)
            return redirect("/meeting?roomID=" + room_id)
        else:
            # Handle case when room ID does not exist
            return render(request, 'joinroom.html', {'error': 'Room ID does not exist. Please try again.'})
    return render(request, 'joinroom.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect("/login")

# def home(req):
#     # return HttpResponse("Hello world");
#     return render(req,'hello.html')
# def next(req):
#     return render(req,'next.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html', {'success': "Registration successful. Please login."})
        else:
            error_message = form.errors.as_text()
            return render(request, 'register.html', {'error': error_message})

    return render(request, 'register.html')


def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'login.html')
def index(request):
    return render(request, 'index.html')

def home(req):
    return render(req,'home.html')