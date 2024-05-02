from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import Appointment, WorkingSchedule, AppointmentPrice
import random
import string
from django.utils import timezone
import datetime
from django.db.models import Q

User = get_user_model()


def create_price(sender, **kwargs):
    try:
        price = AppointmentPrice.objects.get(priceID=1)
    except:
        price = AppointmentPrice.objects.create(priceID=1)
        price.save()


def create_groups(sender, **kwargs):
    all_groups = ["Admin", "Doctor", "Nurse", "Patient"]
    # create groups if they dont already exist
    for group in all_groups:
        try:
            # check group exists
            Group.objects.get(name=group)
        except Group.DoesNotExist:
            # if group does not exist then create it
            Group.objects.create(name=group)
    
    # set permissions
            
            
def create_users(sender, **kwargs):
    # create superuser
    try:
        superuser = User.objects.get(userID="super1")
    except User.DoesNotExist:
        superuser = User.objects.create_superuser(userID="super1", email="superuser@smartcare.com", password="pw1", role="admin", name=f"Super man", is_active=True, location="Bristol")
        superuser.save()

    # create admin
    try:
        admin = User.objects.get(userID="admin1")
    except User.DoesNotExist:
        admin = User.objects.create_user(userID="admin1", email="admin@smartcare.com", password="pw1", role="admin", name=f"Ad Min", is_active=True, location="Bristol")
        admin.save()

    # create patient
    try:
        patient = User.objects.get(userID="patient1")
    except User.DoesNotExist:
        patient = User.objects.create_user(userID="patient1", email="patient@smartcare.com", password="pw1", role="patient", name=f"Pat Ient", is_active=True, location="Bristol")
        patient.save()

    # create doctor
    # this one is active
    try:
        doctor = User.objects.get(userID="DrFirst01")
    except User.DoesNotExist:
        doctor = User.objects.create_user(userID="DrFirst01", email="dr_first@smartcare.com", password="pw1", role="doctor", name=f"Dr First", is_active=True, location="Bristol")
        doctor.save()
        # schedule1 = WorkingSchedule.objects.create(user=doctor, schedule={"Monday": True, "Tuesday": False, "Wednesday": False, "Thursday": False, "Friday": True, "Saturday": False, "Sunday": False})
        # schedule1.save()

    # create nurse
    # this one is active
    try:
        nurse = User.objects.get(userID="MsBest01")
    except User.DoesNotExist:
        nurse = User.objects.create_user(userID="MsBest01", email="ms_best@smartcare.com", password="pw1", role="nurse", name=f"Ms Best", is_active=True, location="Bristol")
        nurse.save()
        # schedule4 = WorkingSchedule.objects.create(nurse, {"Monday": True, "Tuesday": False, "Wednesday": False, "Thursday": False, "Friday": True, "Saturday": False, "Sunday": False})
        # schedule4.save()

    # 10 realistic clients
    try:
        rob_smith = User.objects.get(userID="RobSmith01")
    except User.DoesNotExist:
        rob_smith = User.objects.create_user(userID="RobSmith01", email="rob_smith@hotmail.com", date_of_birth=(datetime.date.today() - datetime.timedelta(weeks=(random.randint(20, 70)*52))), phone_number="0" + str(random.randint(1000000000, 9999999999)), nhs_number=str(random.randint(1000000000, 9999999999)), password="pw1", role="patient", name=f"Rob Smith", is_active=True, location="Bristol")
        rob_smith.save()

    try:
        liz_brown = User.objects.get(userID="LizBrown01")
    except User.DoesNotExist:
        liz_brown = User.objects.create_user(userID="LizBrown01", email="liz_brown@hotmail.com", date_of_birth=(datetime.date.today() - datetime.timedelta(weeks=(random.randint(20, 70)*52))), phone_number="0" + str(random.randint(1000000000, 9999999999)), nhs_number=str(random.randint(1000000000, 9999999999)), password="pw1", role="patient", name=f"Liz Brown", is_active=True, location="Bristol")
        liz_brown.save()

    try:
        mr_hesitant = User.objects.get(userID="MrHesitant01")
    except User.DoesNotExist:
        mr_hesitant = User.objects.create_user(userID="MrHesitant01", email="mr_hesitant@hotmail.com", date_of_birth=(datetime.date.today() - datetime.timedelta(weeks=(random.randint(20, 70)*52))), phone_number="0" + str(random.randint(1000000000, 9999999999)), nhs_number=str(random.randint(1000000000, 9999999999)), password="pw1", role="patient", name=f"Mr Hesitant", is_active=True, location="Bristol")
        mr_hesitant.save()

    try:
        james_bond = User.objects.get(userID="JamesBond01")
    except User.DoesNotExist:
        james_bond = User.objects.create_user(userID="JamesBond01", email="james_bond@hotmail.com", date_of_birth=(datetime.date.today() - datetime.timedelta(weeks=(random.randint(20, 70)*52))), phone_number="0" + str(random.randint(1000000000, 9999999999)), nhs_number=str(random.randint(1000000000, 9999999999)), password="pw1", role="patient", name=f"James Bond", is_active=True, location="Bristol")
        james_bond.save()

    try:
        jane_marie = User.objects.get(userID="JaneMarie01")
    except User.DoesNotExist:
        jane_marie = User.objects.create_user(userID="JaneMarie01", email="jane_marie@hotmail.com", date_of_birth=(datetime.date.today() - datetime.timedelta(weeks=(random.randint(20, 70)*52))), phone_number="0" + str(random.randint(1000000000, 9999999999)), nhs_number=str(random.randint(1000000000, 9999999999)), password="pw1", role="patient", name=f"Jane Marie", is_active=True, location="Bristol")
        jane_marie.save()    

    try:
        amy_sanders = User.objects.get(userID="AmySanders01")
    except User.DoesNotExist:
        amy_sanders = User.objects.create_user(userID="AmySanders01", email="amy_sanders@hotmail.com", date_of_birth=(datetime.date.today() - datetime.timedelta(weeks=(random.randint(20, 70)*52))), phone_number="0" + str(random.randint(1000000000, 9999999999)), nhs_number=str(random.randint(1000000000, 9999999999)), password="pw1", role="patient", name=f"Amy Sanders", is_active=True, location="Bristol")
        amy_sanders.save()

    try:
        andrew_clark = User.objects.get(userID="AndrewClark01")
    except User.DoesNotExist:
        andrew_clark = User.objects.create_user(userID="AndrewClark01", email="andrew_clark@hotmail.com", date_of_birth=(datetime.date.today() - datetime.timedelta(weeks=(random.randint(20, 70)*52))), phone_number="0" + str(random.randint(1000000000, 9999999999)), nhs_number=str(random.randint(1000000000, 9999999999)), password="pw1", role="patient", name=f"Andrew Clark", is_active=True, location="Bristol")
        andrew_clark.save()

    try:
        dewayne_kajetan = User.objects.get(userID="DewayneKajetan01")
    except User.DoesNotExist:
        dewayne_kajetan = User.objects.create_user(userID="DewayneKajetan01", email="dewayne_kajetan@hotmail.com", date_of_birth=(datetime.date.today() - datetime.timedelta(weeks=(random.randint(20, 70)*52))), phone_number="0" + str(random.randint(1000000000, 9999999999)), nhs_number=str(random.randint(1000000000, 9999999999)), password="pw1", role="patient", name=f"Dewayne Kajetan", is_active=True, location="Bristol")
        dewayne_kajetan.save()

    try:
        alana_rosette = User.objects.get(userID="AlanaRosette01")
    except User.DoesNotExist:
        alana_rosette = User.objects.create_user(userID="AlanaRosette01", email="alana_rosette@hotmail.com", date_of_birth=(datetime.date.today() - datetime.timedelta(weeks=(random.randint(20, 70)*52))), phone_number="0" + str(random.randint(1000000000, 9999999999)), nhs_number=str(random.randint(1000000000, 9999999999)), password="pw1", role="patient", name=f"Alana Rosette", is_active=True, location="Bristol")
        alana_rosette.save()

    try:
        shaun_bean = User.objects.get(userID="ShaunBean01")
    except User.DoesNotExist:
        shaun_bean = User.objects.create_user(userID="ShaunBean01", email="shaun_bean@hotmail.com", date_of_birth=(datetime.date.today() - datetime.timedelta(weeks=(random.randint(20, 70)*52))), phone_number="0" + str(random.randint(1000000000, 9999999999)), nhs_number=str(random.randint(1000000000, 9999999999)), password="pw1", role="patient", name=f"Shaun Bean", is_active=True, location="Bristol")
        shaun_bean.save()


def create_appointments(sender, **kwargs):
    for i in range(-7, 14):
        for j in range(9, 17):
            if i <= 0:
                r = range(0, 50, 10)
            elif i <= 7:
                r = range(0, 50, 20)
            else:
                r = range(0, 10, 30)
            for k in r:
                try:
                    appointment = Appointment.objects.get(date=(datetime.date.today() + datetime.timedelta(days=i)), appointment_time=(datetime.time(hour=j, minute=k)))
                except:
                    patient = random.choice(User.objects.filter(role="patient"))
                    doctor = random.choice(User.objects.filter(Q(role="doctor") | Q(role="nurse")))
                    time = datetime.time(hour=j, minute=k)
                    end_time = (datetime.datetime.combine(datetime.date(1,1,1),time) + datetime.timedelta(minutes=10)).time()
                    appointment = Appointment.objects.create(
                        patient=patient, 
                        doctor=doctor, 
                        date=(datetime.date.today() + datetime.timedelta(days=i)),
                        appointment_time=time,
                        appointment_end_time=end_time,
                        patient_type=random.choice(["NHS", "Private"]),
                        appointment_status="Scheduled"
                    ) 
                    appointment.save()
