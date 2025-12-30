from django import forms
from myapp.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "rating"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "rating": forms.Select(
                attrs={"class": "form-select"},
                choices=[(i, str(i)) for i in range(1, 6)],
            ),
        }
