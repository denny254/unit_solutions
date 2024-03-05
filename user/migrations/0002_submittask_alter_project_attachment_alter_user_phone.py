# Generated by Django 4.2.5 on 2024-03-02 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmitTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('writer_email', models.EmailField(max_length=254)),
                ('date_submitted', models.DateField()),
                ('project_link', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='project',
            name='attachment',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]
