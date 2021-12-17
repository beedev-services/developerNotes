from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if 'user_id' not in request.session:
        notes = Note.objects.all().values()
        context = {
            'notes': notes,
            'stacks': Stack.objects.all().values(),
            'owner': User.objects.all().values(),
        }
        return render(request, 'index.html', context)
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

def logReg(request):
    if 'user_id' not in request.session:
        context = {
            "user": User.objects.all().values()
        }
        return render(request, 'logReg.html', context)
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
    return redirect(f'/user/{toUpdate.id}/viewProfile/')

def updateDiscord(request, user_id):
    toUpdate = User.objects.get(id=request.session['user_id'])
    toUpdate.profile.discord = request.POST['discord']
    toUpdate.save()
    return redirect(f'/user/{toUpdate.id}/viewProfile/')

def updateImage(request, user_id):
    toUpdate = User.objects.get(id=request.session['user_id'])
    toUpdate.profile.image = request.FILES['image']
    toUpdate.save()
    return redirect(f'/user/{toUpdate.id}/viewProfile/')

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
        note = Note.objects.get(id=note_id)
        users = User.objects.all().values()
        stacks = Stack.objects.all().values()
        context = {
            'note': note,
            'users': users,
            'stacks': stacks,
            'user': user,
        }
        return render(request, 'altViewNote.html', context)
    else:
        note = Note.objects.get(id=note_id)
        users = User.objects.all().values()
        stacks = Stack.objects.all().values()
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'note': note,
            'users': users,
            'stacks': stacks,
            'user': user,
        }
        return render(request, 'viewNote.html', context)

def likeNote(request, note_id):
    toUpdate = Note.objects.get(id=note_id)
    toUpdate.upvote +=1
    toUpdate.save()
    return redirect('/dashboard')

def editNote(request, note_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        note = Note.objects.get(id=note_id)
        users = User.objects.all().values()
        stacks = Stack.objects.all().values()
        context = {
            'note': note,
            'user': user,
            'users': users,
            'stacks': stacks,
        }
        return render(request, 'editNote.html', context)

def updateNote(request, note_id):
    toUpdate = Note.objects.get(id=note_id)
    toUpdate.subject = request.POST['subject']
    toUpdate.content = request.POST['content']
    toUpdate.code = request.POST['code']
    toUpdate.private = request.POST['private']
    toUpdate.resourceLink = request.POST['resourceLink']
    toUpdate.stack_id = request.POST['stack']
    toUpdate.save()
    return redirect(f"/note/{toUpdate.id}/view/")

def deleteNote(request, note_id):
    toDelete = Note.objects.get(id=note_id)
    toDelete.delete()
    return redirect('/dashboard/')

def uploadNote(request, note_id):
    toUpdate = Note.objects.get(id=note_id)
    toUpdate.upload.uploadName = request.POST['uploadName']
    toUpdate.upload.upload = request.FILES['upload']
    toUpdate.save()
    return redirect(f'/note/{toUpdate.id}/view')


def theAdmin(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please Log in")
        return redirect('/logReg/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        notes = Note.objects.all().values()
        comments = Comment.objects.all().count()
        users = User.objects.all().values()
        stacks = Stack.objects.all().values()
        if user.level == 9:
            context = {
                'user': user,
                'notes': notes,
                'comments': comments,
                'users': users,
                'stacks': stacks,
            }
            print(comments)
            return render(request, 'admin/adminDash.html', context)

def adminAllUsers(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in")
        return redirect('/')
    else:
        users = User.objects.all().values()
        user = User.objects.get(id=request.session['user_id'])
        if user.level == 9:
            context = {
                "users": users,
                'user': user,
            }
            return render (request, 'admin/allUsers.html', context)
        else:
            messages.error(request, "Access Denied to this page. Please see Admin")
            return redirect('/')

def adminAllPosts(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        notes = Note.objects.all().values()
        users = User.objects.all().values()
        stacks = Stack.objects.all().values()
        if user.level == 9:
            context = {
                'notes': notes,
                'user': user,
                'users': users,
                'stacks': stacks,
            }
            return render(request, 'admin/allNotes.html', context)
        else:
            messages.error(request, "Access Denied to this page. Please see Admin")
            return redirect('/')

def makeAdmin(request, user_id):
    toUpdate = User.objects.get(id=user_id)
    toUpdate.level=9
    toUpdate.save()
    return redirect('/theAdmin/allUsers/')

def adminEditNote(request, note_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        note = Note.objects.get(id=note_id)
        users = User.objects.all().values()
        stacks = Stack.objects.all().values()
        if user.level == 9:
            context = {
                'note': note,
                'user': user,
                'users': users,
                'stacks': stacks,
            }
            return render(request, 'admin/editNote.html', context)
        else:
            messages.error(request, "Access Denied to this page. Please see Admin")
            return redirect('/')    

def adminUpdateNote(request, note_id):
    toUpdate = Note.objects.get(id=note_id)
    toUpdate.subject = request.POST['subject']
    toUpdate.content = request.POST['content']
    toUpdate.code = request.POST['code']
    toUpdate.private = request.POST['private']
    toUpdate.resourceLink = request.POST['resourceLink']
    toUpdate.stack_id = request.POST['stack']
    toUpdate.save()
    return redirect(f"/theAdmin/note/{toUpdate.id}/edit")

def adminDeleteNote(request, note_id):
    toDelete = Note.objects.get(id=note_id)
    toDelete.delete()
    return redirect('/theAdmin/allPosts/')

def adminDeleteUser(request, user_id):
    toDelete = User.objects.get(id=user_id)
    toDelete.delete()
    return redirect('/theAdmin/allUsers/')

def adminAddComment(request, note_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        note = Note.objects.get(id=note_id)
        users = User.objects.all().values()
        stacks = Stack.objects.all().values()
        if user.level == 9:
            context = {
                'note': note,
                'user': user,
                'users': users,
                'stacks': stacks,
            }
            return render(request, 'admin/addComment.html', context)
        else:
            messages.error(request, "Access Denied to this page. Please see Admin")
            return redirect('/')   

def adminMakeComment(request, note_id):
    Comment.objects.create(
        comment=request.POST['comment'],
        commentCode=request.POST['commentCode'],
        resourceUrl=request.POST['resourceUrl'],
        commenter=User.objects.get(id=request.session['user_id']),
        note=Note.objects.get(id=note_id),
    )
    return redirect('/theAdmin/')

def adminViewComment(request, note_id):
    if 'user_id' not in request.session:
        messages.error(request, "Please log in")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        note = Note.objects.get(id=note_id)
        comments = Comment.objects.all().values()
        users = User.objects.all().values()
        stacks = Stack.objects.all().values()
        if user.level == 9:
            context = {
                'note': note,
                'user': user,
                'users': users,
                'stacks': stacks,
                'comments': comments,
            }
            return render(request, 'admin/viewComments.html', context)
        else:
            messages.error(request, "Access Denied to this page. Please see Admin")
            return redirect('/') 