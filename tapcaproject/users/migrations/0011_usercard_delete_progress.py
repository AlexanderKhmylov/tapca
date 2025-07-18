# Generated by Django 4.1.13 on 2024-12-03 17:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_alter_form_options'),
        ('users', '0010_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.PositiveSmallIntegerField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='cards.card', verbose_name='Карточка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'слово пользователя',
                'verbose_name_plural': 'Слова пользователя',
                'ordering': ('user', 'frequency'),
                'unique_together': {('user', 'card')},
            },
        ),
        migrations.DeleteModel(
            name='Progress',
        ),
    ]
