# Generated by Django 4.1.2 on 2022-10-15 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("components", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favouritemovie",
            name="custom_title",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="favouriteplanet",
            name="custom_name",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterUniqueTogether(
            name="favouritemovie",
            unique_together={("user_id", "movie")},
        ),
        migrations.AlterUniqueTogether(
            name="favouriteplanet",
            unique_together={("user_id", "planet")},
        ),
    ]