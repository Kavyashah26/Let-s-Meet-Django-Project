from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm,UserProfileForm
from django.utils.crypto import get_random_string
import uuid
from .models import VideoCall,Participant
from django.contrib import messages


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
    participant = Participant.objects.create(user=request.user, video_call=video_call)
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

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'register.html', {'form': form, 'error': error_message})
            else:
                form.save()
                return render(request, 'login.html', {'success': "Registration successful. Please login."})
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

    return render(request, 'login.html')


def home(req):
    return render(req,'home.html')


# from django.http import JsonResponse

# def delete_empty_videocalls(request):
#     print("caleed")
#     if request.method == 'POST':
#         try:
#             # Find and delete all VideoCall instances with user count 0
#             empty_videocalls = VideoCall.objects.annotate(num_users=models.Count('user')).filter(num_users=0)
#             empty_videocalls.delete()
#             return JsonResponse({'message': 'Empty VideoCall instances deleted successfully'}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)



def profile_updated(request):
    if request.session.get('profile_updated_from_update_profile', False):
        # Remove the session variable to prevent accessing this view directly
        del request.session['profile_updated_from_update_profile']
        return render(request, 'profile_updated.html')
    else:
        # If accessed directly without coming from update_profile, redirect to some other page
        # messages.error(request, "Access denied.")
        return redirect('login')  # Redirect to a different page

@login_required
def update_profile(request):
    user = request.user  # Get the current logged-in user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user.userprofile)
        if form.is_valid():
            form.save()
            # Update user's email, first_name, and last_name fields if provided in the form
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            # Set session variable to indicate that profile is updated from update_profile
            request.session['profile_updated_from_update_profile'] = True
            return redirect('profile_updated')
    else:
        # Populate the form with user's existing profile data
        form = UserProfileForm(instance=user.userprofile)
    return render(request, 'update_profile.html', {'form': form})