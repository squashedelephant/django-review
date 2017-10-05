from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def main_page(request):
    return render(request, 'main_page.html', {'user': request.user})

@login_required
def user_page(request, user_id):
    return render(request, 'user_page.html', {'user': request.user})
