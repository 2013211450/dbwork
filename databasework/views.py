from django.shortcuts import render

# Create your views here.

def upload_file(request):
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            return HttpResponse('upload ok!')
    else:
        uf = UserForm()
    return render_to_response('register.html',{'uf':uf})

