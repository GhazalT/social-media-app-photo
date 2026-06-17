from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_profile_support_fields_support"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="support",
            name="creator",
        ),
        migrations.RemoveField(
            model_name="support",
            name="supporter",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="support_enabled",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="support_goal",
        ),
        migrations.DeleteModel(
            name="Support",
        ),
    ]
