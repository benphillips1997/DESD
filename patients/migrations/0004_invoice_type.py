# Generated by Django 5.0.2 on 2024-04-30 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_prescriptionmedicine_surgerychangerequest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='type',
            field=models.CharField(choices=[('Appointment', 'Appointment'), ('Prescription', 'Prescription')], default='Appointment', max_length=12),
        ),
    ]
