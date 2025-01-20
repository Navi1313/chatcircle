from django.shortcuts import render , redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import Room , Topic , Messege , User 
from .forms import RoomForm , UserForm , CustomUserCreationForm
from django.contrib.auth.views import LoginView

# Create your views here.

# rooms = [
#     {'id' : 1 , 'name' : 'Lets Discuss the Philosopy'},
#     {'id' : 2 , 'name' : 'Lets have the Interview Talk '},
#     {'id' : 3 , 'name' : 'Lets play the Chess online'},
# ]

class MyLoginView(LoginView):
    def form_valid(self, form):
        # Log the user in
        login(self.request, form.get_user())
        # Add a welcome message
        messages.success(self.request, f"Welcome {form.cleaned_data['username']}!")
        return super().form_valid(form)


def loginPage(request):
    page = 'loginpage' 
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email= email)
        except :
            messages.error(request , 'User not found')

        user = authenticate(request , email= email , password= password)

        if user != None:
            login(request , user)
            return redirect('home')    
        else:
            messages.error(request , 'Invalid email or password')

    context = {'page' : page}
    return render(request , 'base/login_register.html', context)




# def registerUser(request):
#     form = UserCreationForm()
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             login(request , user)
#             return redirect('home')
#         else:
#             messages.error(request , 'Invalid form')
            
#     return render(request , 'base/login_register.html' ,{'form': form})


def registerUser(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid form')
            
    return render(request, 'base/login_register.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect('home')




def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
                                  Q(topic__name__icontains =q )
                                | Q(name__icontains = q)
                                | Q(description__icontains = q)
                                )
    topic = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messeges = Messege.objects.filter(Q(room__topic__name__icontains=q))[0:10]
    context = {
        'rooms' : rooms ,
        'topics': topic , 
        'room_count': room_count , 
        'room_messeges':room_messeges
        }
    return render(request, 'base/home.html' , context)



def room(request , pk):
    room = Room.objects.get(id = pk)
    room_messeges = room.messege_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Messege.objects.create(
            user= request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room' , pk=room.id)
    
    for msg in room_messeges:
        print("-----------------------------")
        print("Message user:", msg.user)
        print("Message created:", msg.created)
        print("Message body:", msg.body)
        print("-----------------------------")
    context = {'room' : room , 'room_messeges':room_messeges , 'participants': participants}   
    return render(request , 'base/room.html' , context)


def user_profile(request , pk):
    user = User.objects.get(id = pk) 
    room_messeges = user.messege_set.all()
    rooms = user.room_set.all()
    topic  = Topic.objects.all()
    context ={'user' : user , 'rooms' : rooms ,'room_messeges' :room_messeges , 'topic' : topic}
    return render(request , 'base/profile.html', context ) 


@login_required(login_url = 'login')
def create_room(request):
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')

    context = {'form' : form , 'topics': topics}
    return render(request , 'base/room_form.html' , context)



@login_required(login_url = 'login')
def update_room(request , pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host :
        return HttpResponse('You do not have permission to update this room')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('topic')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context = {'form' : form , 'topics': topics , 'room':room }

    return render(request , 'base/room_form.html' , context)



@login_required(login_url = 'login')
def delete_room(request , pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host :
        return HttpResponse('You do not have permission to update this room')
    if request.method == 'POST' :
        room.delete()
        return redirect('home')
    return render (request  , 'base/delete.html' , {'obj' : room})


@login_required(login_url = 'login')
def delete_messege(request , pk):
    messege = Messege.objects.get(id=pk)
    if request.user != messege.user :
        return HttpResponse('You are not allowed here')
    if request.method == 'POST' :
        messege.delete()
        return redirect('home')
    return render (request  , 'base/delete.html' , {'obj' : messege})

@login_required(login_url='login')
def update_user(request):
        user = request.user
        form = UserForm(instance=user)
        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES,instance=user)
            if form.is_valid():
                form.save()
                return redirect('user-profile' , pk=user.id)
        return render(request , 'base/update-user.html' , {'form' : form} )


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request , 'base/topics.html' ,{'topics' : topics} )

def activity_page(request):
    
    room_messeges = Messege.objects.all()
    
    return render(request , 'base/activity.html' , {'room_messeges':room_messeges } )