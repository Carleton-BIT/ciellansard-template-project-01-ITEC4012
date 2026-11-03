from django import forms

class FileUploadForm(forms.Form):
    upload_your_letterboxd_ratings = forms.FileField(
        help_text="Not sure where to find your ratings? On Letterboxd, go to Settings > Data > Export Your Data, unzip the folder it produces, and look for the 'ratings.csv' file."
    )
    star_threshold = forms.FloatField(
        min_value=0,
        max_value=5,
        initial=3.0,
        help_text="Base recommendations on movies with this many stars or more. Default is 3.0"
    )
    keyword_weight_modifier = forms.FloatField(
        min_value=0,
        initial=1.0,
        help_text="Raise this value to favour keywords from your highest-rated movies, lower it to give all keywords a fairer chance. Default = 1.0"
    )
    number_of_keywords_to_search = forms.IntegerField(
        min_value=3,
        max_value=20,
        initial=5,
        help_text="More keywords generates stronger and more varied recommendations, but has a large impact on loading time. Default = 5"
    )
    number_of_recommendations = forms.IntegerField(
        min_value=1,
        initial=10,
        help_text="Recommend this many movies (or fewer, if not enough are found.) Default = 10"
    )