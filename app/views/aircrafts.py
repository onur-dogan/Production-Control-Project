from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from ..models import (
    Aircraft,
    Aircraft_production,
    Part,
    Part_stock,
    Part_stock_mobility,
    User,
)
from django_serverside_datatable.views import ServerSideDatatableView
from common.constants import (
    Assembly_aircraft,
    Update_aircraft_production_status,
    Completed,
    Canceled,
)
from common.utils import getStockPartStatus


class Aircrafts(View):
    def get(self, request):
        user_id = request.session["user_id"]
        # If the user session is ended, then the user should log in again
        if user_id is None:
            return redirect("/login/")

        user = User.objects.filter(id=user_id).first()
        # If the user information doesn't exist in DB or the user hasn't permission to see aircraft processes, then logout it
        if user is None or user.team.has_assemble_permission is False:
            request.session["user_id"] = None
            return redirect("/login")

        # Retrieve all aircrafts
        aircrafts = Aircraft.objects.filter(is_active=True).order_by("name")

        # Retrieve aircraft_production which is in progress (Waiting to be completed/canceled)
        in_progress_aircrafts = Aircraft_production.objects.filter(
            is_completed=False, is_canceled=False
        ).order_by("product_no")

        # If an aircraft is selected, retrieve required parts to display on the UI
        produce_aircraft_id = request.GET.get("produce_aircraft_id")
        required_parts = []
        amount_to_produce_aircraft = 1
        if produce_aircraft_id is not None:
            # Retrieve required parts
            required_parts = Part_stock.objects.filter(
                part__aircraft_id=produce_aircraft_id
            )
            # Aircraft amount that will be produced
            amount_to_produce_aircraft = request.GET.get("amount_to_produce_aircraft")
            if amount_to_produce_aircraft is None or amount_to_produce_aircraft == 0:
                amount_to_produce_aircraft = 1

        is_available_to_reproduce = bool(produce_aircraft_id)
        for part in required_parts:
            # Check if the each part amounts are enough to reproduce the aircraft
            if part.count < int(amount_to_produce_aircraft):
                is_available_to_reproduce = False
                break

        data = {
            "aircrafts": aircrafts,
            "required_parts": required_parts,
            "produce_aircraft_id": produce_aircraft_id,
            "selected_aircraft": aircrafts.filter(id=produce_aircraft_id).first(),
            "amount_to_produce_aircraft": int(amount_to_produce_aircraft),
            "is_available_to_reproduce": is_available_to_reproduce,
            "in_progress_aircrafts": in_progress_aircrafts,
        }

        return render(request, "aircrafts/index.html", data)

    def post(self, request):
        process_type = request.POST.get("process_type")
        if process_type == Assembly_aircraft:
            return self.assembly_aircraft(request)
        elif process_type == Update_aircraft_production_status:
            return self.update_aircraft_production_status(request)

        # If it comes for another reason, then no need to do anything. Just refresh the window
        return redirect("/aircrafts/")

    def assembly_aircraft(self, request):
        user_id = request.session["user_id"]
        produce_aircraft_id = request.POST.get("produce_aircraft_id")
        amount_to_produce_aircraft = request.POST.get("amount_to_produce_aircraft")

        latest_aircraft_production = Aircraft_production.objects.order_by(
            "product_no"
        ).last()
        # Set the latest product no to the aircraft.
        # Quick Note: product no can be defined as a string if any string would be used in it
        parts = Part.objects.filter(aircraft_id=produce_aircraft_id)
        # Retrieeve the related aircraft
        produced_aircraft = Aircraft.objects.filter(id=produce_aircraft_id).first()
        # Retrieve stock decrease status to use in mobility table
        decrease_stock_status = getStockPartStatus(False)

        try:
            for i in range(0, int(amount_to_produce_aircraft)):
                # Increase 1 for each new product. They should be in order like: 1, 2, 3, ...
                product_no = (
                    int(latest_aircraft_production.product_no) + i + 1
                    if latest_aircraft_production is not None
                    else i + 1
                )
                # Generate model for production table
                new_aircraft_production = Aircraft_production.objects.create(
                    product_no=product_no,
                    aircraft_id=produce_aircraft_id,
                    user_id=user_id,
                )

                # Set used parts as many to many relational
                for used_part in parts:
                    new_aircraft_production.used_parts.add(used_part)
                    part_stock = Part_stock.objects.filter(part_id=used_part.id).first()

                    # Decrease the stocks 1 by 1 to log each process specially
                    if part_stock is not None:
                        part_stock.count -= 1
                        part_stock.save()

                        new_part_stock_mobility = Part_stock_mobility.objects.create(
                            aircraft_production_id=new_aircraft_production.id,
                            part_id=used_part.id,
                            status_id=decrease_stock_status.id,
                            # Create a description manually to describe the process
                            description=f"1 {used_part.name} has used for assemblying the {produced_aircraft.name}(No: {product_no})",
                            user_id=user_id,
                        )

                        # Decrease the part stock and log the stock processes
                        new_part_stock_mobility.save()

                # Save aircraft production data
                new_aircraft_production.save()
        except Exception as error:
            print("An error occurred while assemblying an aircraft", error)

        return redirect("/aircrafts/")

    def update_aircraft_production_status(self, request):
        aircraft_production_id = request.POST.get("aircraft_production_id")
        status = request.POST.get("status")

        aircraft_production = Aircraft_production.objects.filter(
            id=aircraft_production_id
        ).first()
        # Edit production's status according to the user's action
        if status == Completed:
            aircraft_production.is_completed = True
        elif status == Canceled:
            increase_stock_status = getStockPartStatus()
            user_id = request.session["user_id"]

            # The process is canceled, So the parts that were planned to be used should be added back to the stock
            used_parts = aircraft_production.used_parts.all()
            for used_part in used_parts:
                part_stock = Part_stock.objects.filter(part_id=used_part.id).first()
                # Increase stock count for the related part
                part_stock.count += 1
                # Update stock count
                part_stock.save()

                # Create a description manually to describe the cancel process
                description = f"1 {used_part.name} is re-added to the stock cause the {aircraft_production.aircraft.name} (No: {aircraft_production.product_no}) aircraft production is canceled."

                # Create a new mobility data in DB to log this stock process
                new_part_stock_mobility = Part_stock_mobility.objects.create(
                    aircraft_production_id=aircraft_production_id,
                    part_id=used_part.id,
                    # Stock will be increased since the parts will come back to the stock
                    status_id=increase_stock_status.id,
                    description=description,
                    user_id=user_id,
                )

                # Save new stock mobility data
                new_part_stock_mobility.save()

            # As final, update aircraft production's status to mention it's canceled
            aircraft_production.is_canceled = True
        else:
            return redirect("/aircrafts/")

        # Save latest updates and reload the window
        aircraft_production.save()

        return redirect("/aircrafts/")


class AircraftListView(ServerSideDatatableView):
    queryset = Aircraft.objects.filter(is_active=True).order_by("name")
    columns = ["name", "description"]


class AircraftProductionListView(ServerSideDatatableView):
    queryset = Aircraft_production.objects.filter(
        Q(is_completed=True) | Q(is_canceled=True)
    ).order_by("product_no")
    columns = [
        "product_no",
        "aircraft__name",
        "user__name",
        "created_at",
        "updated_at",
        "is_completed",
    ]
