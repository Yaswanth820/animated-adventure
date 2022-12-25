from django.shortcuts import render
from django.http import HttpResponse

from .utils.process_file import handle_uploaded_file

# Create your views here.
def upload(request):
    if request.method == 'POST':
        file_name = request.FILES['pdf'].name
        text = handle_uploaded_file(request.FILES['pdf'], file_name)
        print(text)
    return render(request, 'txt_extract_app/upload_pdf.html')

