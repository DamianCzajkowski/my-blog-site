# Generated by Django 4.1.7 on 2023-03-13 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='post_id',
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
