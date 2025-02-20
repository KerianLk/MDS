from admin_panel.models import *

def add_sections(request):
    return {
        'sections': Section.objects.all(),
        'pages': Page.objects.all()
    }
