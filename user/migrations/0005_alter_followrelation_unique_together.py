# Generated by Django 4.1.2 on 2022-11-17 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_user_followings_followrelation'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='followrelation',
            unique_together={('from_user', 'to_user')},
        ),
    ]
