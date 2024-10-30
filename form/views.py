from django.shortcuts import render, redirect
from .forms import ApplyModelForm
from magika import Magika
from .validator import FileUploadValidator
from django.core.exceptions import ValidationError

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # index.html adında bir şablona yönlendirir

def job_application_form(request):
    if request.method == 'POST':
        form = ApplyModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ApplyModelForm()

    return render(request, 'form.html', {'form': form})
