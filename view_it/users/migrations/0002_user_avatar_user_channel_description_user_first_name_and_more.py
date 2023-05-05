# Generated by Django 4.2.1 on 2023-05-05 03:57

from django.db import migrations, models
import view_it.users.validators


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.FileField(
                blank=True,
                help_text="Supported file types are: .jpg, .jpeg, .png, and .gif",
                upload_to="avatars/%Y/%m/%d/%H/",
                validators=[view_it.users.validators.validate_avatar_file_type],
                verbose_name="Avatar",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="channel_description",
            field=models.TextField(blank=True, verbose_name="Channel Description"),
        ),
        migrations.AddField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                help_text="Required. 30 characters or fewer. Alphabetical characters only.",
                max_length=30,
                null=True,
                validators=[view_it.users.validators.validate_name],
                verbose_name="First Name",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                help_text="Required. 30 characters or fewer. Alphabetical characters only.",
                max_length=30,
                null=True,
                validators=[view_it.users.validators.validate_name],
                verbose_name="Last Name",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True,
                help_text="Required. Must be an unique and valid email address.",
                max_length=254,
                unique=True,
                validators=[view_it.users.validators.validate_unique_email],
                verbose_name="email address",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=30,
                unique=True,
                verbose_name="Username",
            ),
        ),
    ]
