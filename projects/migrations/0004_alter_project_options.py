# Generated by Django 4.0.3 on 2022-04-05 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_review_owner_alter_review_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total', '-created']},
        ),
    ]
