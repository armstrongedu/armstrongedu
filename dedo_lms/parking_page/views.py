from django.shortcuts import render


def parking_page(request):
    return render(template_name='main.html', request=request)