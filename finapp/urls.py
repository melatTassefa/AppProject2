from django.urls import path, include
from .views import contact,aboutus,loginPage,registration,home,activate,quiz,survey_view,studentpage,life_science_detail,physical_science_detail,initial_survey,college_detail
urlpatterns = [
    path('', home, name="home_url"),
    path('contact/', contact, name="contact_url"),
    path('aboutus/', aboutus, name="aboutus_url"),
    path('login/', loginPage, name="login_url"),
    path('registration/', registration, name="registration_url"),
    # path('search/', college_search, name="college_search_url"),
    path('activate/<uidb64>/<token>',activate,name='activate'),
    path('quiz/',quiz, name="quiz_url"),
    path('survey/', survey_view, name='survey'),
    path('studentpage/',studentpage, name="studentpage_url"),

    path('initial_survey/', initial_survey, name='initial_survey'),
    path('life_science_detail/',life_science_detail, name='life_science_detail'),
    path('physical_science_detail/',physical_science_detail, name='physical_science_detail'),

    path('college_detail/<int:post_id>/',college_detail, name="college_detail_url"),
]