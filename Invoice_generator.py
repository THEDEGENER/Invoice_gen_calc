from tkinter import *
from tkinter import ttk
from weasyprint import HTML
import datetime as dt
from html_str import gen_html


def main():
    root = Tk()
    root.title("Calculate Payment Amounts")

    # Configure mainframe and grid
    mainframe = ttk.Frame(root, padding='10 10 10 10')
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    total_pay = IntVar()

    # Define StringVars
    worker_name = StringVar()
    days_worked = IntVar()
    hours_per_shift = IntVar()
    hourly_rate = IntVar()
    commission_rate = IntVar()
    total_sales = IntVar()

    # Input widgets
    ttk.Label(mainframe, text="Input This Week's Earnings").grid(column=1, row=1, columnspan=2, sticky=W, pady=(0, 10))

    ttk.Label(mainframe, text='Worker\'s Name:').grid(column=1, row=2, sticky=W, pady=5)
    ttk.Entry(mainframe, width=25, textvariable=worker_name).grid(column=2, row=2, sticky=(W, E), pady=5)

    ttk.Label(mainframe, text="Days Worked:").grid(column=1, row=3, sticky=W, pady=5)
    ttk.Entry(mainframe, width=25, textvariable=days_worked).grid(column=2, row=3, sticky=(W, E), pady=5)

    ttk.Label(mainframe, text="Hours Per Shift:").grid(column=1, row=4, sticky=W, pady=5)
    ttk.Entry(mainframe, width=25, textvariable=hours_per_shift).grid(column=2, row=4, sticky=(W, E), pady=5)

    ttk.Label(mainframe, text="Hourly Rate:").grid(column=1, row=5, sticky=W, pady=5)
    ttk.Entry(mainframe, width=25, textvariable=hourly_rate).grid(column=2, row=5, sticky=(W, E), pady=5)

    ttk.Label(mainframe, text="Commission Rate (%):").grid(column=1, row=6, sticky=W, pady=5)
    ttk.Entry(mainframe, width=25, textvariable=commission_rate).grid(column=2, row=6, sticky=(W, E), pady=5)

    ttk.Label(mainframe, text="Total Sales:").grid(column=1, row=7, sticky=W, pady=5)
    ttk.Entry(mainframe, width=25, textvariable=total_sales).grid(column=2, row=7, sticky=(W, E), pady=5)

    ttk.Label(mainframe, text="Total Pay:").grid(column=1, row=8, sticky=W, pady=5)
    ttk.Entry(mainframe, width=25, textvariable=total_pay, state='readonly').grid(column=2, row=8, sticky=(W, E), pady=5)

    def get_invoice_number():
        with open('invoice_number.txt') as file:
            invoice_number = file.read().strip()
            return invoice_number
        
        
    def update_invoice_number():
        with open('invoice_number.txt') as file:
            content = file.read().strip()
            number = int(content)

        number += 1

        with open('invoice_number.txt', 'w') as file:
            file.write(str(number))

    def calculate():
        try:
            # Convert StringVar to int/float
            days_worked_value = int(days_worked.get())
            hours_per_shift_value = int(hours_per_shift.get())
            hourly_rate_value = float(hourly_rate.get())
            commission_rate_value = float(commission_rate.get())
            total_sales_value = float(total_sales.get())
            # Perform calculations
            total_hours = days_worked_value * hours_per_shift_value
            total_hourly_pay = total_hours * hourly_rate_value
            commission_percent = commission_rate_value / 100
            total_commission = total_sales_value * commission_percent
            total_payment = total_hourly_pay + total_commission
            # Set the result
            total_pay.set(f"{total_payment:.2f}")
            return True, total_hours, total_payment  # Indicate successful calculation
        except ValueError:
            total_pay.set("Invalid Input")
            return False  # Indicate calculation failure
        
    def cal_and_pdf():
        # get the current time when the program executes
        date_generated = dt.datetime.now()
        date_generated_str = date_generated.strftime("%Y-%m-%d %H:%M:%S")

        name = worker_name.get()

        invoice_number = get_invoice_number()

        # if successful calculation then execute gen_html
        success, total_hours, total_payment = calculate()
        if success:
            gen_html(invoice_number, date_generated_str, name, total_hours, total_payment)
            update_invoice_number()
        else:
            print('Calculation Failed. PDF not generated.')

    # Create Calculate & Generate PDF button
    ttk.Button(mainframe, text="Calculate & Generate PDF", command=cal_and_pdf).grid(column=1, row=9, columnspan=2, pady=10)

    # Add padding to all child widgets
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Set focus to the first entry widget
    days_worked_entry = mainframe.grid_slaves(row=3, column=2)[0]
    days_worked_entry.focus()

    # Bind the Return key to the calculate_and_generate_pdf method
    root.bind("<Return>", lambda event: cal_and_pdf)

    root.mainloop()

if __name__ == '__main__':
    main()
    
