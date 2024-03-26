from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

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
        doctor = User.objects.get(userID="doctor1")
    except User.DoesNotExist:
        doctor = User.objects.create_user(userID="doctor1", email="doctor@smartcare.com", password="pw1", role="doctor", name=f"Doc Tor", is_active=True, location="Bristol")
        doctor.save()

    # this one needs verifying
    try:
        doctor2 = User.objects.get(userID="doctor2")
    except User.DoesNotExist:
        doctor2 = User.objects.create_user(userID="doctor2", email="doctor2@smartcare.com", password="pw1", role="doctor", name=f"Doc Tor", is_active=False, location="Bristol")
        doctor2.save()

    # create nurse
    # this one is active
    try:
        nurse = User.objects.get(userID="nurse1")
    except User.DoesNotExist:
        nurse = User.objects.create_user(userID="nurse1", email="nurse@smartcare.com", password="pw1", role="nurse", name=f"Nur Se", is_active=True, location="Bristol")
        nurse.save()

    # this one needs verifying
    try:
        nurse2 = User.objects.get(userID="nurse2")
    except User.DoesNotExist:
        nurse2 = User.objects.create_user(userID="nurse2", email="nurse2@smartcare.com", password="pw1", role="nurse", name=f"Nur Se", is_active=False, location="Bristol")
        nurse2.save()