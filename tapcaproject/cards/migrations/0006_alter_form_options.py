# Generated by Django 4.2.16 on 2024-11-29 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_alter_example_eng_alter_example_rus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='form',
            options={'ordering': ('type',), 'verbose_name': 'форма', 'verbose_name_plural': 'Формы'},
        ),
    ]
