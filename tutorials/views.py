from django.shortcuts import render
from djangoapps.utils import get_this_template
from .models import Tutorial


# project page
def project_markdown(request):

    page_height = 1050
    f = open('tutorials/markdowns/README.md', 'r')
    if f.mode == 'r':
        readme = f.read()
        page_height = len(readme)/2 + 200

    tutorial_name = 'README'

    content = {
        'tutorial_name': tutorial_name,
        'readme': readme,
        'page_height': page_height
    }

    template_page = get_this_template('tutorials', 'project.html')

    return render(request, template_page, content)


# list tutorials
def list_tutorials(request):

    t = Tutorial.objects.all()

    context = {
        'tutorials': t
    }

    return render(request, 'pages/tutorials.html', context)


# tutorial pages
def tutorial_markdown(request):

    page_height = 1050
    f = open('tutorials/markdowns/README.md', 'r')
    if f.mode == 'r':
        readme = f.read()
        page_height = len(readme)/2 + 200

    tutorial_name = 'README'

    content = {
        'tutorial_name': tutorial_name,
        'readme': readme,
        'page_height': page_height
    }

    template_page = get_this_template('tutorials', 'project.html')

    return render(request, template_page, content)
