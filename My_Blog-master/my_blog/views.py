from django.shortcuts import render, render_to_response


def handler404(request, exception):
    return render(request, '404.html', status=404)

