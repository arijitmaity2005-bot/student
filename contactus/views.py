from django.shortcuts import render

# Create your views here.
def contact_view(request):
    return render(request, 'contact.html')