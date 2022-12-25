from django.shortcuts import render
import uuid

from .models import Document
from .utils.process_file import handle_uploaded_file

# Create your views here.
def home(request):
    documents = Document.objects.all()
    return render(request, 'txt_extract_app/list.html', {'documents': documents})

def show_pdf(request, pk):
    document = Document.objects.get(id=pk)
    return render(request, 'txt_extract_app/show_pdf.html', {'document': document})

def upload_pdf(request):
    if request.method == 'POST':
        request.FILES['pdf'].name = f'{uuid.uuid4()}-{request.FILES["pdf"].name}'
        text = handle_uploaded_file(request.FILES['pdf'], request.FILES['pdf'].name)
        print(text)
    return render(request, 'txt_extract_app/upload_pdf.html')

