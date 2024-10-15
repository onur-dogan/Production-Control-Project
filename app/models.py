from django.db import models


# For storing the teams
class Team(models.Model):
    name = models.CharField(null=False, max_length=255)
    # It would be better to create another table for permissions and assign them to the teams if there would be multiple permissions
    has_assemble_permission = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# For storing each user registered in the system
class User(models.Model):
    # Each user should belong to a team
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    name = models.TextField(null=False, max_length=255)
    surname = models.TextField(null=False, max_length=255)
    email = models.CharField(null=False, max_length=255)
    password = models.CharField(null=False, max_length=255)
    # Store user's activity to check whether user is active or not
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Store the latest login tepmorarily for now
    latest_login = models.DateTimeField(auto_now=True)


# For storing the aircraft's information
class Aircraft(models.Model):
    # Store aircraft's name and descriptions about it
    name = models.CharField(null=False, max_length=255)
    description = models.TextField(null=True, max_length=3000)
    # For the aircraft that is no longer produced, store them as passive
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# For storing each part that will be used to produce aircraft
class Part(models.Model):
    # Each parts can be produced by one team
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    # Each parts are produced specially for each aircrafts
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT)
    name = models.CharField(null=False, max_length=255)
    description = models.TextField(null=True, max_length=3000)
    # Parts might not be producing anymore but they should stay in DB as passive
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# For counting the part's amounts in the store
class Part_stock(models.Model):
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    # Store each part's stock information in DB
    count = models.IntegerField(null=False, default=0)
    updated_at = models.DateTimeField(auto_now=True)


# For defining the stock mobility processes status
class Part_stock_status(models.Model):
    name = models.CharField(null=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


# For storing the produced, canceled, or have any other situations aircrafts
class Aircraft_production(models.Model):
    # Aircraft's special product no
    product_no = models.IntegerField(null=False)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.PROTECT)
    # The used parts information for producing the aircraft
    used_parts = models.ManyToManyField(Part)
    # To store the status of whether the production is completed, waiting, or canceled. For now, only checking the completed/canceled status
    is_completed = models.BooleanField(default=False)
    # To store the status of whether the production is canceled
    is_canceled = models.BooleanField(default=False)
    # The related user id who gave the production order
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# For displaying the stock mobility processes in store
class Part_stock_mobility(models.Model):
    # Store the aircraft production information to check which parts are used for which aircrafts
    aircraft_production = models.ForeignKey(
        Aircraft_production, null=True, on_delete=models.PROTECT
    )
    # Store part information to show in the logs
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    # Store status like it is added to the stock, removed from the stock, or etc.
    status = models.ForeignKey(Part_stock_status, on_delete=models.PROTECT)
    # Manually generated description about the stock mobility
    description = models.TextField(null=False, max_length=1000)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
