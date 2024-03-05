from django.contrib.auth.models import Group

def create_groups(sender, **kwargs):
    all_groups = ["Admin", "Doctor", "Nurse", "Patient"]
    # create groups if they dont already exist
    for group in all_groups:
        exists = False
        try:
            Group.objects.get(name=group)
        except Group.DoesNotExist:
            pass
        if exists:
            Group.objects.create(name=group)
    
    # set permissions