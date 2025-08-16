from django.views.generic import DetailView
from myapp.models import Playground


class FacilityDetailView(DetailView):
    model = Playground
    template_name = "myapp/facility_detail.html"
    context_object_name = (
        "playground"  # This makes the object available as 'playground' in the template
    )
