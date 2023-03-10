from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid

from .models import Document
from .utils.process_file import handle_uploaded_file


# Show all pdfs
@login_required(login_url='login')
def home(request):
    documents = Document.objects.filter(user=request.user)
    # Filter documents by search query
    if q := request.GET.get('q'):
        documents = Document.objects.filter(user=request.user, fileName__icontains=q)
    return render(request, 'txt_extract_app/list.html', {'documents': documents})


# Show specific pdf
@login_required(login_url='login')
def show_pdf(request, pk):
    try:
        # Get document by id and user
        document = Document.objects.get(user=request.user, id=pk)
    except:
        return render(request, '404.html')
    return render(request, 'txt_extract_app/show_pdf.html', {'document': document})


@login_required(login_url='login')
def upload_document(request):
    if request.method == 'POST':
        # Ensures that both pdf and cover image are uploaded
        try:
            pdf = request.FILES['pdf']
            cover = request.FILES['cover']
        except:
            messages.error(request, 'You have to upload both pdf and cover image')
            return render(request, 'txt_extract_app/upload.html')
        
        if not pdf.name.endswith('.pdf'):
            messages.error(request, 'PDF file ends with .pdf')
            return render(request, 'txt_extract_app/upload.html')

        if not (cover.name.endswith('.jpg') or cover.name.endswith('.jpeg') or cover.name.endswith('.png')):
            messages.error(request, 'Cover must be an image (jpg, jpeg, png)')
            return render(request, 'txt_extract_app/upload.html')

        # Rename files to avoid conflicts
        pdf.name = f'{uuid.uuid4()}-{pdf.name}'
        cover.name = f'{uuid.uuid4()}-{cover.name}'

        # Extract text from pdf
        text = handle_uploaded_file(pdf, pdf.name)
        
        document = Document(user=request.user, text=text, fileName=pdf.name, pdf=pdf, cover=cover)
        document.save()

        messages.success(request, 'File uploaded successfully')
    return render(request, 'txt_extract_app/upload.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    return render(request, 'txt_extract_app/login_register.html', {'login': True})


def logout_user(request):
    logout(request)
    return redirect('login')


def register_page(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user1 = User.objects.filter(username=user.username)
            if user1:
                messages.error(request, 'Username already exists')
            else:
                user.save()
                login(request, user)
                return redirect('home')
    return render(request, 'txt_extract_app/login_register.html', {'form': form})