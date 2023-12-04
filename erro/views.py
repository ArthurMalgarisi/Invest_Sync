from django.shortcuts import render

def pagina_erro_404(request, exception):
    return render(request, 'erro_404.html', status=404)

def pagina_erro_500(request):
    return render(request, 'erro_500.html', status=500)

def pagina_erro_403(request, exception):
    return render(request, 'erro_403.html', status=403)