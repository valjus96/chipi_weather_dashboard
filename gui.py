#ChiPi Weather Dashboard
#By valjus96, (https://github.com/valjus96)

#main gui
import customtkinter
from PIL import Image
import datetime
import time
import threading
import call
import os

class Gui:
    def __init__(self, location, api_key, update_cycle):
        self.__api_object = call.create_obj()      
        self.__countdown_to_update = 300
        self.__is_night = False

        #Values set from the launch.py module, when program in initialized.
        self.__location = location
        self.__api_key = api_key
        self.__update_cycle = update_cycle

        #Holder for the configure window root, so it can be conviently accessed outside of the method and destroyed when ending the program.
        self.__configure_window = None

        #main weather/time&date attributes that will contain the latest weather data fetched from Openweather.
        self.__weather_symbol_label = None
        self.__temperature = None
        self.__temperature_feel = None
        self.__last_update = None
        self.__location_label = None
        self.__date = None
        self.__clock = None
        self.__humidity = None
        self.__weather_status = None
        self.__wind_speed = None
        self.__pressure = None
        
        #Error text box to display error message when one is encountered.
        self.__error_label = ""

        #Holders for the forecasts displayed in the main window
        self.__three_hour_forecast_first = None
        self.__three_hour_forecast_second = None
        self.__three_hour_forecast_third = None
        self.__three_hour_forecast_fourth = None
        self.__three_hour_forecast_fifth = None

        #Holders for the forecast condition images displayed in the main window
        self.__three_hour_forecast_first_image = None
        self.__three_hour_forecast_second_image = None
        self.__three_hour_forecast_third_image = None
        self.__three_hour_forecast_fourth_image = None
        self.__three_hour_forecast_fifth_image = None

        #Relative file path to the data/assets folder.
        self.__assets_file_path = self.set_file_paths()

        #Thread for the clock, which updates the time and date in the main window. Runs the timer for the update cycle as well (self.__countdown_to_update)
        self.__time_update = threading.Thread(name='gui_clock_update', target=self.update_clock)
        #Thread for the gui.
        self.__gui_loop = threading.Thread(name='gui_loop', target=self.main_loop)
        #When killswitch is True, ends the self.__time_update thread.
        self.__threads_killswitch = False

        self.__gui_loop.start()    

    def set_file_paths(self):
        '''
        setting the relative path for the assets folder containing the image files for the gui.
        '''
        abs_path = os.path.dirname(__name__)
        rel_path = "assets/"
        return os.path.join(abs_path, rel_path)

    def start_exit(self):
        '''
        Kills the ongoing threads and exits the program
        '''
        self.__threads_killswitch = True

        try:
            self.__configure_window.destroy()
        except:
            pass
        exit()

    def update_clock(self):
        '''
        Updates the clock in the interface every second. Every 300 seconds an api call will be made and weathers stats will be updated.
        '''
        while self.__threads_killswitch == False:
            time_date = datetime.datetime.now()
            current_date = time_date.strftime("%A\n%d/%m/%Y")
            current_time = time_date.strftime("%H:%M")
            self.__date.configure(text=f"{current_date}")
            self.__clock.configure(text=f"{current_time}")

            current_hour = time_date.strftime("%H")
            if int(current_hour) < 6:
                self.__is_night = True
            else:
                self.__is_night = False


            if self.__countdown_to_update >= self.__update_cycle:
                self.request_weather_data()
                self.__countdown_to_update = 0

            time.sleep(1)
            self.__countdown_to_update+=1

    def request_weather_data(self):
        '''
        Calls call.py module twice: weather_data is the current weather data,
        and forecast_data is the weather data for the next 15 hours in 3 hour cycles.
        '''
        weather_data = self.__api_object.call_api(self.__api_key, self.__location)
        forecast_data = self.__api_object.call_api(self.__api_key, self.__location, True)

        if weather_data == None or forecast_data == None:
            self.__error_label.configure(text="Error in retrieving the weather data from OpenWeather")
            return
        else:
            self.__error_label.configure(text="")

        self.update_gui_stats(weather_data)
        self.update_gui_forecasts(forecast_data)

    def update_gui_stats(self, weather_data):
        '''
        Updates the weather stats and the weather condition image in the interface
        '''
        self.__temperature.configure(text=f"{int(weather_data['main']['temp_max']) - 273.15:.1f}°C", )
        self.__temperature_feel.configure(text=f"Feels like: {int(weather_data['main']['feels_like']) - 273.15:.1f}°C")
        self.__humidity.configure(text=f"Humidity: {str(weather_data['main']['humidity'])}%")
        self.__weather_status.configure(text=f"Condition: {str(weather_data['weather'][0]['description'])}")
        self.__wind_speed.configure(text=f"Wind: {str(weather_data['wind']['speed'])}m/s")
        self.__pressure.configure(text=f"Pressure: {str(weather_data['main']['pressure'])} hPa")

        current_time = datetime.datetime.now()
        self.__last_update.configure(text= "Last update: " + current_time.strftime("%X"))

        condition = str(weather_data['weather'][0]['description'])

        if self.__is_night == True:
            try:
                if condition == "clear sky" or condition == "few clouds" or condition == "scattered clouds":
                    new_icon = customtkinter.CTkImage(Image.open(self.__assets_file_path + condition + "night.png"), size=[200, 200])
                else:
                    new_icon = customtkinter.CTkImage(Image.open(self.__assets_file_path + condition + ".png"), size=[200, 200])
                self.__weather_symbol_label.configure(image=new_icon)
            except:
                new_icon = customtkinter.CTkImage(Image.open(self.__assets_file_path + "error.png"), size=[200, 200])
                self.__weather_symbol_label.configure(image=new_icon)

        else:
            try:
                new_icon = customtkinter.CTkImage(Image.open(self.__assets_file_path + condition + ".png"), size=[200, 200])
                self.__weather_symbol_label.configure(image=new_icon)
            except:
                new_icon = customtkinter.CTkImage(Image.open(self.__assets_file_path + "error.png"), size=[200, 200])
                self.__weather_symbol_label.configure(image=new_icon)

    def update_gui_forecasts(self, forecast_data):
        '''
        Updating the forecasts labels in the ui based on the retrieved forecast data from openweather
        '''
        self.__three_hour_forecast_first.configure(text=f"{self.format_forecast_time(forecast_data['list'][1]['dt_txt'])}\n{forecast_data['list'][1]['main']['temp_max'] - 273.15:.1f}°C")
        self.__three_hour_forecast_first_image.configure(image=self.forecast_symbol_creation(2, forecast_data, self.format_forecast_time(forecast_data['list'][1]['dt_txt'])))

        self.__three_hour_forecast_second.configure(text=f"{self.format_forecast_time(forecast_data['list'][2]['dt_txt'])}\n{forecast_data['list'][2]['main']['temp_max'] - 273.15:.1f}°C")
        self.__three_hour_forecast_second_image.configure(image=self.forecast_symbol_creation(2, forecast_data, self.format_forecast_time(forecast_data['list'][2]['dt_txt'])))

        self.__three_hour_forecast_third.configure(text=f"{self.format_forecast_time(forecast_data['list'][3]['dt_txt'])}\n{forecast_data['list'][3]['main']['temp_max'] - 273.15:.1f}°C")
        self.__three_hour_forecast_third_image.configure(image=self.forecast_symbol_creation(2, forecast_data, self.format_forecast_time(forecast_data['list'][3]['dt_txt'])))

        self.__three_hour_forecast_fourth.configure(text=f"{self.format_forecast_time(forecast_data['list'][4]['dt_txt'])}\n{forecast_data['list'][4]['main']['temp_max'] - 273.15:.1f}°C")
        self.__three_hour_forecast_fourth_image.configure(image=self.forecast_symbol_creation(2, forecast_data, self.format_forecast_time(forecast_data['list'][4]['dt_txt'])))

        self.__three_hour_forecast_fifth.configure(text=f"{self.format_forecast_time(forecast_data['list'][5]['dt_txt'])}\n{forecast_data['list'][5]['main']['temp_max'] - 273.15:.1f}°C")
        self.__three_hour_forecast_fifth_image.configure(image=self.forecast_symbol_creation(2, forecast_data, self.format_forecast_time(forecast_data['list'][5]['dt_txt'])))

    def forecast_symbol_creation(self, index_number, data_container, time):
        '''
        Returns a CTkImage with the correct weather symbol for the chosen forecast slot.
        '''

        condition = data_container['list'][index_number]['weather'][0]['description']

        #determining if night time weather symbols should be displayed or not. Every condition does not have a night time version, so in that case the regular one will be displayed.
        night_time = False
        if int(time[:2]) < 6:
            night_time = True

        if night_time == False:
            try:
                return_image = customtkinter.CTkImage(Image.open(self.__assets_file_path + condition + ".png"), size=[150, 150])
            except:
                return_image = customtkinter.CTkImage(Image.open(self.__assets_file_path + "error.png"), size=[150, 150])

        else:
            try:
                if condition == "clear sky" or condition == "few clouds" or condition == "scattered clouds":
                    return_image = customtkinter.CTkImage(Image.open(self.__assets_file_path + condition + " night.png"), size=[150, 150])
                else:
                    return_image = customtkinter.CTkImage(Image.open(self.__assets_file_path + condition + ".png"), size=[150, 150])
            except:
                    return_image = customtkinter.CTkImage(Image.open(self.__assets_file_path + "error.png"), size=[150, 150])

        return return_image

    def format_forecast_time(self, forecast_time):
        '''
        "cleans" the timestamp by removing the date from the beginning of the string and seconds from the end of the string.
        Returns the reformated time to be displayed in the ui.
        '''
        forecast_time = forecast_time[11:]
        forecast_time = forecast_time[:5]
        return forecast_time
    
    def main_loop(self):
        '''
        Loop for the main window.
        '''
        customtkinter.set_appearance_mode("Light")
        customtkinter.set_default_color_theme("blue") 

        root = customtkinter.CTk()
        root.title("ChiPi Weather Dashboard")
        root.geometry("1020x600")

        #left disabled, but when active does fill the 10.1 inch screen nicely. Blocks you from doing anything else on the pi though.
        #root.overrideredirect(True)

        #initializing the frames of the interface
        main_frame = customtkinter.CTkFrame(master=root, width=1020, height=600)
        main_frame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        #initializing top left frame widgets, containing weather data and symbol for the weather condition.
        icon = customtkinter.CTkImage(Image.open(self.__assets_file_path + "error.png"), size=[150, 150])

        self.__weather_symbol_label = customtkinter.CTkLabel(main_frame, text="", image=icon, width=200, height=200)
        self.__weather_symbol_label.place(relx=0.03, rely=0.13, anchor=customtkinter.NW)

        self.__temperature = customtkinter.CTkLabel(main_frame, text="0.0°C", width=25, height=100, font=('Ubuntu', 55)) 
        self.__temperature.place(relx=0.25, rely=0.09, anchor=customtkinter.NW)

        self.__temperature_feel =customtkinter.CTkLabel(main_frame, text="Feels: 0.0°C", width=50, height=25, font=('Ubuntu', 20)) 
        self.__temperature_feel.place(relx=0.26, rely=0.22, anchor=customtkinter.NW)

        self.__weather_status =customtkinter.CTkLabel(main_frame, text="Condition: error", width=50, height=25, font=('Ubuntu', 20)) 
        self.__weather_status.place(relx=0.26, rely=0.27, anchor=customtkinter.NW)

        self.__humidity =customtkinter.CTkLabel(main_frame, text="Humidity: 0%", width=50, height=25, font=('Ubuntu', 20)) 
        self.__humidity.place(relx=00.26, rely=0.32, anchor=customtkinter.NW)

        self.__wind_speed =customtkinter.CTkLabel(main_frame, text="Wind: 0.0/s", width=50, height=25, font=('Ubuntu', 20)) 
        self.__wind_speed.place(relx=0.26, rely=0.37, anchor=customtkinter.NW)

        self.__pressure =customtkinter.CTkLabel(main_frame, text="Pressure: 0 hpA", width=50, height=25, font=('Ubuntu', 20)) 
        self.__pressure.place(relx=0.26, rely=0.42, anchor=customtkinter.NW)

        self.__last_update = customtkinter.CTkLabel(main_frame, text="Last update: Error", width=20, height=10, font=('Ubuntu', 15)) 
        self.__last_update.place(relx=0.03, rely=0.07, anchor=customtkinter.NW)

        self.__location_label = customtkinter.CTkLabel(main_frame, text="Selected location: " + self.__location, width=20, height=10, font=('Ubuntu', 15)) 
        self.__location_label.place(relx=0.03, rely=0.03, anchor=customtkinter.NW)

        #Center Up/Right
        self.__date = customtkinter.CTkLabel(main_frame, text="Error in retrieving date and time", width=50, height=25, font=('Ubuntu', 27)) 
        self.__date.place(relx=0.75, rely=0.05, anchor=customtkinter.N)

        self.__clock = customtkinter.CTkLabel(main_frame, text="00:00", width=50, height=25, font=('Ubuntu', 85)) 
        self.__clock.place(relx=0.75, rely=0.19, anchor=customtkinter.N)

        self.__error_label = customtkinter.CTkLabel(main_frame, text="", text_color="red", width=50, height=15, font=('Ubuntu', 16)) 
        self.__error_label.place(relx=0.8, rely=0.35, anchor=customtkinter.NE)

        #right side panel buttons
        update_button = customtkinter.CTkButton(master=main_frame, text="Force update", text_color="white", command=self.request_weather_data, width=150, height=60, fg_color=("#6ad0ff"), font=('Ubuntu' ,20))
        update_button.place(relx=0.83, rely=0.55)

        settings_button = customtkinter.CTkButton(master=main_frame, text="Configure", text_color="white", command=self.configure_window, width=150, height=60, fg_color=("#6ad0ff"), font=('Ubuntu' ,20))
        settings_button.place(relx=0.83, rely=0.67)

        exit_button = customtkinter.CTkButton(master=main_frame, text="Exit", text_color="white", command=self.start_exit, width=150, height=60, fg_color=("#6ad0ff"), font=('Ubuntu' ,20))
        exit_button.place(relx=0.83, rely=0.79)

        #bottom 3h forecasts section
        forecast_title_label = customtkinter.CTkLabel(main_frame, text="Forecasts", width=50, height=25, font=('Ubuntu', 35))
        forecast_title_label.place(relx=0.09, rely=0.54, anchor=customtkinter.CENTER)

        #labels 3h forecasts for temperature/time.
        self.__three_hour_forecast_first =customtkinter.CTkLabel(main_frame, text="21:00\n25.4°C", width=50, height=25, font=('Ubuntu', 20)) 
        self.__three_hour_forecast_first.place(relx=0.1, rely=0.85, anchor=customtkinter.CENTER)

        self.__three_hour_forecast_second =customtkinter.CTkLabel(main_frame, text="00:00\n25.4°C", width=50, height=25, font=('Ubuntu', 20)) 
        self.__three_hour_forecast_second.place(relx=0.25, rely=0.85, anchor=customtkinter.CENTER)

        self.__three_hour_forecast_third =customtkinter.CTkLabel(main_frame, text="03:00\n25.4°C", width=50, height=25, font=('Ubuntu', 20)) 
        self.__three_hour_forecast_third.place(relx=0.40, rely=0.85, anchor=customtkinter.CENTER)

        self.__three_hour_forecast_fourth =customtkinter.CTkLabel(main_frame, text="06:00\n25.4°C", width=50, height=25, font=('Ubuntu', 20)) 
        self.__three_hour_forecast_fourth.place(relx=0.55, rely=0.85, anchor=customtkinter.CENTER)

        self.__three_hour_forecast_fifth =customtkinter.CTkLabel(main_frame, text="09:00\n25.4°C", width=50, height=25, font=('Ubuntu', 20)) 
        self.__three_hour_forecast_fifth.place(relx=0.70, rely=0.85, anchor=customtkinter.CENTER)

        #weather symbols for the 3h forecasts, error image for default
        self.__three_hour_forecast_first_image =customtkinter.CTkLabel(main_frame, text="", image=icon, width=150, height=150) 
        self.__three_hour_forecast_first_image.place(relx=0.1, rely=0.69, anchor=customtkinter.CENTER)

        self.__three_hour_forecast_second_image =customtkinter.CTkLabel(main_frame, text="", image=icon, width=150, height=150) 
        self.__three_hour_forecast_second_image.place(relx=0.25, rely=0.69, anchor=customtkinter.CENTER)

        self.__three_hour_forecast_third_image =customtkinter.CTkLabel(main_frame, text="", image=icon, width=150, height=150) 
        self.__three_hour_forecast_third_image.place(relx=0.40, rely=0.69, anchor=customtkinter.CENTER)

        self.__three_hour_forecast_fourth_image =customtkinter.CTkLabel(main_frame, text="", image=icon, width=150, height=150) 
        self.__three_hour_forecast_fourth_image.place(relx=0.55, rely=0.69, anchor=customtkinter.CENTER)

        self.__three_hour_forecast_fifth_image =customtkinter.CTkLabel(main_frame, text="", image=icon, width=150, height=150) 
        self.__three_hour_forecast_fifth_image.place(relx=0.70, rely=0.69, anchor=customtkinter.CENTER)

        self.__time_update.start()
        root.mainloop()

    def configure_window(self):
        '''
        In this window the user can configure the api-key, location and update cycle settings on-the-fly.
        The user can either close and save the entered new settings into the setup.dat file, or decide to close
        the window without making any changes to the file.
        '''
        customtkinter.set_appearance_mode("Light")
        customtkinter.set_default_color_theme("blue") 

        self.__configure_window = customtkinter.CTk()
        self.__configure_window.title("ChiPi Weather Configurations")
        self.__configure_window.geometry("500x400")

        title_label = customtkinter.CTkLabel(self.__configure_window, text="Configurations", width=50, height=25, font=('Ubuntu', 30))
        title_label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        location_label = customtkinter.CTkLabel(self.__configure_window, text="Location:", width=50, height=25, font=('Ubuntu', 18))
        location_label.place(relx=0.06, rely=0.3, anchor=customtkinter.W)

        api_label = customtkinter.CTkLabel(self.__configure_window, text="Api-key: ", width=50, height=25, font=('Ubuntu', 18))
        api_label.place(relx=0.06, rely=0.4, anchor=customtkinter.W)

        cycle_label = customtkinter.CTkLabel(self.__configure_window, text="Update cycle: ", width=50, height=15, font=('Ubuntu', 18))
        cycle_label.place(relx=0.06, rely=0.5, anchor=customtkinter.W)

        current_location_label = customtkinter.CTkLabel(self.__configure_window, text="Current location: " + self.__location, width=50, height=25, font=('Ubuntu', 10))
        current_location_label.place(relx=0.1, rely=0.35, anchor=customtkinter.W)

        current_api_label = customtkinter.CTkLabel(self.__configure_window, text="Current api-key: " + self.__api_key, width=50, height=15, font=('Ubuntu', 10))
        current_api_label.place(relx=0.1, rely=0.45, anchor=customtkinter.W)

        current_cycle = customtkinter.CTkLabel(self.__configure_window, text="Current update cycle: every " + str(int(self.__update_cycle / 60)) + " minutes", width=50, height=15, font=('Ubuntu', 10))
        current_cycle.place(relx=0.1, rely=0.55, anchor=customtkinter.W)

        location_input = customtkinter.CTkEntry(master=self.__configure_window, placeholder_text="Enter city name", placeholder_text_color="gray", width=300, height=25, border_width=1, corner_radius=5)
        location_input.place(relx=0.6, rely=0.30, anchor=customtkinter.CENTER)

        api_input = customtkinter.CTkEntry(master=self.__configure_window, placeholder_text="Enter api-key", placeholder_text_color="gray", width=300, height=25, border_width=1, corner_radius=5)
        api_input.place(relx=0.6, rely=0.4, anchor=customtkinter.CENTER)

        cycle_input = customtkinter.CTkEntry(master=self.__configure_window, placeholder_text="Enter update cycle in minutes", placeholder_text_color="gray", width=300, height=25, border_width=1, corner_radius=5)
        cycle_input.place(relx=0.6, rely=0.5, anchor=customtkinter.CENTER)

        bottom_text_label = customtkinter.CTkLabel(self.__configure_window, text="Save given information to the setup.dat file by\nchoosing 'Save and close'\n or choose 'Close' to exit without saving.", width=50, height=25, font=('Ubuntu', 19))
        bottom_text_label.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

        save_close_button = customtkinter.CTkButton(master=self.__configure_window, text="Save and close", command=lambda: self.configure_window_closing(api_input.get(), location_input.get(), cycle_input.get()), width=150, height=50, fg_color=("red"), font=('Ubuntu' ,20))
        save_close_button.place(relx=0.75, rely=0.9, anchor=customtkinter.CENTER)

        hard_close_button = customtkinter.CTkButton(master=self.__configure_window, text="Close", command=self.__configure_window.destroy, width=150, height=50, fg_color=("red"), font=('Ubuntu' ,20))
        hard_close_button.place(relx=0.25, rely=0.9, anchor=customtkinter.CENTER)

        self.__configure_window.mainloop()

    def configure_window_closing(self, api_key, location, update_cycle=5):
        '''
        This method saves the user entered information from the configuration window into the setup.data file.
        If a field in the window is left empty, no changes will be made in that specific setting.
        '''
        if len(api_key) == 0 and len(self.__api_key) == 0:
            self.__error_label.configure(text="No api-key entered")

        elif len(api_key) == 0 and len(self.__api_key) > 0:
            api_key = self.__api_key
            self.__error_label.configure(text="")

        else:
            self.__error_label.configure(text="")
            self.__api_key = api_key

        if len(location) == 0:
            location = self.__location
        
        if len(update_cycle) == 0:
                update_cycle = self.__update_cycle

        with open("setup.dat", "w") as file:
            file.write(f"location:{location}\napi_key:{api_key}\ncycle:{update_cycle*60}")
            file.close()

        self.__location = location
        self.__location_label.configure(text="Selected location: " + location)
        self.__configure_window.destroy()
        self.__configure_window = None

def main(location, api, update_cycle):
    Gui(location, api, update_cycle*60)

if __name__ == "__main__":
    main()