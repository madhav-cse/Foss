from django.shortcuts import render,redirect
from .models import User,Queries,Profile
from django.contrib import messages
from .forms import RegistrationForm,LoginForm
import datetime
import cv2
import pywhatkit as w
import os
from nylas import APIClient

os.environ["CLIENT_ID"] = "2ptm3q4vfhep6576ndyl8kjp7"
os.environ["CLIENT_SECRET"] = "aunp2lc6r66zz3cnvuzuhkvvc"
os.environ["ACCESS_TOKEN"] = "YCMzFvN8g4fhijt7aNqBFr7mkUEhy6"
def onoff(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    mean_value = cv2.mean(gray_image)[0] 

    if(mean_value<50):
        return 'Shop is closed'
    else:
        return 'Shop is Open'

def send_mail(name,email,body_des):
    nylas = APIClient(
        os.environ.get("CLIENT_ID"),
        os.environ.get("CLIENT_SECRET"),
        os.environ.get("ACCESS_TOKEN"),
    )
    draft = nylas.drafts.create()
    draft.subject = "Hostel Hub"
    draft.body = body_des
    draft.to = [{"name": name, "email": email}]
    draft.send()

email=""
username=""
groupID=1
breakfast=0
lunch=0
dinner=0
super_emails=["ishvaryas@student.tce.edu"]
menu={"sunday":[" Khichadi","Bread Biriyani","Dosa"],"monday":["Idly Vada Sambar","Variety Rice Sweet Pongal","Chapathi Panneer butter masala"],"tuesday":["Dosa Sambar","White Rice Drumstick Sambar Rasam","Kothu parotta"],"wednesday":["Bread Jam","Mushroom Biryani","Idly"],"thursday":["Dosa Sambar","Rice Vatha kuzhambu Rasam","Chapathi Mix veg gravy"],"friday":["Idly Kesari","Rice Sambar Cauliflower fry","Dosa"],"saturday":["Upma","White Rice Paruppu urandai kuzhambu","Puri"]}
def home(request):
    return render(request,"main/index.html")


def about(request):
    return render(request,"main/about.html")


def login(request):
    global email,username,groupID
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['emailid'] 
            password = request.POST['password']
            user=None
            try:
                user = User.objects.get(emailid=email)
                if(user.password!=password):
                    messages.error(request,"The given password does not match!")
                    return redirect("/login")
                else:
                    username=user.username
                    request.session['username'] = username
                    groupID=user.group_id
                    return render(request,"main/hostel.html",{"username":username})
            except User.DoesNotExist:
                user = None
                messages.error(request,"The EmailID is not registered.Try Registering!")
                return redirect("/register")
    else:
        form = LoginForm()

    return render(request, 'main/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if(password1!=password2):
                messages.error(request,"Passwords do not match!")
                return redirect('/register')
            group_id = 1
            if(email in super_emails):
                group_id=2
            if User.objects.filter(emailid=email).exists():
                messages.error(request,"The EmailID is already registered.Try logging in!")
                return redirect("/login")
            user = User(emailid=email, username=username, password=password1, group_id=group_id)
            user.save()
            messages.success(request,"Registration successful!")
            return redirect('/login')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})


def hostel(request):
    return render(request,"main/hostel.html",{"username":username})

def shop(request):
    if request.method == 'POST':
        profile = Profile.objects.get(mailid=email)
        if profile:
            selected_status = request.POST.get('shop_status')
            ret=onoff(f"static/images/{selected_status}.jpg")
            msg="Shop Status at "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+"=>"+ret+".Wishing you a happy stay! Team HostelHub"
            try:
                w.sendwhatmsg_instantly("+91"+str(profile.phno),msg)
            except:
                pass
            send_mail(username,email,msg)
        return render(request,"main/shop.html",{"ret_str":ret})
    return render(request,"main/shop.html")
def create_post(request):
    if request.method == 'POST':
        service = request.POST.get('service')
        description = request.POST.get('description')
        q = Queries(mailid=email, query=description, query_type=service)
        q.save()
        return redirect('/query')
    return render(request,"main/create_post.html")


def poll(request):
    global breakfast,lunch,dinner
    current_day = datetime.datetime.now().strftime("%A")
    msg="Thank you for polling your food preference. You have opted for "
    if request.method == 'POST':
        meal_preferences = request.POST.getlist('meal_preference')
        if(len(meal_preferences)==0):
            msg+="None"
        else:
            for meal in meal_preferences:
                if(meal=="breakfast"):
                    msg+="\n breakfast"
                    breakfast+=1
                if(meal=="lunch"):
                    msg+="\n lunch"
                    lunch+=1
                if(meal=="dinner"):
                    msg+="\n dinner"
                    dinner+=1
            print(breakfast,lunch,dinner)
        msg+=".Wishing you a happy stay! Team HostelHub"
        try:
            profile = Profile.objects.get(mailid=email)
            w.sendwhatmsg_instantly("+91"+str(profile.phno),msg)
        except:
            pass
        send_mail(username,email,msg)
        return render(request,"main/hostel.html",{"username":username})

    return render(request,"main/poll.html",{"food": menu[current_day.lower()]})


def query(request):
    queries = Queries.objects.all()  
    request.session['email'] = email
    if request.method == 'POST':
        query_id = request.POST.get('query_id')
        if query_id:
            Queries.objects.filter(pk=query_id).delete()

    return render(request, 'main/query.html', {'queries': queries,"email":email,"groupID":groupID})

def profile(request):
    try:
        profile = Profile.objects.get(mailid=email)
    
        if request.method == 'POST':
                profile = Profile.objects.get(mailid=email)
                return render(request,"main/hostel.html")
        if profile:
            return render(request,"main/profile.html",{"profile":profile})
        
    except:
         return render(request,"main/hostel.html")

