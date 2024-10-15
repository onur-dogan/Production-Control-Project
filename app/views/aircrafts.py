from django.shortcuts import render, redirect
from django.views import View
from ..models import (
    Aircraft,
    Aircraft_production,
    Part,
    Part_stock,
    Part_stock_mobility,
    Part_stock_status,
    User,
)
from django_serverside_datatable.views import ServerSideDatatableView


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
        }

        return render(request, "aircrafts/index.html", data)

    def post(self, request):
        user_id = request.session["user_id"]
        produce_aircraft_id = request.POST.get("produce_aircraft_id")
        amount_to_produce_aircraft = request.POST.get("amount_to_produce_aircraft")

        latest_aircraft_production = Aircraft_production.objects.last()
        # Set the latest product no to the aircraft.
        # Quick Note: product no can be defined as a string if any string would be used in it
        parts = Part.objects.filter(aircraft_id=produce_aircraft_id)
        # Retrieeve the related aircraft
        produced_aircraft = Aircraft.objects.filter(id=produce_aircraft_id).first()
        # Retrieve stock decrease status to use in mobility table
        decrease_stock_status = Part_stock_status.objects.filter(
            name__icontains="decrease"
        ).first()

        try:
            for i in range(0, int(amount_to_produce_aircraft)):
                # Increase 1 for each new product. They should be in order like: 1, 2, 3, ...
                product_no = (
                    int(latest_aircraft_production.product_no) + i
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
                            user_id=user_id
                        )

                        # Decrease the part stock and log the stock processes
                        new_part_stock_mobility.save()

                # Save aircraft production data
                new_aircraft_production.save()
        except Exception as error:
            print("An error occurred while assemblying an aircraft", error)

        return redirect("/aircrafts/")


class AircraftListView(ServerSideDatatableView):
    queryset = Aircraft.objects.filter(is_active=True).order_by("name")
    columns = ["name", "description"]


class AircraftProductionListView(ServerSideDatatableView):
    queryset = Aircraft_production.objects.all().order_by("updated_at")
    columns = [
        "product_no",
        "aircraft__name",
        "used_parts",
        "is_completed",
        "user__name",
    ]
