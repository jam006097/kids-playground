from django import forms
from myapp.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "rating"]
        labels = {
            "content": "口コミ内容",
            "rating": "評価 (5段階)",
        }
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "口コミ内容を200文字以内でご記入ください。",
                }
            ),
            "rating": forms.Select(
                attrs={"class": "form-select"},
                choices=[(i, str(i)) for i in range(1, 6)],
            ),
        }
