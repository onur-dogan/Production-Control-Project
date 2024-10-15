# Database table/model name constants
Team = "Team"
User = "User"
Aircraft = "Aircraft"
Part = "Part"
Part_stock = "Part_stock"
Part_stock_status = "Part_stock_status"
Part_stock_mobility = "Part_stock_mobility"
Aircraft_production = "Aircraft_production"

# Name constants of the aircraft models
Aircrafts = ["TB2", "TB3", "AKINCI", "KIZILELMA"]
# Name constants of the part models
Parts = ["Wing", "Fuselage", "Tail", "Avionics"]
# Part stock status constants
Part_stock_statuses = ["Stock Increase", "Stock Decrease"]

# The query parameters that are used in login page to show warning message to the user
# Recaptcha warning query parameter to show warning message if the user doesn't click on it
Wrong_recaptcha_query_parameter = "wrong_recaptcha"
# Information warning query parameter to show warning message it the user's informations don't correct
Wrong_info_query_parameter = "wrong_info"

# The query parameter types to separate the part stock processes
# Uses to add parts to the stock
Add_to_stock_process_type = "add_to_stock"
# Uses to remove parts from the stock
Remove_from_stock_process_type = "remove_from_stock"

# The query parameter types to separate aircraft processes
# Uses to assembly a new aircraft
Assembly_aircraft = "assembly_aircraft"
# Uses to update aircraft production's status
Update_aircraft_production_status = "update_aircraft_production_status"

# Aircraft production statuses 
# Use for the completed processes status
Completed = "completed"
# Use for the canceled processes status
Canceled = "canceled"

# Part stock mobility statuses
# Use for mentioning that new parts were added to the stock 
Increase = "increase"  
# Use for mentioning that some parts were removed from the stock
Decrease = "decrease"
