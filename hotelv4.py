
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date
import uuid


# Rooms information
rooms = {
    101: {"type": "Single Room", "price": 1500, "capacity": 2, "available": True},
    102: {"type": "Single Room", "price": 1500, "capacity": 2, "available": True},
    201: {"type": "Double Room", "price": 2500, "capacity": 4, "available": True},
    202: {"type": "Double Room", "price": 2500, "capacity": 4, "available": True},
    301: {"type": "Deluxe Room", "price": 4000, "capacity": 6, "available": True},
    302: {"type": "Deluxe Room", "price": 4000, "capacity": 6, "available": True}
}

# Stores confirmed reservations
bookings = {}


# Refresh the room table
def refresh_table():

    for row in table.get_children():
        table.delete(row)

    for number in rooms:

        room = rooms[number]

        if room["available"] == True:
            status = "Available"
            guest = ""
        else:
            status = "Booked"
            guest = bookings[number]["guest"]

        table.insert(
            "",
            "end",
            iid=str(number),
            values=(
                number,
                room["type"],
                "₱" + str(room["price"]),
                status,
                guest
            )
        )


# Check if the name contains valid characters
def is_valid_name(name):

    has_letter = False

    for character in name:

        if character.isalpha():
            has_letter = True

        elif character not in " -'.":
            return False

    if has_letter == True:
        return True
    else:
        return False


# Check if the email address is valid
def is_valid_email(email):

    if email == "":
        return True

    if "@" not in email:
        return False

    parts = email.split("@")

    if len(parts) != 2:
        return False

    if parts[0] == "" or parts[1] == "":
        return False

    if "." not in parts[1]:
        return False

    if parts[1].startswith(".") or parts[1].endswith("."):
        return False

    return True


# Open the booking window
def add_booking():

    booking_window = tk.Toplevel(root)
    booking_window.title("New Room Reservation")
    booking_window.geometry("900x800")
    booking_window.minsize(800, 650)
    booking_window.transient(root)

    main_frame = tk.Frame(booking_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=15)

    tk.Label(
        main_frame,
        text="New Room Reservation",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", pady=(0, 5))

    tk.Label(
        main_frame,
        text="Complete the information below to make a reservation.",
        font=("Arial", 10),
        fg="gray"
    ).pack(anchor="w", pady=(0, 12))

    # Buttons at the bottom of the window
    button_frame = tk.Frame(main_frame)
    button_frame.pack(side="bottom", fill="x", pady=10)

    # Create a scrollable form
    content_frame = tk.Frame(main_frame)
    content_frame.pack(side="top", fill="both", expand=True)

    canvas = tk.Canvas(content_frame, highlightthickness=0)

    scrollbar = ttk.Scrollbar(
        content_frame,
        orient="vertical",
        command=canvas.yview
    )

    form_frame = tk.Frame(canvas)

    def update_scroll_region(event):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    form_frame.bind("<Configure>", update_scroll_region)

    canvas_window = canvas.create_window(
        (0, 0),
        window=form_frame,
        anchor="nw"
    )

    def resize_form(event):

        canvas.itemconfig(
            canvas_window,
            width=event.width
        )

    canvas.bind("<Configure>", resize_form)

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Allow scrolling with the mouse wheel
    def scroll_form(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind("<MouseWheel>", scroll_form)

    def close_booking_window():

        booking_window.destroy()

    booking_window.protocol(
        "WM_DELETE_WINDOW",
        close_booking_window
    )

    # Room selection
    tk.Label(
        form_frame,
        text="1. Room Selection",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", pady=(5, 8))

    room_frame = tk.Frame(
        form_frame,
        bd=1,
        relief="solid",
        padx=12,
        pady=10
    )

    room_frame.pack(fill="x", pady=(0, 15))

    available_rooms = []

    for number in rooms:

        if rooms[number]["available"] == True:
            available_rooms.append(number)

    if len(available_rooms) == 0:

        messagebox.showinfo(
            "No Available Rooms",
            "There are currently no available rooms.",
            parent=booking_window
        )

        booking_window.destroy()
        return

    room_values = []

    for number in available_rooms:

        room_name = (
            str(number) + " - " +
            rooms[number]["type"] +
            " (₱" + str(rooms[number]["price"]) + ")"
        )

        room_values.append(room_name)

    room_var = tk.StringVar()

    tk.Label(
        room_frame,
        text="Select Room:"
    ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

    room_combo = ttk.Combobox(
        room_frame,
        textvariable=room_var,
        values=room_values,
        state="readonly",
        width=45
    )

    room_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    room_combo.current(0)

    room_info_label = tk.Label(
        room_frame,
        text="",
        font=("Arial", 9),
        fg="gray"
    )

    room_info_label.grid(
        row=1,
        column=0,
        columnspan=2,
        sticky="w",
        padx=5,
        pady=5
    )

    # Primary booker information
    tk.Label(
        form_frame,
        text="2. Primary Booker Information",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", pady=(5, 8))

    booker_frame = tk.Frame(
        form_frame,
        bd=1,
        relief="solid",
        padx=12,
        pady=10
    )

    booker_frame.pack(fill="x", pady=(0, 15))

    tk.Label(
        booker_frame,
        text="Contact Number:"
    ).grid(row=0, column=0, sticky="w", padx=5, pady=7)

    contact_entry = ttk.Entry(booker_frame, width=45)
    contact_entry.grid(row=0, column=1, sticky="w", padx=5, pady=7)

    tk.Label(
        booker_frame,
        text="Email Address:"
    ).grid(row=1, column=0, sticky="w", padx=5, pady=7)

    email_entry = ttk.Entry(booker_frame, width=45)
    email_entry.grid(row=1, column=1, sticky="w", padx=5, pady=7)

    # Guest information
    tk.Label(
        form_frame,
        text="3. Guest Information",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", pady=(5, 8))

    guest_frame = tk.Frame(
        form_frame,
        bd=1,
        relief="solid",
        padx=12,
        pady=10
    )

    guest_frame.pack(fill="x", pady=(0, 15))

    tk.Label(
        guest_frame,
        text="Number of Guests:"
    ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

    guest_count_var = tk.StringVar()
    guest_count_var.set("1")

    guest_count_combo = ttk.Combobox(
        guest_frame,
        textvariable=guest_count_var,
        state="readonly",
        width=10
    )

    guest_count_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)

    guest_fields_frame = tk.Frame(guest_frame)

    guest_fields_frame.grid(
        row=1,
        column=0,
        columnspan=3,
        sticky="ew",
        pady=10
    )

    guest_entries = []

    # Create input fields for each guest
    def update_guest_fields(event=None):

        previous_data = []

        for guest in guest_entries:

            guest_data = {
                "name": guest["name"].get(),
                "age": guest["age"].get(),
                "pwd": guest["pwd"].get(),
                "senior": guest["senior"].get()
            }

            previous_data.append(guest_data)

        for widget in guest_fields_frame.winfo_children():
            widget.destroy()

        guest_entries.clear()

        count = int(guest_count_var.get())

        for i in range(count):

            guest_number = i + 1

            guest_box = tk.LabelFrame(
                guest_fields_frame,
                text="Guest " + str(guest_number),
                padx=8,
                pady=8
            )

            guest_box.pack(fill="x", pady=5)

            tk.Label(
                guest_box,
                text="Full Name:"
            ).grid(row=0, column=0, sticky="w", padx=5, pady=4)

            name_entry = ttk.Entry(guest_box, width=42)
            name_entry.grid(row=0, column=1, sticky="w", padx=5, pady=4)

            tk.Label(
                guest_box,
                text="Age:"
            ).grid(row=1, column=0, sticky="w", padx=5, pady=4)

            age_entry = ttk.Entry(guest_box, width=15)
            age_entry.grid(row=1, column=1, sticky="w", padx=5, pady=4)

            pwd_var = tk.BooleanVar()

            pwd_check = ttk.Checkbutton(
                guest_box,
                text="Has valid PWD ID",
                variable=pwd_var
            )

            pwd_check.grid(row=2, column=0, sticky="w", padx=5, pady=4)

            senior_var = tk.BooleanVar()

            senior_check = ttk.Checkbutton(
                guest_box,
                text="Has valid Senior Citizen ID",
                variable=senior_var
            )

            senior_check.grid(row=2, column=1, sticky="w", padx=5, pady=4)

            # Restore previously entered information
            if i < len(previous_data):

                name_entry.insert(0, previous_data[i]["name"])
                age_entry.insert(0, previous_data[i]["age"])

                pwd_var.set(previous_data[i]["pwd"])
                senior_var.set(previous_data[i]["senior"])

            guest_data = {
                "name": name_entry,
                "age": age_entry,
                "pwd": pwd_var,
                "senior": senior_var
            }

            guest_entries.append(guest_data)

    # Stay details
    tk.Label(
        form_frame,
        text="4. Stay Details",
        font=("Arial", 12, "bold")
    ).pack(anchor="w", pady=(5, 8))

    stay_frame = tk.Frame(
        form_frame,
        bd=1,
        relief="solid",
        padx=12,
        pady=10
    )

    stay_frame.pack(fill="x", pady=(0, 15))

    tk.Label(
        stay_frame,
        text="Check-in Date (YYYY-MM-DD):"
    ).grid(row=0, column=0, sticky="w", padx=5, pady=7)

    checkin_entry = ttk.Entry(stay_frame, width=30)
    checkin_entry.grid(row=0, column=1, sticky="w", padx=5, pady=7)

    tk.Label(
        stay_frame,
        text="Check-out Date (YYYY-MM-DD):"
    ).grid(row=1, column=0, sticky="w", padx=5, pady=7)

    checkout_entry = ttk.Entry(stay_frame, width=30)
    checkout_entry.grid(row=1, column=1, sticky="w", padx=5, pady=7)

    tk.Label(
        stay_frame,
        text="Special Requests:"
    ).grid(row=2, column=0, sticky="nw", padx=5, pady=7)

    special_entry = tk.Text(stay_frame, width=45, height=4)
    special_entry.grid(row=2, column=1, sticky="w", padx=5, pady=7)

    # Display the estimated total
    total_frame = tk.Frame(
        form_frame,
        bd=1,
        relief="solid",
        padx=12,
        pady=10
    )

    total_frame.pack(fill="x", pady=(0, 15))

    tk.Label(
        total_frame,
        text="Estimated Total:",
        font=("Arial", 11, "bold")
    ).pack(side="left")

    total_label = tk.Label(
        total_frame,
        text="₱0.00",
        font=("Arial", 12, "bold"),
        fg="#27834A"
    )

    total_label.pack(side="right")

    # Get the selected room number
    def get_selected_room():

        selected_text = room_var.get()
        parts = selected_text.split(" - ")

        number = int(parts[0])

        return number

    # Calculate the estimated room cost
    def update_estimate(event=None):

        number = get_selected_room()

        check_in_text = checkin_entry.get().strip()
        check_out_text = checkout_entry.get().strip()

        try:

            check_in = datetime.strptime(
                check_in_text,
                "%Y-%m-%d"
            ).date()

            check_out = datetime.strptime(
                check_out_text,
                "%Y-%m-%d"
            ).date()

            date_difference = check_out - check_in
            nights = date_difference.days

            if nights > 0:

                room_price = rooms[number]["price"]
                total = room_price * nights

                total_label.config(
                    text="₱" + format(total, ",.2f")
                )

            else:

                total_label.config(text="₱0.00")

        except ValueError:

            total_label.config(text="₱0.00")

    # Update room details when another room is selected
    def update_room_info(event=None):

        number = get_selected_room()

        room = rooms[number]

        capacity = room["capacity"]
        price = room["price"]

        room_info_label.config(
            text=(
                "Maximum Capacity: " + str(capacity) +
                " guests     |     Price per Night: ₱" +
                format(price, ",")
            )
        )

        guest_choices = []

        for i in range(1, capacity + 1):
            guest_choices.append(str(i))

        guest_count_combo["values"] = guest_choices

        if int(guest_count_var.get()) > capacity:
            guest_count_var.set("1")

        update_guest_fields()
        update_estimate()

    room_combo.bind(
        "<<ComboboxSelected>>",
        update_room_info
    )

    guest_count_combo.bind(
        "<<ComboboxSelected>>",
        update_guest_fields
    )

    checkin_entry.bind(
        "<KeyRelease>",
        update_estimate
    )

    checkout_entry.bind(
        "<KeyRelease>",
        update_estimate
    )

    update_room_info()

    # Check the information before confirming
    def review_booking():

        number = get_selected_room()

        if rooms[number]["available"] == False:

            messagebox.showerror(
                "Room Unavailable",
                "This room is no longer available.",
                parent=booking_window
            )

            return

        # Validate contact number
        contact = contact_entry.get().strip()

        if not contact.isdigit() or len(contact) < 10 or len(contact) > 15:

            messagebox.showerror(
                "Invalid Contact Number",
                "Please enter a contact number containing 10 to 15 digits.",
                parent=booking_window
            )

            contact_entry.focus_set()
            return

        # Validate email address
        email = email_entry.get().strip()

        if is_valid_email(email) == False:

            messagebox.showerror(
                "Invalid Email Address",
                "Please enter a valid email address or leave it blank.",
                parent=booking_window
            )

            email_entry.focus_set()
            return

        total_guests = int(guest_count_var.get())
        capacity = rooms[number]["capacity"]

        if total_guests < 1 or total_guests > capacity:

            messagebox.showerror(
                "Invalid Guest Count",
                "The number of guests exceeds the room capacity.",
                parent=booking_window
            )

            return

        # Validate each guest
        guests = []

        for i in range(total_guests):

            guest = guest_entries[i]

            name = guest["name"].get().strip()
            age_text = guest["age"].get().strip()

            if is_valid_name(name) == False:

                messagebox.showerror(
                    "Invalid Guest Name",
                    "Please enter a valid name for Guest " + str(i + 1) + ".",
                    parent=booking_window
                )

                guest["name"].focus_set()
                return

            try:

                age = int(age_text)

                if age < 0:
                    raise ValueError

            except ValueError:

                messagebox.showerror(
                    "Invalid Guest Age",
                    "Please enter a valid age for Guest " + str(i + 1) + ".",
                    parent=booking_window
                )

                guest["age"].focus_set()
                return

            guest_information = {
                "name": name,
                "age": age,
                "pwd": guest["pwd"].get(),
                "senior": False
            }

            if age >= 60:
                guest_information["senior"] = guest["senior"].get()

            guests.append(guest_information)

        # Validate check-in date
        check_in_text = checkin_entry.get().strip()

        try:

            check_in = datetime.strptime(
                check_in_text,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            messagebox.showerror(
                "Invalid Check-in Date",
                "Please enter a valid date using YYYY-MM-DD.",
                parent=booking_window
            )

            checkin_entry.focus_set()
            return

        if check_in < date.today():

            messagebox.showerror(
                "Invalid Check-in Date",
                "The check-in date cannot be in the past.",
                parent=booking_window
            )

            checkin_entry.focus_set()
            return

        # Validate check-out date
        check_out_text = checkout_entry.get().strip()

        try:

            check_out = datetime.strptime(
                check_out_text,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            messagebox.showerror(
                "Invalid Check-out Date",
                "Please enter a valid date using YYYY-MM-DD.",
                parent=booking_window
            )

            checkout_entry.focus_set()
            return

        if check_out <= check_in:

            messagebox.showerror(
                "Invalid Check-out Date",
                "The check-out date must be later than the check-in date.",
                parent=booking_window
            )

            checkout_entry.focus_set()
            return

        # Calculate the total cost
        date_difference = check_out - check_in
        nights = date_difference.days

        room_price = rooms[number]["price"]
        total = room_price * nights

        special_requests = special_entry.get(
            "1.0",
            "end"
        ).strip()

        # Generate a booking reference
        reference = "OCC-" + uuid.uuid4().hex[:8].upper()

        primary_booker = guests[0]["name"]

        # Store the reservation information
        booking_data = {
            "guest": primary_booker,
            "contact": contact,
            "email": email,
            "guests": guests,
            "total_guests": total_guests,
            "reference": reference,
            "nights": nights,
            "check_in": str(check_in),
            "check_out": str(check_out),
            "total": total,
            "special_requests": special_requests,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        show_booking_review(
            booking_window,
            number,
            booking_data
        )

    # Buttons at the bottom of the booking window
    tk.Button(
        button_frame,
        text="Cancel",
        width=15,
        command=close_booking_window
    ).pack(side="left", padx=5)

    tk.Button(
        button_frame,
        text="Review Booking",
        width=18,
        bg="#4CAF50",
        fg="white",
        command=review_booking
    ).pack(side="right", padx=5)


# Display the reservation summary
def show_booking_review(parent, number, info):

    review_window = tk.Toplevel(parent)
    review_window.title("Review Reservation")
    review_window.geometry("600x700")
    review_window.minsize(500, 550)
    review_window.transient(parent)

    frame = tk.Frame(review_window, padx=20, pady=15)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text="Reservation Summary",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", pady=(0, 12))

    summary_frame = tk.Frame(
        frame,
        bd=1,
        relief="solid",
        padx=12,
        pady=12
    )

    summary_frame.pack(fill="both", expand=True)

    text_box = tk.Text(
        summary_frame,
        wrap="word",
        font=("Arial", 10)
    )

    text_box.pack(fill="both", expand=True)

    room = rooms[number]

    summary = (
        "BOOKING INFORMATION\n"
        "----------------------------------------\n"
        "Booking Reference: " + info["reference"] + "\n"
        "Primary Booker: " + info["guest"] + "\n"
        "Contact Number: " + info["contact"] + "\n"
        "Email Address: " + (info["email"] if info["email"] else "Not provided") + "\n\n"

        "ROOM INFORMATION\n"
        "----------------------------------------\n"
        "Room Number: " + str(number) + "\n"
        "Room Type: " + room["type"] + "\n"
        "Maximum Capacity: " + str(room["capacity"]) + " guests\n"
        "Number of Guests: " + str(info["total_guests"]) + "\n\n"

        "GUEST DETAILS\n"
        "----------------------------------------\n"
    )

    guest_number = 1

    for guest in info["guests"]:

        summary += (
            "Guest " + str(guest_number) + ": " + guest["name"] + "\n"
            "Age: " + str(guest["age"]) + "\n"
            "PWD ID Declared: " + ("Yes" if guest["pwd"] else "No") + "\n"
            "Senior Citizen ID Declared: " + ("Yes" if guest["senior"] else "No") + "\n\n"
        )

        guest_number += 1

    summary += (
        "STAY INFORMATION\n"
        "----------------------------------------\n"
        "Check-in Date: " + info["check_in"] + "\n"
        "Check-out Date: " + info["check_out"] + "\n"
        "Number of Nights: " + str(info["nights"]) + "\n\n"

        "PAYMENT INFORMATION\n"
        "----------------------------------------\n"
        "Price per Night: ₱" + format(room["price"], ",") + "\n"
        "Total Room Cost: ₱" + format(info["total"], ",") + "\n\n"

        "SPECIAL REQUESTS\n"
        "----------------------------------------\n"
        + (info["special_requests"] if info["special_requests"] else "None") + "\n\n"

        "Note: PWD and Senior Citizen benefits are subject to "
        "valid ID verification and applicable hotel policies.\n"
    )

    text_box.insert("1.0", summary)
    text_box.config(state="disabled")

    # Save the reservation after confirmation
    def confirm_booking():

        if rooms[number]["available"] == False:

            messagebox.showerror(
                "Room Unavailable",
                "This room is no longer available.",
                parent=review_window
            )

            review_window.destroy()
            return

        bookings[number] = info
        rooms[number]["available"] = False

        refresh_table()

        review_window.destroy()
        parent.destroy()

        messagebox.showinfo(
            "Booking Successful",
            "The reservation has been successfully confirmed.\n\n"
            "Booking Reference: " + info["reference"],
            parent=root
        )

    buttons = tk.Frame(frame)
    buttons.pack(fill="x", pady=12)

    tk.Button(
        buttons,
        text="Back",
        width=15,
        command=review_window.destroy
    ).pack(side="left", padx=5)

    tk.Button(
        buttons,
        text="Confirm Booking",
        width=18,
        bg="#4CAF50",
        fg="white",
        command=confirm_booking
    ).pack(side="right", padx=5)


# Search for reservations
def view_search_reservations():

    search = simpledialog.askstring(
        "Search Reservations",
        "Please enter a guest name, room number, or booking reference:",
        parent=root
    )

    if search is None:
        return

    search = search.strip().lower()

    if search == "":

        messagebox.showwarning(
            "Empty Search",
            "Please enter the requested search information."
        )

        return

    results = []

    for number in bookings:

        info = bookings[number]
        match = False

        if search in info["guest"].lower():
            match = True

        if search == str(number):
            match = True

        if search in info["reference"].lower():
            match = True

        for guest in info["guests"]:

            if search in guest["name"].lower():
                match = True

        if match == True:
            results.append(number)

    if len(results) == 0:

        messagebox.showinfo(
            "No Reservations Found",
            "No reservations match the provided search information."
        )

        return

    result_text = "MATCHING RESERVATIONS\n\n"

    for number in results:

        info = bookings[number]

        result_text += (
            "Booking Reference: " + info["reference"] + "\n"
            "Primary Booker: " + info["guest"] + "\n"
            "Contact Number: " + info["contact"] + "\n"
            "Email: " + (info["email"] if info["email"] else "Not provided") + "\n\n"

            "Room Number: " + str(number) + "\n"
            "Room Type: " + rooms[number]["type"] + "\n"
            "Number of Guests: " + str(info["total_guests"]) + "\n"
        )

        guest_number = 1

        for guest in info["guests"]:

            result_text += (
                "\nGuest " + str(guest_number) + ": " + guest["name"] + "\n"
                "Age: " + str(guest["age"]) + "\n"
                "PWD ID Declared: " + ("Yes" if guest["pwd"] else "No") + "\n"
                "Senior Citizen ID Declared: " + ("Yes" if guest["senior"] else "No") + "\n"
            )

            guest_number += 1

        result_text += (
            "\nCheck-in: " + info["check_in"] + "\n"
            "Check-out: " + info["check_out"] + "\n"
            "Number of Nights: " + str(info["nights"]) + "\n"
            "Total: ₱" + format(info["total"], ",") + "\n"
            "Special Requests: " +
            (info["special_requests"] if info["special_requests"] else "None") + "\n"
            "Booking Date: " + info["date"] + "\n"
            "-------------------------------------\n\n"
        )

    # Display the search results
    result_window = tk.Toplevel(root)
    result_window.title("Reservation Details")
    result_window.geometry("650x650")

    result_frame = tk.Frame(result_window, padx=15, pady=15)
    result_frame.pack(fill="both", expand=True)

    tk.Label(
        result_frame,
        text="Reservation Details",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", pady=(0, 10))

    result_box = tk.Text(
        result_frame,
        wrap="word",
        font=("Arial", 10)
    )

    result_box.pack(fill="both", expand=True)

    result_box.insert("1.0", result_text)
    result_box.config(state="disabled")


# Main application window
root = tk.Tk()

root.title("Hotel Reservation System")
root.geometry("700x420")

title = tk.Label(
    root,
    text="Hotel Reservation System",
    font=("Arial", 18, "bold")
)

title.pack(pady=10)

tip = tk.Label(
    root,
    text="Click a room, then press a button below."
)

tip.pack()

# Room table
columns = (
    "Room",
    "Type",
    "Price",
    "Status",
    "Guest"
)

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=8
)

for col in columns:

    table.heading(col, text=col)
    table.column(col, width=120, anchor="center")

table.pack(padx=15, pady=10, fill="x")

# Main buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Add Booking",
    width=15,
    bg="#4CAF50",
    fg="white",
    command=add_booking
).grid(row=0, column=0, padx=8)

tk.Button(
    button_frame,
    text="Search Reservations",
    width=15,
    bg="#2196F3",
    fg="white",
    command=view_search_reservations
).grid(row=0, column=1, padx=8)

tk.Button(
    button_frame,
    text="Exit",
    width=15,
    command=root.destroy
).grid(row=0, column=2, padx=8)

# Display the rooms
refresh_table()

# Run the application
root.mainloop()