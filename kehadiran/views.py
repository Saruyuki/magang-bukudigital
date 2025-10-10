from django.shortcuts import render
from .forms import PengurusForm

# Create your views here.
def pengurus_form(request):
    if request.method == 'POST':
        form = PengurusForm(request.POST)
        if form.is_valid():
            pengurus = form.save(commit=False)

            try:
                pengurus.save(commit=False)
                return render(request, "pengurus_success.html")
            except:
                form.add_error('nama', 'Terjadi keasalahan saat menyimpan data')
                
    else:
        form = PengurusForm()
    return render(request, 'pengurus_form.html', {'form': form})
