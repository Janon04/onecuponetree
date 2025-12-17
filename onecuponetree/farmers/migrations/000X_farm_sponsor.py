from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ("farmers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Farm",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("location", models.CharField(max_length=255, blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="farm_images/")),
                ("video", models.FileField(blank=True, null=True, upload_to="farm_videos/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="FarmSponsorship",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sponsor_name", models.CharField(blank=True, help_text="Optional public sponsor name", max_length=255)),
                ("sponsor_email", models.EmailField(blank=True, help_text="For receipt/confirmation, not shown publicly", max_length=254)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("message", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")], default="pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("farm", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sponsorships", to="farmers.farm")),
            ],
        ),
    ]