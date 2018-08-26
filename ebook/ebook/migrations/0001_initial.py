# Generated by Django 2.1 on 2018-08-22 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ebook.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='도서명')),
                ('author', models.CharField(max_length=50, verbose_name='저자')),
                ('description', models.CharField(blank=True, max_length=300, verbose_name='책요약/소개')),
                ('image', ebook.fields.ThumbnailImageField(upload_to='photo/%Y/%m')),
                ('content', models.FileField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='RentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rent_start', models.DateTimeField(verbose_name='대여시작일')),
                ('rent_end', models.DateField(verbose_name='대여종료일')),
                ('rent_status', models.BooleanField(verbose_name='반납여부')),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ebook.Books', verbose_name='대출도서')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='대출회원')),
            ],
        ),
    ]
