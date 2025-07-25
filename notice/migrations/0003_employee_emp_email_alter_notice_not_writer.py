# Generated by Django 4.1 on 2023-06-06 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("notice", "0002_alter_notice_options_notice_not_hits_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="emp_email",
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="notice",
            name="not_writer",
            field=models.ForeignKey(
                db_column="emp_email",
                on_delete=django.db.models.deletion.CASCADE,
                to="notice.employee",
                verbose_name="작성자",
            ),
        ),
    ]
