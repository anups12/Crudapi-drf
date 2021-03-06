# Generated by Django 4.0.5 on 2022-06-20 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crudapi', '0003_alter_creator_user_alter_reader_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creator',
            name='course',
        ),
        migrations.RemoveField(
            model_name='creator',
            name='description',
        ),
        migrations.RemoveField(
            model_name='creator',
            name='title',
        ),
        migrations.RemoveField(
            model_name='creator',
            name='user',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='course',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='user',
        ),
        migrations.AddField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crudapi.creator'),
        ),
        migrations.AddField(
            model_name='creator',
            name='username',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reader',
            name='username',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='Enrolled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courses', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crudapi.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crudapi.creator')),
            ],
        ),
    ]
