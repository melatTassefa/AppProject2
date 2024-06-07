from django.shortcuts import render,redirect
import requests
from .models import AboutUs,Home,CustomUser, College_List
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.contrib.auth import get_user_model

from django.template.loader import render_to_string  # Import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.conf import settings
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.http import JsonResponse
import json
from django.urls import reverse

def contact(request):
    return render(request, 'contact.html')

def home(request):
   homeimg = Home.objects.all().first()
   data = {'home_data':homeimg}
   return render(request, 'home.html',data) 


def aboutus(request):
      about = AboutUs.objects.all().first()
      data = {'about_data':about}
      return render(request,'aboutus.html',data)


# def college_search(requests):
#     co_data = College_List.objects.all()
#     co_number = College_List.objects.all().count()
#     college_number = {'college_number', co_number}
#     college_data = {'college_data': co_data}
#     return render(requests, 'search2.html',college_data)


def loginPage(request):
       page='login'
       if request.method=='POST':
          
           username=request.POST.get('username').lower()
           password=request.POST.get('password')
           try:
               user=User.objects.get(username=username)
           except:
               messages.error(request,'User does not exist')

           user = authenticate(request,username=username,password=password)
           if user is not None:
               login(request,user)
               return redirect('home_url')
           else:
               messages.error(request,'Username or Password does not exist')
       context={'page':page}
       return render(request, 'login.html',context)



def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Thank you for your email confirmation")
        return redirect('login_url')
    else:
        messages.error(request,"Activation link invalid")
    return redirect('home_url')



def activateEmail(request,user, to_email):
    mail_subject="Activate your user account."
    message = render_to_string("template_activate_account.html",{
        'user':user.username,
        'domain': get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'

    })
    email=EmailMessage(mail_subject,message,to=[to_email])
    if email.send():
      messages.success(request,f'Dear {user} , please go to your email{to_email} inbox and click on\
                     recieved activation link to confirm and complete the registration. Note: Check your spam folder.' )
    else:
      messages.error(request, f'Problem sending email to {to_email},check if you types it correctly')



def registration(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.username = user.username.lower()
            user.role = form.cleaned_data['role']
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            
            # Determine the group based on the selected role
            if user.role == CustomUser.ADMIN:
                group_name = 'admin'
            elif user.role == CustomUser.HIGHER_EDUCATION:
                group_name = 'highereducation'
            else:  # Assume 'customer' if the role is not specified or unknown
                group_name = 'student'
            # form = CustomUserCreationForm(initial={'agent': CustomUser.AGENT})
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            activateEmail(request, user, form.cleaned_data.get('email'))
            login(request, user)
            return redirect('login_url')
            
        else:
            for error in list(form.errors.values()):
                messages.error(request, "An error occurred during registration")

    context = {'form': form}
    return render(request, 'registration.html', context)





def quiz(request):
    return render(request, 'quiz.html')


#####################RECOMMENDATION
class SurveyForm(forms.Form):
    CHOICES = [
        (1, 'Never'),
        (2, 'Rarely'),
        (3, 'Sometimes'),
        (4, 'Often'),
        (5, 'Always')
    ]

    reading_habits = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you read books or articles that challenge your views?")
    information_evaluation1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How thoroughly do you verify the credibility of information you encounter online?")
    information_evaluation2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you check the accuracy of news stories or social media posts before sharing?")
    problem_solving = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="When you face a complex problem, how often do you follow a detailed, step-by-step plan to solve it?")
    engagement_in_discussions = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How open are you to engaging in discussions or debates with people who have differing opinions?")
    questioning_curiosity1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you question the status quo or conventional wisdom?")
    questioning_curiosity2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How frequently do you ask questions or refer to other sources to understand new concepts or ideas?")
    creativity = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you come up with new ideas or try new ways of doing things in your daily life?")
    communication_clarity = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Do others easily understand you when you share your thoughts with classmates or teachers?")
    communication_participation = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you actively participate in class discussions or group activities?")
    communication_confidence = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How confidently do you share your opinions or ideas in class discussions or group projects?")
    market_trends_follow = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Do you follow news or articles about trends in technology, fashion, or other industries you're interested in?")
    market_research_analyze = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Do you research and analyze information about changes in your favorite industries (like technology, sports, or entertainment)?")
    market_predict_trends = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you try to predict what new trends or changes might happen in the future?")
    market_feedback = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you ask your friends or family for their opinions on new products or trends and use their feedback to make a decision (like buying something new or trying a new activity)?")
    market_planning = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Have you ever used information about trends to help plan school club projects, or events?")
    leadership_responsibility = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you take responsibility for leading group projects or activities?")
    leadership_decision_making = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How comfortable are you making decisions for your group or team?")
    leadership_communication = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Do you effectively communicate your ideas and plans to your team members?")
    leadership_conflict_resolution = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How well do you handle conflicts or disagreements within your group?")
    leadership_teamwork = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Do you work well with others to achieve common goals in group projects?")
    leadership_initiative = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you take the initiative to start new projects or activities in your school?")

# Function to suggest a career based on the answers
def suggest_career(answers):
    # Define the weight of each category
    weights = {
        'critical_thinking': 1.0,
        'communication': 0.8,
        'understanding_market': 0.7,
        'leadership': 0.6
    }

    # Critical Thinking Questions
    critical_thinking = sum([
        answers['reading_habits'],
        answers['information_evaluation1'],
        answers['information_evaluation2'],
        answers['problem_solving'],
        answers['engagement_in_discussions'],
        answers['questioning_curiosity1'],
        answers['questioning_curiosity2'],
        answers['creativity']
    ])

    # Communication Questions
    communication = sum([
        answers['communication_clarity'],
        answers['communication_participation'],
        answers['communication_confidence']
    ])

    # Understanding Social Politics and Market Needs Questions
    understanding_market = sum([
        answers['market_trends_follow'],
        answers['market_research_analyze'],
        answers['market_predict_trends'],
        answers['market_feedback'],
        answers['market_planning']
    ])

    # Leadership Questions
    leadership = sum([
        answers['leadership_responsibility'],
        answers['leadership_decision_making'],
        answers['leadership_communication'],
        answers['leadership_conflict_resolution'],
        answers['leadership_teamwork'],
        answers['leadership_initiative']
    ])

    # Calculate weighted scores
    computing_score = weights['critical_thinking'] * critical_thinking
    business_score = (weights['communication'] * communication +
                      weights['understanding_market'] * understanding_market +
                      weights['leadership'] * leadership)

    # Suggest a career based on the scores
    if computing_score >= business_score:
        return 'Computing'
    else:
        return 'Business'

# View to handle the survey form
# def survey_view(request):
#     if request.method == 'POST':
#         form = SurveyForm(request.POST)
#         if form.is_valid():
#             answers = {key: int(value) for key, value in form.cleaned_data.items()}
#             suggestion = suggest_career(answers)
#             return render(request, 'result.html', {'suggestion': suggestion})
#     else:
#         form = SurveyForm()
#     return render(request, 'survey.html', {'form': form})


######################QUIZ3 SOCIAL

# def calculate_career(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         answers = data.get('answers')
#         # Calculate based on the answers
#         law_score = calculate_law_score(answers)
#         economics_score = calculate_economics_score(answers)
#         # Decide the career path
#         if law_score > economics_score:
#             result = "Law"
#         elif economics_score > law_score:
#             result = "Economics"
#         else:
#             result = "Either Law or Economics"
#         return JsonResponse({'result': result})
#     else:
#         return HttpResponse("Method not allowed", status=405)

# quiz/views.py


##################################################
# Sample questions for demonstration purposes
questions = [
    {"id": 1, "text": "How confident are you in your ability to persuade others during discussions or debates?", "category": "Verbal Communication", "rank": 1},
    {"id": 2, "text": "Do you actively participate in class discussions or group conversations?", "category": "Verbal Communication", "rank": 2},
    {"id": 3, "text": "How well do you handle disagreements and maintain respectful communication during conflicts?", "category": "Verbal Communication", "rank": 3},
    {"id": 4, "text": "Do you consistently follow rules and guidelines even when no one is watching?", "category": "Ethical Judgement", "rank": 1},
    {"id": 5, "text": "How well do you handle sensitive or confidential information keeping it private and secure?", "category": "Ethical Judgement", "rank": 2},
    {"id": 6, "text": "Do you often stand up for what you believe is right even if it is unpopular or risky?", "category": "Ethical Judgement", "rank": 3},
    {"id": 7, "text": "Do you easily adapt to new or unexpected changes in your environment or schedule?", "category": "Resilience", "rank": 1},
    {"id": 8, "text": "How often do you seek help or support from friends, family, or teachers when you are struggling?", "category": "Resilience", "rank": 2},
    {"id": 9, "text": "How comfortable are you with solving mathematical problems and equations?", "category": "Quantitative Analysis", "rank": 1},
    {"id": 10, "text": "How well do you understand and interpret data presented in charts, graphs, and tables?", "category": "Quantitative Analysis", "rank": 2},
    {"id": 11, "text": "How effectively do you apply mathematical concepts to real-world problems?", "category": "Quantitative Analysis", "rank": 3},
    {"id": 12, "text": "How well do you understand complex theoretical concepts in your studies?", "category": "Theoretical Thinking", "rank": 1},
    {"id": 13, "text": "How effectively do you combine different ideas and theories to form a cohesive understanding of a subject?", "category": "Theoretical Thinking", "rank": 2},
    {"id": 14, "text": "How effectively do you gather information from reliable sources for your assignments?", "category": "Patience for Research", "rank": 1},
    {"id": 15, "text": "How well do you analyze and interpret the data you collected to draw meaningful conclusions?", "category": "Patience for Research", "rank": 2},
    {"id": 16, "text": "Do you often collaborate effectively with others (such as classmates or teachers) on doing assignments?", "category": "Patience for Research", "rank": 3},
    {"id": 17, "text": "How often do you critically evaluate the strengths and weaknesses of different arguments or theories?", "category": "Critical Evaluation", "rank": 1},
    {"id": 18, "text": "How proficient are you at writing clear and logical analyses of topics when doing assignments?", "category": "Critical Evaluation", "rank": 2},
    {"id": 19, "text": "How often do you question the assumptions underlying different viewpoints or arguments?", "category": "Critical Thinking", "rank": 1},
    {"id": 20, "text": "How frequently do you consider multiple perspectives before forming an opinion?", "category": "Critical Thinking", "rank": 2},
]

# Page size
questions_per_page = 5

def quiz_view(request, page=1):
    page = int(page)  # Ensure page is an integer
    if request.method == 'POST':
        # Retrieve the previous scores from the session
        scores = request.session.get('scores', {})

        # Update the scores based on the submitted answers
        for question in questions[(page-1)*questions_per_page : page*questions_per_page]:
            answer = int(request.POST.get(f"question{question['id']}"))
            category = question['category']
            scores[category] = scores.get(category, 0) + answer

        # Save the updated scores in the session
        request.session['scores'] = scores

        # If it's the last page, redirect to the result page
        if page == (len(questions) + questions_per_page - 1) // questions_per_page:
            return redirect('quiz_results')
        else:
            return redirect(reverse('quiz', kwargs={'page': page + 1}))

    # Fetch the current set of questions
    current_questions = questions[(page-1)*questions_per_page : page*questions_per_page]

    return render(request, 'quiz4.html', {'questions': current_questions, 'page': page})

def quiz_results(request):
    scores = request.session.get('scores', {})
    categories = ["Verbal Communication", "Ethical Judgement", "Resilience"]
    law_score = sum(scores.get(cat, 0) for cat in categories)
    economics_score = sum(scores.get(cat, 0) for cat in ["Quantitative Analysis", "Theoretical Thinking", "Patience for Research"])

    recommendation = "Economics"
    if law_score > economics_score:
        recommendation = "Law"

    return render(request, 'results.html', {'scores': scores, 'recommendation': recommendation})
#################################################################
#############################################



def studentpage(requests):
    co_data = College_List.objects.all()
    co_number = College_List.objects.all().count()
    college_number = {'college_number', co_number}
    college_data = {'college_data': co_data}
    return render(requests, 'studentpage.html',college_data)