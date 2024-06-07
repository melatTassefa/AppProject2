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
from .forms import InitialSurveyForm, LifeScienceDetailForm, PhysicalScienceDetailForm

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
# class SurveyForm(forms.Form):
#     CHOICES = [
#         (1, 'Never'),
#         (2, 'Rarely'),
#         (3, 'Sometimes'),
#         (4, 'Often'),
#         (5, 'Always')
#     ]

#     reading_habits = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you read books or articles that challenge your views?")
#     information_evaluation1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How thoroughly do you verify the credibility of information you encounter online?")
#     information_evaluation2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you check the accuracy of news stories or social media posts before sharing?")
#     problem_solving = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="When you face a complex problem, how often do you follow a detailed, step-by-step plan to solve it?")
#     engagement_in_discussions = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How open are you to engaging in discussions or debates with people who have differing opinions?")
#     questioning_curiosity1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you question the status quo or conventional wisdom?")
#     questioning_curiosity2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How frequently do you ask questions or refer to other sources to understand new concepts or ideas?")
#     creativity = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you come up with new ideas or try new ways of doing things in your daily life?")
#     communication_clarity = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Do others easily understand you when you share your thoughts with classmates or teachers?")
#     communication_participation = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you actively participate in class discussions or group activities?")
#     communication_confidence = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How confidently do you share your opinions or ideas in class discussions or group projects?")
#     market_trends_follow = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Do you follow news or articles about trends in technology, fashion, or other industries you're interested in?")
#     market_research_analyze = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Do you research and analyze information about changes in your favorite industries (like technology, sports, or entertainment)?")
#     market_predict_trends = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you try to predict what new trends or changes might happen in the future?")
#     market_feedback = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you ask your friends or family for their opinions on new products or trends and use their feedback to make a decision (like buying something new or trying a new activity)?")
#     market_planning = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Have you ever used information about trends to help plan school club projects, or events?")
#     leadership_responsibility = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you take responsibility for leading group projects or activities?")
#     leadership_decision_making = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How comfortable are you making decisions for your group or team?")
#     leadership_communication = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Do you effectively communicate your ideas and plans to your team members?")
#     leadership_conflict_resolution = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How well do you handle conflicts or disagreements within your group?")
#     leadership_teamwork = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Do you work well with others to achieve common goals in group projects?")
#     leadership_initiative = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="How often do you take the initiative to start new projects or activities in your school?")

# # Function to suggest a career based on the answers
# def suggest_career(answers):
#     # Define the weight of each category
#     weights = {
#         'critical_thinking': 1.0,
#         'communication': 0.8,
#         'understanding_market': 0.7,
#         'leadership': 0.6
#     }

#     # Critical Thinking Questions
#     critical_thinking = sum([
#         answers['reading_habits'],
#         answers['information_evaluation1'],
#         answers['information_evaluation2'],
#         answers['problem_solving'],
#         answers['engagement_in_discussions'],
#         answers['questioning_curiosity1'],
#         answers['questioning_curiosity2'],
#         answers['creativity']
#     ])

#     # Communication Questions
#     communication = sum([
#         answers['communication_clarity'],
#         answers['communication_participation'],
#         answers['communication_confidence']
#     ])

#     # Understanding Social Politics and Market Needs Questions
#     understanding_market = sum([
#         answers['market_trends_follow'],
#         answers['market_research_analyze'],
#         answers['market_predict_trends'],
#         answers['market_feedback'],
#         answers['market_planning']
#     ])

#     # Leadership Questions
#     leadership = sum([
#         answers['leadership_responsibility'],
#         answers['leadership_decision_making'],
#         answers['leadership_communication'],
#         answers['leadership_conflict_resolution'],
#         answers['leadership_teamwork'],
#         answers['leadership_initiative']
#     ])

#     # Calculate weighted scores
#     computing_score = weights['critical_thinking'] * critical_thinking
#     business_score = (weights['communication'] * communication +
#                       weights['understanding_market'] * understanding_market +
#                       weights['leadership'] * leadership)

#     # Suggest a career based on the scores
#     if computing_score >= business_score:
#         return 'Computing'
#     else:
#         return 'Business'

# View to handle the survey form
def survey_view(request):
    # if request.method == 'POST':
    #     form = SurveyForm(request.POST)
    #     if form.is_valid():
    #         answers = {key: int(value) for key, value in form.cleaned_data.items()}
    #         suggestion = suggest_career(answers)
    #         return render(request, 'result.html', {'suggestion': suggestion})
    # else:
    #     form = SurveyForm()          , {'form': form}
    return render(request, 'survey.html')










def studentpage(request):
    co_data = College_List.objects.all()
    co_number = College_List.objects.all().count()
    college_number = {'college_number', co_number}
    college_data = {'college_data': co_data}
    return render(request, 'studentpage.html',college_data)













def initial_survey(request):
    if request.method == 'POST':
        form = InitialSurveyForm(request.POST)
        if form.is_valid():
            answers = {key: int(value) for key, value in form.cleaned_data.items()}
            result = determine_science_field(answers)
            broad_category = result['broad_category']
            if broad_category == 'Life Sciences':
                return redirect('life_science_detail')
            elif broad_category == 'Physical Sciences':
                return redirect('physical_science_detail')
    else:
        form = InitialSurveyForm()
    return render(request, 'initial_survey.html', {'form': form})

def life_science_detail(request):
    if request.method == 'POST':
        form = LifeScienceDetailForm(request.POST)
        if form.is_valid():
            answers = {key: int(value) for key, value in form.cleaned_data.items()}
            suggestion = suggest_life_science_field(answers)
            return render(request, 'result2.html', {'suggestion': suggestion})
    else:
        form = LifeScienceDetailForm()
    return render(request, 'life_science_detail.html', {'form': form})

def physical_science_detail(request):
    if request.method == 'POST':
        form = PhysicalScienceDetailForm(request.POST)
        if form.is_valid():
            answers = {key: int(value) for key, value in form.cleaned_data.items()}
            suggestion = suggest_physical_science_field(answers)
            return render(request, 'result2.html', {'suggestion': suggestion})
    else:
        form = PhysicalScienceDetailForm()
    return render(request, 'physical_science_detail.html', {'form': form})


# Define the function to initialize answers
def initialize_answers(user_input, all_traits):
    answers = {trait: user_input.get(trait, 0) for trait in all_traits}
    return answers

# Define all possible traits
initial_traits = [
    'curiosity', 'attention_to_detail', 'patience', 'empathy', 'critical_thinking',
    'adaptability', 'collaboration', 'analytical_skills', 'creativity', 'technical_aptitude',
    'problem_solving', 'observational_skills', 'scientific_rigor'
]

life_science_traits = [
    'plant_propagation', 'herbarium_collection', 'botanical_illustration', 'plant_id_walks',
    'bonsai_cultivation', 'orchid_cultivation', 'edible_plant_foraging', 'ethnobotany',
    'carnivorous_plant_cultivation', 'terrarium_gardening', 'birdwatching',
    'insect_collecting', 'wildlife_photography', 'animal_tracking', 'aquarium_keeping',
    'reptile_husbandry', 'butterfly_gardening', 'mammal_tracking', 'ethology',
    'zoo_volunteering', 'nature_watching', 'nature_photography', 'citizen_science_projects',
    'hiking_nature_walks', 'wildlife_habitat_restoration', 'environmental_education',
    'botanical_gardening', 'volunteering_conservation', 'nature_journaling',
    'ecological_field_research', 'systems_thinking', 'collaborative_work', 'data_analysis_skills',
    'understanding_ecosystem_dynamics', 'environmental_stewardship', 'appreciation_for_biodiversity',
    'dedication_to_conservation', 'ethical_research', 'compassion_for_animals'
]


# Expand the list of physical science traits to include Chemistry and Geology
physical_science_traits = [
    'amateur_astronomy', 'model_rocketry', 'robotics', 'diy_electronics', 'water_rockets',
    'physics_puzzles', 'lego_engineering', 'high_speed_photography', 'magnets_experiments',
    'replicating_experiments', 'reading_physics_books', 'physics_based_video_games',
    'attending_physics_lectures', 'watching_documentaries', 'participating_in_physics_olympiads',
    'experimental_skills', 'logical_reasoning', 'home_chemistry_experiments', 'crystal_growing',
    'brewing_beer_wine', 'soap_making', 'perfume_blending', 'diy_cosmetics',
    'electroplating_metal_etching', 'candle_making', 'alchemy_board_games', 'molecular_gastronomy',
    'creativity_in_designing_compounds', 'precision_in_lab_techniques', 'tinkering_with_mechanical_devices',
    'building_physics_models', 'participating_in_physics_clubs', 'conducting_simple_physics_experiments',
    'mineral_collecting', 'rock_identification', 'fossil_hunting', 'volcano_study',
    'soil_analysis', 'geological_mapping', 'field_geology', 'geochemical_analysis',
    'petrology', 'seismology', 'hydrogeology', 'remote_sensing',
    'analytical_skills', 'creativity', 'logical_reasoning'
]


# Define functions to suggest broader categories
def suggest_broad_category(answers):
    category_scores = {
        'Life Sciences': sum([
            answers.get('curiosity', 0),
            answers.get('attention_to_detail', 0),
            answers.get('patience', 0),
            answers.get('empathy', 0),
            answers.get('critical_thinking', 0),
            answers.get('adaptability', 0),
            answers.get('collaboration', 0),
            answers.get('creativity', 0),
            answers.get('observational_skills', 0),
            answers.get('compassion_for_animals', 0)
        ]),
        'Physical Sciences': sum([
            answers.get('critical_thinking', 0),
            answers.get('analytical_skills', 0),
            answers.get('technical_aptitude', 0),
            answers.get('problem_solving', 0),
            answers.get('scientific_rigor', 0),
            answers.get('creativity', 0),
            answers.get('adaptability', 0),
            answers.get('curiosity', 0)
        ])
    }

    return max(category_scores, key=category_scores.get)

# Define functions to suggest specific fields within each category
def suggest_life_science_field(answers):
    field_scores = {
        'Botany': sum([
            answers.get('plant_propagation', 0),
            answers.get('herbarium_collection', 0),
            answers.get('botanical_illustration', 0),
            answers.get('plant_id_walks', 0),
            answers.get('bonsai_cultivation', 0),
            answers.get('orchid_cultivation', 0),
            answers.get('edible_plant_foraging', 0),
            answers.get('ethnobotany', 0),
            answers.get('carnivorous_plant_cultivation', 0),
            answers.get('terrarium_gardening', 0),
            answers.get('curiosity', 0),
            answers.get('dedication_to_conservation', 0),
            answers.get('observational_skills', 0)
        ]),
        'Zoology': sum([
            answers.get('birdwatching', 0),
            answers.get('insect_collecting', 0),
            answers.get('wildlife_photography', 0),
            answers.get('animal_tracking', 0),
            answers.get('aquarium_keeping', 0),
            answers.get('reptile_husbandry', 0),
            answers.get('butterfly_gardening', 0),
            answers.get('mammal_tracking', 0),
            answers.get('ethology', 0),
            answers.get('zoo_volunteering', 0),
            answers.get('compassion_for_animals', 0),
            answers.get('empathy', 0),
            answers.get('curiosity', 0)
        ]),
        'Ecology': sum([
            answers.get('nature_watching', 0),
            answers.get('nature_photography', 0),
            answers.get('citizen_science_projects', 0),
            answers.get('hiking_nature_walks', 0),
            answers.get('wildlife_habitat_restoration', 0),
            answers.get('environmental_education', 0),
            answers.get('botanical_gardening', 0),
            answers.get('volunteering_conservation', 0),
            answers.get('nature_journaling', 0),
            answers.get('ecological_field_research', 0),
            answers.get('systems_thinking', 0),
            answers.get('data_analysis_skills', 0),
            answers.get('environmental_stewardship', 0),
            answers.get('observational_skills', 0),
            answers.get('dedication_to_conservation', 0)
        ])
    }

    return max(field_scores, key=field_scores.get)

def suggest_physical_science_field(answers):
    field_scores = {
        'Physics': sum([
            answers.get('amateur_astronomy', 0),
            answers.get('model_rocketry', 0),
            answers.get('robotics', 0),
            answers.get('diy_electronics', 0),
            answers.get('water_rockets', 0),
            answers.get('physics_puzzles', 0),
            answers.get('lego_engineering', 0),
            answers.get('high_speed_photography', 0),
            answers.get('magnets_experiments', 0),
            answers.get('replicating_experiments', 0),
            answers.get('analytical_skills', 0),
            answers.get('creativity', 0),
            answers.get('logical_reasoning', 0)
        ]),
        'Chemistry': sum([
            answers.get('home_chemistry_experiments', 0),
            answers.get('crystal_growing', 0),
            answers.get('brewing_beer_wine', 0),
            answers.get('soap_making', 0),
            answers.get('perfume_blending', 0),
            answers.get('diy_cosmetics', 0),
            answers.get('electroplating_metal_etching', 0),
            answers.get('candle_making', 0),
            answers.get('molecular_gastronomy', 0),
            answers.get('creativity_in_designing_compounds', 0),
            answers.get('precision_in_lab_techniques', 0),
            answers.get('analytical_skills', 0),
            answers.get('logical_reasoning', 0)
        ]),
       'Astronomy': sum([  
            answers.get('amateur_astronomy', 0),
            answers.get('model_rocketry', 0),
            answers.get('robotics', 0),
            answers.get('diy_electronics', 0),
            answers.get('water_rockets', 0),
            answers.get('physics_puzzles', 0),
            answers.get('lego_engineering', 0),
            answers.get('high_speed_photography', 0),
            answers.get('magnets_experiments', 0),
            answers.get('replicating_experiments', 0),
            answers.get('analytical_skills', 0),
            answers.get('creativity', 0),
            answers.get('logical_reasoning', 0)
        ])
    }

    return max(field_scores, key=field_scores.get)

# Main function to determine field
def determine_science_field(user_input):
    # Initialize answers based on user input
    all_traits = initial_traits + life_science_traits + physical_science_traits
    answers = initialize_answers(user_input, all_traits)
    
    # Determine broad category
    broad_category = suggest_broad_category(answers)
    
    # Determine specific field
    if broad_category == 'Life Sciences':
        specific_field = suggest_life_science_field(answers)
    else:
        specific_field = suggest_physical_science_field(answers)
    
    return {
        'broad_category': broad_category,
        'specific_field': specific_field
    }






def college_detail(request,post_id):

   collegepost = College_List.objects.get(id = post_id)


   return render(request, 'college_detail.html',{'x':collegepost})