# tracker/admin.py

from django.contrib import admin
from .models import Expense
# Note: Since your views use ExpenseForm, there's no direct need to import it here.
# The core task is to register the model(s).

## Optional: Create a custom ModelAdmin for better display
class ExpenseAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('date', 'category', 'description', 'amount')

    # Fields to filter the list view by
    list_filter = ('category', 'date')

    # Fields to use for searching
    search_fields = ('description', 'category')

    # Order the list by date in descending order by default
    ordering = ('-date',)
    
    # Make the date field a date hierarchy for navigation
    date_hierarchy = 'date'


## Register your model with the admin site
# Use the custom admin class for better presentation
admin.site.register(Expense, ExpenseAdmin)

# You can also customize the Admin Site Headers
admin.site.site_header = "Expense Tracker Admin"
admin.site.site_title = "Expense Tracker Portal"
admin.site.index_title = "Welcome to the Expense Tracker Administration"