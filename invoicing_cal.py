from tkinter import *
from tkinter import ttk
from fpdf import FPDF
import datetime

# Define the PDF class
class PDF(FPDF):
    def __init__(self, worker_name, date_generated, total_payment):
        super().__init__()  
        self.worker_name = worker_name
        self.date_generated = date_generated
        self.total_payment = total_payment

    def header(self):
        self.set_font('helvetica', style='B', size=15)
        self.cell(0, 10, "Weekly Pay Invoice", ln=True, align="C")
        self.ln(10)  

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', style='I', size=8)
        self.cell(0, 10, "Amy and Alex Group PTY LTD", align='C')

    def invoice_chapter_title(self):
        self.set_font('helvetica', size=12)
        self.cell(
            0,
            10,
            f'Weekly invoice for {self.worker_name} : Generated on {self.date_generated}',
            ln=True,
            align='L',
        )
        self.ln(5)  

    def chapter_body(self):
        self.set_font('helvetica', size=12)
        self.cell(0, 10, f'This pay cycle you earned ${self.total_payment}, thank you for your hard work.', ln=True, align='L')

    def print_chapter(self):
        self.add_page()
        self.invoice_chapter_title()
        self.chapter_body()


class ButtonPress:
    def __init__(self, days_worked, hours_per_shift, hourly_rate, commission_rate, total_sales, total_pay, worker_name):
        self.days_worked = days_worked
        self.hours_per_shift = hours_per_shift
        self.hourly_rate = hourly_rate
        self.commission_rate = commission_rate
        self.total_sales = total_sales
        self.total_pay = total_pay
        self.worker_name = worker_name
        self.date_generated = None  

    def calculate(self, *args):
        try:
            # Convert StringVar to int/float
            days_worked_value = int(self.days_worked.get())
            hours_per_shift_value = int(self.hours_per_shift.get())
            hourly_rate_value = float(self.hourly_rate.get())
            commission_rate_value = float(self.commission_rate.get())
            total_sales_value = float(self.total_sales.get())

            # Perform calculations
            total_hours = days_worked_value * hours_per_shift_value
            total_hourly_pay = total_hours * hourly_rate_value
            commission_percent = commission_rate_value / 100
            total_commission = total_sales_value * commission_percent
            total_payment = total_hourly_pay + total_commission

            # Set the result
            self.total_pay.set(f"{total_payment:.2f}")

            return True  # Indicate successful calculation

        except ValueError:
            self.total_pay.set("Invalid Input")
            return False  # Indicate calculation failure

    def time_at_press(self):
        # Capture the current date and time
        self.date_generated = datetime.datetime.now()

    def generate_pdf(self):
        self.time_at_press()
        date_generated_str = self.date_generated.strftime("%Y-%m-%d %H:%M:%S")

        # Retrieve worker's name from StringVar
        name = self.worker_name.get()

        # Retrieve total payment
        total_payment = self.total_pay.get()

        # Validate total_payment
        try:
            total_payment_float = float(total_payment)
            total_payment_str = f"{total_payment_float:.2f}"
        except ValueError:
            total_payment_str = "Invalid Payment"

        # Create the PDF instance with dynamic data
        pdf = PDF(name, date_generated_str, total_payment_str)
        pdf.print_chapter()

        # Save the PDF
        pdf.output(f'/Users/amyalex/Desktop/Projects/invoicing_calculator/invoices/invoicing:{name}:{date_generated_str}.pdf')
        print(f"PDF Generated for {name} on {date_generated_str}")

    def calculate_and_generate_pdf(self, *args):
        
        success = self.calculate()
        if success:
            
            self.generate_pdf()
        else:
            print("Calculation failed. PDF not generated.")


def main():
    root = Tk()
    root.title("Calculate Payment Amounts")

    # Configure mainframe and grid
    mainframe = ttk.Frame(root, padding='10 10 10 10')
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    total_pay = StringVar()

    # Define StringVars
    worker_name = StringVar()
    days_worked = StringVar()
    hours_per_shift = StringVar()
    hourly_rate = StringVar()
    commission_rate = StringVar()
    total_sales = StringVar()

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

    # Create an instance of ButtonPress
    calc = ButtonPress(
        days_worked=days_worked,
        hours_per_shift=hours_per_shift,
        hourly_rate=hourly_rate,
        commission_rate=commission_rate,
        total_sales=total_sales,
        total_pay=total_pay,
        worker_name=worker_name
    )

    # Create Calculate & Generate PDF button
    ttk.Button(mainframe, text="Calculate & Generate PDF", command=calc.calculate_and_generate_pdf).grid(column=1, row=9, columnspan=2, pady=10)

    # Add padding to all child widgets
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # Set focus to the first entry widget
    days_worked_entry = mainframe.grid_slaves(row=3, column=2)[0]
    days_worked_entry.focus()

    # Bind the Return key to the calculate_and_generate_pdf method
    root.bind("<Return>", lambda event: calc.calculate_and_generate_pdf())

    root.mainloop()

if __name__ == "__main__":
    main()
