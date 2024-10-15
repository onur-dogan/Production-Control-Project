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

# The query parameter types to separate the part stock process
# Sends to add parts to the stock
Add_to_stock_process_type = "add_to_stock"
# Sends to remove parts from the stock
Remove_from_stock_process_type = "remove_from_stock"