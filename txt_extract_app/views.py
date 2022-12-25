from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid

from .models import Document
from .utils.process_file import handle_uploaded_file


# Create your views here.
@login_required(login_url='login')
def home(request):
    documents = Document.objects.filter(user=request.user)
    if q := request.GET.get('q'):
        documents = Document.objects.filter(user=request.user, fileName__icontains=q)
    return render(request, 'txt_extract_app/list.html', {'documents': documents})


@login_required(login_url='login')
def show_pdf(request, pk):
    try:
        document = Document.objects.get(user=request.user, id=pk)
    except:
        return render(request, '404.html')
    return render(request, 'txt_extract_app/show_pdf.html', {'document': document})


@login_required(login_url='login')
def upload_pdf(request):
    if request.method == 'POST':
        try:
            pdf = request.FILES['pdf']
        except:
            messages.error(request, 'No file selected')
            return render(request, 'txt_extract_app/upload_pdf.html')

        if not pdf.name.endswith('.pdf'):
            messages.error(request, 'File must be a pdf')
            return render(request, 'txt_extract_app/upload_pdf.html')

        pdf.name = f'{uuid.uuid4()}-{pdf.name}'
        text = handle_uploaded_file(pdf, pdf.name)
        
        document = Document(user=request.user, text=text, fileName=pdf.name, pdf=pdf)
        document.save()

        messages.success(request, 'File uploaded successfully')
    return render(request, 'txt_extract_app/upload_pdf.html')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('list_pdf')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_pdf')
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
                return redirect('list_pdf')
    return render(request, 'txt_extract_app/login_register.html', {'form': form})