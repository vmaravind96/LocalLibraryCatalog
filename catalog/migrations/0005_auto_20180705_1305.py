# Generated by Django 2.0.6 on 2018-07-05 07:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20180702_1423'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'permissions': [('can_edit_author', 'Add,modify or del author')]},
        ),
    ]
