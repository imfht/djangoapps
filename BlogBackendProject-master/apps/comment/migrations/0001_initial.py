# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-23 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_content', models.TextField(help_text='原始内容', verbose_name='原始内容')),
                ('formatted_content', models.TextField(blank=True, help_text='处理后内容', null=True, verbose_name='处理后内容')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name_plural': '评论详细信息列表',
                'verbose_name': '评论详细信息',
            },
        ),
        migrations.CreateModel(
            name='CommentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_level', models.IntegerField(default=0, help_text='评论级别', verbose_name='评论级别')),
                ('like_num', models.IntegerField(default=0, help_text='点赞数', verbose_name='点赞数')),
                ('unlike_num', models.IntegerField(default=0, help_text='反对数', verbose_name='反对数')),
                ('comment_num', models.IntegerField(default=0, help_text='评论数', verbose_name='评论数')),
                ('is_hot', models.BooleanField(default=False, help_text='是否热门', verbose_name='是否热门')),
                ('is_recommend', models.BooleanField(default=False, help_text='是否推荐', verbose_name='是否推荐')),
                ('is_active', models.BooleanField(default=True, help_text='是否激活', verbose_name='是否激活')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', null=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name_plural': '评论基本信息列表',
                'verbose_name': '评论基本信息',
            },
        ),
    ]