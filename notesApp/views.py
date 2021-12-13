from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if 'user_id' not in request.session:
        context = {
            "user": User.objects.all().values()
        }
        return render(request, 'index.html', context)
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
        }
    return redirect('/dashboard/')

def logout(request):
    request.session.clear()
    messages.error(request, 'You have been logged out')
    return redirect('/')

def login(request):
    user = User.objects.filter(username = request.POST['username'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            return redirect('/dashboard/')
        messages.error(request, 'Invalid Credentials')
        return redirect('/login/')
    messages.error(request, 'That Username is not in our system, please register for an account')
    return redirect('/login/')

def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect('/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        email = request.POST['email'],
        username = request.POST['username'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    return redirect('/dashboard/')

def dashboard(request):
    if 'user_id' not in request.session:
        return render(request, 'index.html')
    else:
        user = User.objects.get(id=request.session['user_id'])
        notes = Note.objects.all().values()
        context = {
            'user': user,
            'notes': notes,
            'stacks': Stack.objects.all().values(),
            'owner': User.objects.all().values(),
        }
        print("Current User: ", user)
        print("Notes :", notes)
        return render(request, "dashboard.html", context)

def viewProfile(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
        }
        return render(request, 'viewProfile.html', context)

def updateUser(request, user_id):
    toUpdate = User.objects.get(id=request.session['user_id'])
    toUpdate.firstName = request.POST['firstName']
    toUpdate.lastName = request.POST['lastName']
    toUpdate.email = request.POST['email']
    toUpdate.username = request.POST['username']
    toUpdate.save()
    return redirect(f'/user/{user.id}/viewProfile/')

def updateDiscord(request, user_id):
    toUpdate = User.objects.get(id=request.session['user_id'])
    toUpdate.profile.discord = request.POST['discord']
    toUpdate.save()
    return redirect(f'/user/{user.id}/viewProfile/')

def updateImage(request, user_id):
    toUpdate = User.objects.get(id=request.session['user_id'])
    toUpdate.profile.image = request.FILES['image']
    toUpdate.save()
    return redirect(f'/user/{user.id}/viewProfile/')

def theAdmin(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in")
        return redirect('/')
    else:
        users = User.objects.all().values()
        user = User.objects.get(id=request.session['user_id'])
        if user.level == 9:
            context = {
                "users": users,
            }
            return render (request, 'admin/adminDash.html', context)
        else:
            messages.error(request, "Access Denied to this page. Please see Admin")
            return redirect('/')

def makeAdmin(request, user_id):
    toUpdate = User.objects.get(id=user_id)
    toUpdate.level=9
    toUpdate.save()
    return redirect('/theAdmin/allUsers/')

def addNote(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please log in')
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'stacks': Stack.objects.all(),
        }
        return render(request, 'addNote.html', context)

def createNote(request):
    Note.objects.create(
        subject=request.POST['subject'],
        content=request.POST['content'],
        code=request.POST['code'],
        private=request.POST['private'],
        resourceLink=request.POST['resourceLink'],
        stack_id=request.POST['stack'],
        author=User.objects.get(id=request.session['user_id']),
    )
    return redirect('/dashboard/')

def viewNote(request, note_id):
    if 'user_id' not in request.session:
        messages.error(request, "Access Denied.")
        return redirect('/')
    else:
        note = Note.objects.get(id=note_id)
        users = User.objects.all().values()
        stacks = Stack.objects.all().values()
        context = {
            'note': note,
            'users': users,
            'stacks': stacks,
        }
        print("the note: ", note)
        print("all stacks: ", stacks)
        print("all users: ", users)
        return render(request, 'viewNote.html', context)

def likeNote(request, note_id):
    toUpdate = Note.objects.get(id=note_id)
    toUpdate.upvote +=1
    toUpdate.save()
    return redirect('/dashboard')
