#Yeamin
# views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Avg,Q
from Users.forms import ProfileImageForm
from .models import ProfileImage, SkillOption, profile, Skill, PublicProfile,Rating
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def login_page(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            if not User.objects.filter(username=username).exists():
                errors['username_error'] = "Username does not exist."
            else:
                errors['password_error'] = "Incorrect password. Please try again."
    return render(request, 'login.html', {'errors': errors})

def signup_page(request):
    errors = {}
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            errors['username_error'] = "Username already exists. Please choose a different username."
        if User.objects.filter(email=email).exists():
            errors['email_error'] = "An account with this email already exists. Please use a different email."
        if len(pass1) < 4:
            errors['password_error'] = "Password is too short. It must be at least 4 characters long."
        if pass1 != pass2:
            errors['confirm_password_error'] = "Your password and confirm password are not the same!"

        if not errors:
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html', {'errors': errors})

@login_required
def profile_page(request):
    user_profile_instance, created = profile.objects.get_or_create(user=request.user)
    errors = {}  

    if request.method == 'POST':
        img = request.FILES.get('img')
        bio = request.POST.get('bio')
        name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        location = request.POST.get('location')

        
        if img:
            user_profile_instance.image = img
        if bio:
            user_profile_instance.bio = bio
        if name:
            user_profile_instance.name = name
        if birthday:
            user_profile_instance.birthday = birthday

        
        if phone:
            if phone.isdigit() and len(phone) == 11:
                user_profile_instance.phone = phone
            else:
                errors['phone_error'] = "Invalid phone number. Please enter an 11-digit number."

        if gender:
            user_profile_instance.gender = gender    
        if location:
            user_profile_instance.location = location
        
        
        if not errors:
            user_profile_instance.save()
            return redirect('profile')  

    return render(request, 'profile.html', {'profile': user_profile_instance, 'user': request.user, 'errors': errors})

def Ulogout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def delete_profile(request):
    if request.method == 'POST':
        
        user = request.user
        user.delete()
        messages.success(request, "Your profile has been deleted successfully.")
        return redirect('signup')  

    return render(request, 'delete_profile.html')

@login_required
def activate_professional_mode(request):
    user_profile_instance = profile.objects.get(user=request.user)
    user_profile_instance.status = "Professional"
    user_profile_instance.save()
    return redirect('profile')



@login_required
def Skills(request):
    skill_options = SkillOption.objects.all()  

    if request.method == 'POST':
        skill_name = request.POST.get('skill_name')
        skill_description = request.POST.get('skill_description')
        skill_price = request.POST.get('skill_price')
        
        
        existing_skill = Skill.objects.filter(user=request.user, name=skill_name).first()
        
        if existing_skill:
            messages.error(request, "You have already registered this skill.")
        else:
            
            skill_option = SkillOption.objects.get(name=skill_name)
            skill_category = skill_option.category

            Skill.objects.create(
                user=request.user,
                name=skill_name,
                category=skill_category,
                description=skill_description,
                price=skill_price
            )
            messages.success(request, "Skill added successfully!")
            return redirect('profile')  

    return render(request, 'add_skill.html', {'skill_options': skill_options})


@login_required
def view_skill(request):
    
    user_skills = Skill.objects.filter(user=request.user)
    return render(request, 'view_skills.html', {'skills': user_skills})




def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_public_profile, created = PublicProfile.objects.get_or_create(user=user)

    skills = Skill.objects.filter(user=user)
    images = ProfileImage.objects.filter(user=user)

    followers_count = user_public_profile.followers.count()
    following_count = user_public_profile.following.count() 
    rating = user_public_profile.rating

   
    is_following = request.user.is_authenticated and user_public_profile.followers.filter(id=request.user.id).exists()

    is_owner = request.user == user

   
    has_rated = request.user.is_authenticated and Rating.objects.filter(rated_user=user, rated_by=request.user).exists()

    context = {
        'public_profile': user_public_profile,
        'skills': skills,
        'images': images,
        'followers_count': followers_count,
        'following_count': following_count,
        'rating': rating,
        'is_following': is_following,
        'is_owner': is_owner,
        'has_rated': has_rated,  
    }

    return render(request, 'public_profile.html', context)



@login_required
def toggle_follow(request, username):
    
    user_to_follow = get_object_or_404(User, username=username)
    public_profile = get_object_or_404(PublicProfile, user=user_to_follow)

    logged_in_profile, created = PublicProfile.objects.get_or_create(user=request.user)

    if public_profile.followers.filter(id=request.user.id).exists():

        public_profile.followers.remove(request.user)

        logged_in_profile.following.remove(user_to_follow)
        messages.success(request, f"You unfollowed {user_to_follow.username}.")
    else:

        public_profile.followers.add(request.user)

        logged_in_profile.following.add(user_to_follow)
        messages.success(request, f"You followed {user_to_follow.username}.")


    public_profile.save()
    logged_in_profile.save()

    return redirect('public_profile', username=username)




def filter_skills(request):
    categories = Skill.objects.values_list('category', flat=True).distinct()
    skill_names = Skill.objects.values_list('name', flat=True).distinct()

    divisions = [
        'Dhaka', 'Chattogram', 'Khulna', 'Rajshahi', 'Barishal', 'Sylhet', 'Rangpur', 'Mymensingh'
    ]

    selected_category = request.GET.get('category')
    selected_skill_name = request.GET.get('skill_name')
    selected_location = request.GET.get('location')
    selected_rating = request.GET.get('rating')


    skill_users = profile.objects.filter(
        status='Professional',
        user__public_profile__isnull=False
    )

    if selected_category:
        skill_users = skill_users.filter(user__skills__category=selected_category)
    if selected_skill_name:
        skill_users = skill_users.filter(user__skills__name=selected_skill_name)
    if selected_location:
        skill_users = skill_users.filter(location=selected_location)
    if selected_rating:
        skill_users = skill_users.filter(user__public_profile__rating__gte=int(selected_rating))

    skill_users = skill_users.distinct()

    context = {
        'categories': categories,
        'skill_names': skill_names,
        'divisions': divisions,
        'skill_users': skill_users,
        'selected_category': selected_category,
        'selected_skill_name': selected_skill_name,
        'selected_location': selected_location,
        'selected_rating': selected_rating,
    }
    return render(request, 'filter_skills.html', context)




def services_page(request):
    categories = SkillOption.objects.values('category').annotate(skill_count=Count('name'))
    skills = SkillOption.objects.all()
    return render(request, 'services.html', {'categories': categories, 'skills': skills})



@login_required
def submit_rating(request, username):
    if request.method == 'POST':
        user_to_rate = get_object_or_404(User, username=username)

        
        if request.user == user_to_rate:
            messages.error(request, "You cannot rate yourself.")
            return redirect('public_profile', username=username)

        
        try:
            rating_value = int(request.POST.get('rating_value'))
        except (ValueError, TypeError):
            messages.error(request, "Invalid rating value.")
            return redirect('public_profile', username=username)

        if rating_value < 1 or rating_value > 5:
            messages.error(request, "Rating must be between 1 and 5.")
            return redirect('public_profile', username=username)

        
        existing_rating = Rating.objects.filter(rated_user=user_to_rate, rated_by=request.user).first()
        if existing_rating:
            messages.error(request, "You have already rated this user.")
            return redirect('public_profile', username=username)

        
        Rating.objects.create(rated_user=user_to_rate, rated_by=request.user, rating_value=rating_value)

        
        user_ratings = Rating.objects.filter(rated_user=user_to_rate)
        average_rating = user_ratings.aggregate(Avg('rating_value'))['rating_value__avg']
        user_to_rate.public_profile.rating = average_rating
        user_to_rate.public_profile.save()

        
        messages.success(request, f"You successfully rated {user_to_rate.username} with a {rating_value}.")
        return redirect('public_profile', username=username)
    
@login_required
def delete_rating(request, username):
    user_to_unrate = get_object_or_404(User, username=username)

    
    rating = Rating.objects.filter(rated_user=user_to_unrate, rated_by=request.user).first()
    if rating:
        rating.delete()

       
        user_ratings = Rating.objects.filter(rated_user=user_to_unrate)
        average_rating = user_ratings.aggregate(Avg('rating_value'))['rating_value__avg'] or 0.0
        user_to_unrate.public_profile.rating = average_rating
        user_to_unrate.public_profile.save()

        messages.success(request, f"Your rating for {user_to_unrate.username} has been removed.")
    else:
        messages.error(request, "You have not rated this user yet.")

    return redirect('public_profile', username=username)

def search(request):
    query = request.GET.get('query', '').strip()

    
    users = User.objects.filter(
        Q(username__icontains=query) | Q(profile__name__icontains=query)
    ).distinct() if query else []

    
    skills = Skill.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
    ).distinct() if query else []

    context = {
        'query': query,
        'users': users,
        'skills': skills,
    }

    return render(request, 'search_results.html', context)




@login_required
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        ProfileImage.objects.create(user=request.user, image=image_file)
        messages.success(request, "Image uploaded successfully!")
    else:
        messages.error(request, "Failed to upload image. Please try again.")
    return redirect('public_profile', username=request.user.username)