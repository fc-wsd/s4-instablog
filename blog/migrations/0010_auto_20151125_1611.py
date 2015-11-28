# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20151121_1601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': (('share_post', 'Can share post'),)},
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='404.png', upload_to='%Y/%m/%d/'),
            preserve_default=False,
        ),
    ]
