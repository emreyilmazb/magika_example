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
            uploaded_file = request.FILES['cv']  # `cv` dosya alanı ismini doğrulayın.

            # Validator sınıfını kullanarak doğrulama
            validator = FileUploadValidator(allowed_extensions=['png', 'jpg', 'jpeg'], max_size=2 * 1024 * 1024)  # Örnek: PDF ve 2 MB sınırı
            try:
                validator(uploaded_file)
                form.save()
                return redirect('index')
            except ValidationError as e:
                form.add_error('cv', str(e))
        else:
            pass
    else:
        form = ApplyModelForm()

    return render(request, 'form.html', {'form': form})
