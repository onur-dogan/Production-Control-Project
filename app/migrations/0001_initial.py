from django.db import migrations, models
import django.db.models.deletion
from common.constants import (
    Aircraft,
    Team,
    Part,
    Part_stock_status,
    Aircrafts as aircrafts,
    Parts as parts,
    Part_stock_statuses as part_stock_statuses,
)


def createInitialTeamsData(apps):
    # Get Team model
    team_model = apps.get_model("app", Team)

    # Loop parts since there should be a team for each part. Then, append the Assembly team as extra with a permission
    # Model Example: { id: 1, name: 'Team', has_assemble_permission=False }
    teams = [
        team_model(id=num + 1, name=f"{parts[num]} Team")
        for num in range(0, len(parts))
    ]
    teams.append(team_model(id="5", name="Assembly Team", has_assemble_permission=True))

    # Create the default teams initially
    team_model.objects.bulk_create(teams)


def createInitialAircraftData(apps):
    # Get Aircraft model
    aircraft_model = apps.get_model("app", Aircraft)

    # Create the default aircrafts initially
    aircraft_model.objects.bulk_create(
        [
            # Loop the aircrafts and create models for each one of them quickly, to save in DB as default
            # Model Example: { id: 2, name: KIZILELMA, description: KIZILELMA }
            aircraft_model(id=num + 1, name=aircrafts[num], description=aircrafts[num])
            for num in range(0, len(aircrafts))
        ]
    )


def createInitialPartData(apps):
    # Get Part model
    part_model = apps.get_model("app", Part)
    # Create the default parts initially
    part_model.objects.bulk_create(
        [
            # Part models should include:
            # Team ID to check which team can update the related part's situations
            # Aircraft ID to check which parts are required to produce the aircraft
            # Model Example: { id: 3, team_id: 1, aircraft_id: 2, name: 'TB2 Wing', description: 'TB2 Wing' }
            part_model(
                # Give id automatically between 1,16(4*4 - There are 4 aircraft and 4 parts)
                id=(aircraft_index * 4) + (part_index + 1),
                team_id=part_index + 1,
                aircraft_id=aircraft_index + 1,
                # Combine the aircraft name with the part to customize it. e.g. TB2 Wing, AKINCI Tail, etc.
                name=f"{aircrafts[aircraft_index]} {parts[part_index]}",
                description=f"{aircrafts[aircraft_index]} {parts[part_index]}",
            )
            # Loop the aircrafts since each part should be defined for each aircraft specially
            for aircraft_index in range(0, len(aircrafts))
            # Then, loop the parts and assign them to the aircrafts one to one
            for part_index in range(0, len(parts))
        ]
    )


def createInitialPartStockStatusData(apps):
    # Get Part Stock Status model
    part_stock_status_model = apps.get_model("app", Part_stock_status)
    # Create the default part stock statuses initially
    part_stock_status_model.objects.bulk_create(
        [
            # Loop Part stock status constants and create a model for each
            # Model Example: { id: 4, name: 'Stock Increase' }
            part_stock_status_model(
                id=part_stock_status_index + 1,
                name=part_stock_statuses[part_stock_status_index],
            )
            for part_stock_status_index in range(0, len(part_stock_statuses))
        ]
    )


def createInitialData(apps, schema):
    createInitialTeamsData(apps)
    createInitialAircraftData(apps)
    createInitialPartData(apps)
    createInitialPartStockStatusData(apps)


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Aircraft",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(max_length=3000, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Part",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(max_length=3000, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "aircraft",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="app.aircraft"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Part_stock_status",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("has_assemble_permission", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.TextField(max_length=255)),
                ("surname", models.TextField(max_length=255)),
                ("password", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("latest_login", models.DateTimeField(auto_now=True)),
                (
                    "team",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app.team",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Part_stock_mobility",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("description", models.TextField(max_length=1000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "aircraft",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="app.aircraft",
                    ),
                ),
                (
                    "part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="app.part"
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="app.part_stock_status",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="app.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Part_stock",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("count", models.IntegerField(default=0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="app.part"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="part",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="app.team"
            ),
        ),
        migrations.CreateModel(
            name="Aircraft_production",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("product_no", models.IntegerField()),
                ("is_completed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "aircraft",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="app.aircraft"
                    ),
                ),
                ("used_parts", models.ManyToManyField(to="app.part")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="app.user"
                    ),
                ),
            ],
        ),
        migrations.RunPython(createInitialData),
    ]
