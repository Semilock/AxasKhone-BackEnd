from django.shortcuts import render


# Create your views here
def profile_info(request):
    token = request.POST.get('token')
    user = token.user
    profile = user.profile
