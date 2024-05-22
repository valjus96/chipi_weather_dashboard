#ChiPi Weather Dashboard
#By valjus96, (https://github.com/valjus96)

#setup window/initializing the software
import customtkinter
import gui

def main():
    #if setup.dat is not already created in the data folder, initializing the setup screen for the user to input their information.
    try:
        with open("setup.dat", "r") as file:
            values = {}
            for i in file:
                line = i.rstrip('\n').rsplit(':')
                values[str(line[0])] = str(line[1])

            file.close()  
            try:
                gui.main(values["location"], values["api_key"], int(values["cycle"]))
            except:
                setup_window()
    except:
        setup_window()

def setup_window():
    '''
    Loop for the setup window.
    '''
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    root = customtkinter.CTk()
    root.title("ChiPi Weather Initialization")
    root.geometry("700x500")

    title_label = customtkinter.CTkLabel(root, text="Please enter the name of the city, your OpenWeather Api-key,\nand the wait time between update cycles (in minutes).", width=50, height=40, font=('Ubuntu', 18))
    title_label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

    location_label = customtkinter.CTkLabel(root, text="Location:", width=50, height=25, font=('Ubuntu', 18))
    location_label.place(relx=0.110, rely=0.3, anchor=customtkinter.CENTER)

    api_label = customtkinter.CTkLabel(root, text="Api-key:", width=50, height=25, font=('Ubuntu', 18))
    api_label.place(relx=0.1, rely=0.4, anchor=customtkinter.CENTER)

    location_input = customtkinter.CTkEntry(root, placeholder_text="Enter city name here", placeholder_text_color="gray", width=300, height=25, border_width=1, corner_radius=5)
    location_input.place(relx=0.6, rely=0.30, anchor=customtkinter.CENTER)

    api_input = customtkinter.CTkEntry(root, placeholder_text="Enter api-key here", placeholder_text_color="gray", width=300, height=25, border_width=1, corner_radius=5)
    api_input.place(relx=0.6, rely=0.4, anchor=customtkinter.CENTER)

    update_cycle_label = customtkinter.CTkLabel(root, text="Update cycle (minutes):", width=50, height=25, font=('Ubuntu', 18))
    update_cycle_label.place(relx=0.05, rely=0.47)

    cycle_entry = customtkinter.CTkEntry(master=root, border_width=1, height=25, width=100, corner_radius=5)
    cycle_entry.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

    help_button = customtkinter.CTkButton(root, text="Help", command=None, fg_color="orange", width=150, height=80)
    help_button.place(relx=0.10, rely=0.8)

    continue_button = customtkinter.CTkButton(root, text="Continue", command=lambda:input_valid(location_input.get(), api_input.get(), cycle_entry.get(), root, title_label), fg_color="green", width=150, height=80)
    continue_button.place(relx=0.65, rely=0.8)

    root.mainloop()

def input_valid(location, api, cycle, root, title):
    '''
    Checks if the entered information are valid to safely proceed further in the program.
    '''
    if location != "" and api != "" and cycle.isdigit() == True:
        cycle = int(cycle)
        if cycle > 1440:
            cycle = 1440
        elif cycle <= 0:
            cycle = 1
        create_setup_file(location, api, cycle, root)        
    else:
        title.configure(text="Empty or invalid fields detected, please check that you\nhave filled the input fields correctly!")

def create_setup_file(location, api, cycle, root):
    '''
    Generates the setup.dat file with the user entered information.
    If the file exists but is invalid in some way, this function will also work
    as a overwriter.
    '''
    with open("setup.dat", "w") as file:
        file.write(f"location:{location}\napi_key:{api}\ncycle:{cycle}")
        file.close()
        root.destroy()
        gui.main(location, api, cycle)

if __name__ == "__main__":
    main()