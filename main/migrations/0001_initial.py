# Generated by Django 3.1 on 2020-08-27 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, default='')),
                ('markdown', models.TextField(blank=True, default='')),
                ('docType', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('readFlag', models.IntegerField(choices=[(1, 'open'), (2, 'restricted')], default=1)),
                ('writeFlag', models.IntegerField(choices=[(1, 'open'), (2, 'restricted')], default=2)),
            ],
        ),
        migrations.CreateModel(
            name='FileVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.document')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.file')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('operation', models.IntegerField(choices=[(1, 'open'), (2, 'restricted')])),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.file')),
                ('fileNewVersion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='newLog', to='main.fileversion')),
                ('fileOldVersion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='oldLog', to='main.fileversion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileUserPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissionFlag', models.SmallIntegerField(choices=[(1, 'READ'), (2, 'WRITE'), (3, 'READ/WRITE')])),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.file')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.file')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tag')),
            ],
        ),
        migrations.CreateModel(
            name='FileGroupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permissionFlag', models.SmallIntegerField(choices=[(1, 'READ'), (2, 'WRITE'), (3, 'READ/WRITE')])),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.file')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.group')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='latestVersion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='latestFile', to='main.fileversion'),
        ),
        migrations.AddField(
            model_name='file',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
