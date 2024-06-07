
from .models import CustomUser
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
  
    username = forms.CharField(
        max_length=30,
        help_text='Required. Enter a unique username.',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user mb-3', 'placeholder': 'Enter Username...'})
    )
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Enter a valid email address.',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user mb-3', 'placeholder': 'Email Address'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. Enter your first name.',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user mb-3', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Required. Enter your last name.',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user mb-3', 'placeholder': 'Last Name'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user mb-3', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user mb-3', 'placeholder': 'Confirm Password'})
    )

    role = forms.CharField(
        max_length=100,  # Adjust the max length as per your requirements
        required=True,
        help_text='Enter your role.',  # Provide appropriate help text
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user mb-3', 'placeholder': 'Role'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role')







class InitialSurveyForm(forms.Form):
    curiosity = forms.IntegerField(label='Curiosity', min_value=1, max_value=5)
    attention_to_detail = forms.IntegerField(label='Attention to Detail', min_value=1, max_value=5)
    patience = forms.IntegerField(label='Patience', min_value=1, max_value=5)
    empathy = forms.IntegerField(label='Empathy', min_value=1, max_value=5)
    critical_thinking = forms.IntegerField(label='Critical Thinking', min_value=1, max_value=5)
    adaptability = forms.IntegerField(label='Adaptability', min_value=1, max_value=5)
    collaboration = forms.IntegerField(label='Collaboration', min_value=1, max_value=5)
    analytical_skills = forms.IntegerField(label='Analytical Skills', min_value=1, max_value=5)
    creativity = forms.IntegerField(label='Creativity', min_value=1, max_value=5)
    technical_aptitude = forms.IntegerField(label='Technical Aptitude', min_value=1, max_value=5)
    problem_solving = forms.IntegerField(label='Problem Solving', min_value=1, max_value=5)
    observational_skills = forms.IntegerField(label='Observational Skills', min_value=1, max_value=5)
    scientific_rigor = forms.IntegerField(label='Scientific Rigor', min_value=1, max_value=5)

# Life sciences traits form
class LifeScienceDetailForm(forms.Form):
    plant_propagation = forms.IntegerField(label='Plant Propagation', min_value=1, max_value=5)
    herbarium_collection = forms.IntegerField(label='Herbarium Collection', min_value=1, max_value=5)
    botanical_illustration = forms.IntegerField(label='Botanical Illustration', min_value=1, max_value=5)
    plant_id_walks = forms.IntegerField(label='Plant Identification Walks', min_value=1, max_value=5)
    bonsai_cultivation = forms.IntegerField(label='Bonsai Cultivation', min_value=1, max_value=5)
    orchid_cultivation = forms.IntegerField(label='Orchid Cultivation', min_value=1, max_value=5)
    edible_plant_foraging = forms.IntegerField(label='Edible Plant Foraging', min_value=1, max_value=5)
    ethnobotany = forms.IntegerField(label='Ethnobotany', min_value=1, max_value=5)
    carnivorous_plant_cultivation = forms.IntegerField(label='Carnivorous Plant Cultivation', min_value=1, max_value=5)
    terrarium_gardening = forms.IntegerField(label='Terrarium Gardening', min_value=1, max_value=5)
    birdwatching = forms.IntegerField(label='Birdwatching', min_value=1, max_value=5)
    insect_collecting = forms.IntegerField(label='Insect Collecting', min_value=1, max_value=5)
    wildlife_photography = forms.IntegerField(label='Wildlife Photography', min_value=1, max_value=5)
    animal_tracking = forms.IntegerField(label='Animal Tracking', min_value=1, max_value=5)
    aquarium_keeping = forms.IntegerField(label='Aquarium Keeping', min_value=1, max_value=5)
    reptile_husbandry = forms.IntegerField(label='Reptile Husbandry', min_value=1, max_value=5)
    butterfly_gardening = forms.IntegerField(label='Butterfly Gardening', min_value=1, max_value=5)
    mammal_tracking = forms.IntegerField(label='Mammal Tracking', min_value=1, max_value=5)
    ethology = forms.IntegerField(label='Ethology', min_value=1, max_value=5)
    zoo_volunteering = forms.IntegerField(label='Zoo Volunteering', min_value=1, max_value=5)
    nature_watching = forms.IntegerField(label='Nature Watching', min_value=1, max_value=5)
    nature_photography = forms.IntegerField(label='Nature Photography', min_value=1, max_value=5)
    citizen_science_projects = forms.IntegerField(label='Citizen Science Projects', min_value=1, max_value=5)
    hiking_nature_walks = forms.IntegerField(label='Hiking and Nature Walks', min_value=1, max_value=5)
    wildlife_habitat_restoration = forms.IntegerField(label='Wildlife Habitat Restoration', min_value=1, max_value=5)
    environmental_education = forms.IntegerField(label='Environmental Education', min_value=1, max_value=5)
    botanical_gardening = forms.IntegerField(label='Botanical Gardening', min_value=1, max_value=5)
    volunteering_conservation = forms.IntegerField(label='Volunteering for Conservation', min_value=1, max_value=5)
    nature_journaling = forms.IntegerField(label='Nature Journaling', min_value=1, max_value=5)
    ecological_field_research = forms.IntegerField(label='Ecological Field Research', min_value=1, max_value=5)
    systems_thinking = forms.IntegerField(label='Systems Thinking', min_value=1, max_value=5)
    collaborative_work = forms.IntegerField(label='Collaborative Work', min_value=1, max_value=5)
    data_analysis_skills = forms.IntegerField(label='Data Analysis Skills', min_value=1, max_value=5)
    understanding_ecosystem_dynamics = forms.IntegerField(label='Understanding Ecosystem Dynamics', min_value=1, max_value=5)
    environmental_stewardship = forms.IntegerField(label='Environmental Stewardship', min_value=1, max_value=5)
    appreciation_for_biodiversity = forms.IntegerField(label='Appreciation for Biodiversity', min_value=1, max_value=5)
    dedication_to_conservation = forms.IntegerField(label='Dedication to Conservation', min_value=1, max_value=5)
    ethical_research = forms.IntegerField(label='Ethical Research', min_value=1, max_value=5)
    compassion_for_animals = forms.IntegerField(label='Compassion for Animals', min_value=1, max_value=5)

# Physical sciences traits form
class PhysicalScienceDetailForm(forms.Form):
    amateur_astronomy = forms.IntegerField(label='Amateur Astronomy', min_value=1, max_value=5)
    model_rocketry = forms.IntegerField(label='Model Rocketry', min_value=1, max_value=5)
    robotics = forms.IntegerField(label='Robotics', min_value=1, max_value=5)
    diy_electronics = forms.IntegerField(label='DIY Electronics', min_value=1, max_value=5)
    water_rockets = forms.IntegerField(label='Water Rockets', min_value=1, max_value=5)
    physics_puzzles = forms.IntegerField(label='Physics Puzzles', min_value=1, max_value=5)
    lego_engineering = forms.IntegerField(label='LEGO Engineering', min_value=1, max_value=5)
    high_speed_photography = forms.IntegerField(label='High Speed Photography', min_value=1, max_value=5)
    magnets_experiments = forms.IntegerField(label='Magnets Experiments', min_value=1, max_value=5)
    replicating_experiments = forms.IntegerField(label='Replicating Experiments', min_value=1, max_value=5)
    analytical_skills = forms.IntegerField(label='Analytical Skills', min_value=1, max_value=5)
    creativity = forms.IntegerField(label='Creativity', min_value=1, max_value=5)
    logical_reasoning = forms.IntegerField(label='Logical Reasoning', min_value=1, max_value=5)
    home_chemistry_experiments = forms.IntegerField(label='Home Chemistry Experiments', min_value=1, max_value=5)
    crystal_growing = forms.IntegerField(label='Crystal Growing', min_value=1, max_value=5)
    brewing_beer_wine = forms.IntegerField(label='Brewing Beer/Wine', min_value=1, max_value=5)
    soap_making = forms.IntegerField(label='Soap Making', min_value=1, max_value=5)
    perfume_blending = forms.IntegerField(label='Perfume Blending', min_value=1, max_value=5)
    diy_cosmetics = forms.IntegerField(label='DIY Cosmetics', min_value=1, max_value=5)
    electroplating_metal_etching = forms.IntegerField(label='Electroplating/Metal Etching', min_value=1, max_value=5)
    candle_making = forms.IntegerField(label='Candle Making', min_value=1, max_value=5)
    molecular_gastronomy = forms.IntegerField(label='Molecular Gastronomy', min_value=1, max_value=5)
    creativity_in_designing_compounds = forms.IntegerField(label='Creativity in Designing Compounds', min_value=1, max_value=5)
    precision_in_lab_techniques = forms.IntegerField(label='Precision in Lab Techniques', min_value=1, max_value=5)

   