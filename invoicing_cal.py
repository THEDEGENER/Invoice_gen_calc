from tkinter import *
from tkinter import ttk
 

def calculate(*args):
    try:
        # converts StringVar to int/float
        days_worked_value = int(days_worked.get())
        hours_per_shift_value = int(hours_per_shift.get())
        hourly_rate_value = float(hourly_rate.get())
        commission_rate_value = float(commission_rate.get())
        total_sales_value = float(total_sales.get())

        total_hours = days_worked_value * hours_per_shift_value
        total_hourly_pay = total_hours * hourly_rate_value
        commission_percent = commission_rate_value / 100
        total_commission = total_sales_value * commission_percent
        total_payment = total_hourly_pay + total_commission
        total_pay.set(f"{total_payment:.2f}")

    except ValueError:
        total_pay.set("Invalid Input")
   
root = Tk()
root.title("Calculate Payment Amounts")

# configures mainframe and grid
mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
total_pay = StringVar()

# dynamic label
ttk.Label(mainframe, textvariable=total_pay).grid(column=2, row=7, sticky=(W, E))
          
# static labels
ttk.Label(mainframe, text="Input This Weeks Earnings").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Days Worked:").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Hours Per Shift:").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="Hourly Rate:").grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, text="Commision Rate:").grid(column=1, row=5, sticky=W)
ttk.Label(mainframe, text="Total Sales:").grid(column=1, row=6, sticky=W)
ttk.Label(mainframe, text="total Pay:").grid(column=1, row=7, sticky=W)



# input the days worked
days_worked = StringVar()
days_worked_entry = ttk.Entry(mainframe, width=7, textvariable=days_worked)
days_worked_entry.grid(column=2, row=2, sticky=(W, E))

# input hours per shift
hours_per_shift = StringVar()
hours_per_shift_entry = ttk.Entry(mainframe, width=7, textvariable=hours_per_shift)
hours_per_shift_entry.grid(column=2, row=3, sticky=((W, E)))

# input hourly rate
hourly_rate = StringVar()
hourly_rate_entry = ttk.Entry(mainframe, width=7, textvariable=hourly_rate)
hourly_rate_entry.grid(column=2, row=4, sticky=((W, E)))

# input commission rate
commission_rate = StringVar()
commission_rate_entry = ttk.Entry(mainframe, width=7, textvariable=commission_rate)
commission_rate_entry.grid(column=2, row=5, sticky=((W, E)))

# input total sales
total_sales = StringVar()
total_sales_entry = ttk.Entry(mainframe, width=7, textvariable=total_sales)
total_sales_entry.grid(column=2, row=6, sticky=((W, E)))

# calculate button 
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=7, sticky=E)

# adds padding to widgets
for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

days_worked_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()

