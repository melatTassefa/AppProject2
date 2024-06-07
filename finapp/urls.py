from django.urls import path, include
from .views import contact,aboutus,loginPage,registration,home,activate,quiz,quiz_view,quiz_results,studentpage
urlpatterns = [
    path('', home, name="home_url"),
    path('contact/', contact, name="contact_url"),
    path('aboutus/', aboutus, name="aboutus_url"),
    path('login/', loginPage, name="login_url"),
    path('registration/', registration, name="registration_url"),
#    path('search/', college_search, name="college_search_url"),
    path('activate/<uidb64>/<token>',activate,name='activate'),
    # path('quiz/',quiz, name="quiz_url"),
    # path('calculate/', calculate_career, name='calculate_career'),
    path('studentpage/',studentpage, name="studentpage_url"),
    path('quiz/<int:page>/', quiz_view, name='quiz'),
    path('results/', quiz_results, name='quiz_results'),
]