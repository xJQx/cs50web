# Generated by Django 2.2.12 on 2021-06-14 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_delete_likedpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikedPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.Posts')),
                ('postuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postuser', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likeuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]