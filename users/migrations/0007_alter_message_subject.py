# Generated by Django 4.0.3 on 2022-04-05 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_email_message_sender_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=200),
        ),
    ]
