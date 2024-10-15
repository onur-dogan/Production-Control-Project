from django.shortcuts import render, redirect
from django.views import View
from ..models import Part_stock, User, Part_stock_mobility
from common.constants import Add_to_stock_process_type, Remove_from_stock_process_type
from common.utils import getStockPartStatus
from django_serverside_datatable.views import ServerSideDatatableView


class Parts(View):
    def get(self, request):
        user_id = request.session["user_id"]
        # If the user session is ended, then the user should log in again
        if user_id is None:
            return redirect("/login/")

        user = User.objects.filter(id=user_id).first()
        # If the user information doesn't exist in DB, then go to the login page to check user data again
        if user is None:
            request.session["user_id"] = None
            return redirect("/login")

        # Retrieve only the parts that the user can update stock information on it
        available_parts_with_stocks = Part_stock.objects.filter(
            part__team_id=user.team_id
        ).order_by("part__name")

        data = {
            "available_parts_with_stocks": available_parts_with_stocks,
            "has_assemble_permission": user.team.has_assemble_permission,
        }
        return render(request, "parts/index.html", data)

    def post(self, request):
        part_stock_id = request.POST.get("part_stock_id")
        part_stock = Part_stock.objects.filter(id=part_stock_id).first()
        # If the part doesn't exist on DB
        if part_stock is None:
            return redirect("/parts/")

        status = None
        description = ""
        try:
            # Check stock process type. It can be add or rermove
            stock_process_type = request.POST.get("stock_process_type")
            # If the process type is add, then add parts to the stocks by added amount
            if stock_process_type == Add_to_stock_process_type:
                amount_added = request.POST.get("amount_added")
                part_stock.count += int(amount_added) or 0

                # Retrieve stock increase status since a new parts are inserted to the stocks
                status = getStockPartStatus(True)

                # Define a description to describe the process
                description = (
                    f"{amount_added} {part_stock.part.name} added to the stocks"
                )
            # If process type is remove, then remove the parts from the stocks by amount
            elif stock_process_type == Remove_from_stock_process_type:
                amount_removed = request.POST.get("amount_removed")
                part_stock.count -= int(amount_removed) or 0
                # Stock count can't be lower than 0
                if part_stock.count < 0:
                    part_stock.count = 0

                # Retrieve stock decrease status since a new parts are inserted to the stocks
                status = getStockPartStatus(False)

                # Define a description to describe the process
                description = (
                    f"{amount_removed} {part_stock.part.name} removed from the stocks"
                )

            part_stock.save()

            # If the status is defined, create a new mobility log in DB
            if status is not None:
                user_id = request.session["user_id"]
                # Add a new log data in stock mobility
                new_part_stock_mobility = Part_stock_mobility.objects.create(
                    part_id=part_stock.part.id,
                    status_id=status.id,
                    # Create a description manually to describe the process
                    description=description,
                    user_id=user_id,
                )

                new_part_stock_mobility.save()
        except Exception as error:
            print("An error occurred while adding/removing a part", error)

        return redirect("/parts/")


class PartListView(ServerSideDatatableView):
    queryset = Part_stock.objects.all()
    columns = ["part__name", "part__description", "part__aircraft__name", "count"]


class PartStockMobilityView(ServerSideDatatableView):
    queryset = Part_stock_mobility.objects.all()
    columns = [
        "id",
        "part__name",
        "description",
        "user__name",
        "status__name",
        "created_at"
    ]
