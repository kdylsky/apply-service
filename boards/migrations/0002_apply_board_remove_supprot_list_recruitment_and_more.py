# Generated by Django 4.1.2 on 2022-10-16 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('companies', '0001_initial'),
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'applies',
            },
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField()),
                ('descrtption', models.TextField()),
                ('position', models.CharField(max_length=50)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company')),
                ('skills', models.ManyToManyField(related_name='board_of_skills', to='boards.skill')),
            ],
            options={
                'db_table': 'boards',
            },
        ),
        migrations.RemoveField(
            model_name='supprot_list',
            name='recruitment',
        ),
        migrations.RemoveField(
            model_name='supprot_list',
            name='user',
        ),
        migrations.DeleteModel(
            name='Recruitment',
        ),
        migrations.DeleteModel(
            name='Supprot_list',
        ),
        migrations.AddField(
            model_name='apply',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.board'),
        ),
        migrations.AddField(
            model_name='apply',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
