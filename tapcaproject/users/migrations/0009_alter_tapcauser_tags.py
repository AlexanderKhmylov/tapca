# Generated by Django 4.1.13 on 2024-12-02 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_alter_form_options'),
        ('users', '0008_tapcauser_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tapcauser',
            name='tags',
            field=models.ManyToManyField(blank=True, to='cards.tag', verbose_name='Категории для изучения'),
        ),
    ]
