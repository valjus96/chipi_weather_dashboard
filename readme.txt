----------------------
ChiPi Weather Dashboards
----------------------

By valjus96
(https://github.com/valjus96)

Gui builded using customtkinter by Tom Schimansky
(https://github.com/TomSchimansky/CustomTkinter)

This simple software is designed to be left running for non defined amount of time and display
weather statistics fetched from Openweather.org based on specific location and update cycles defined by the user. Created for my own raspberry pi project, and main window is designed to fill a 10.1 inch screen and be run on a Raspberry pi Zero 2.

Note that to use this software you must have your own openweather api-key that you can request from the openweather website (https://openweathermap.org/). Keep in mind the daily call limits, and plan your update cycle to "stay within the budget".

When booting the software for the first time you will be prompted to enter the name of the city
which weather you would like to follow, as well as your openweather api-key. Enter the weather update cycle in minutes (1 minute is minimun, max 1440). A setup.dat file will be generated in to the data folder, which will store the entered information for the future, so you dont have to enter them again after reebooting the software.

In the main window the weather of your chosen location will be shown and updated in the pre-determed cycles.
-- Force update -button will update the weather information immediately.
-- Configure -button will open a separate window, where you can change the location and api-key                    information on the fly. New information will be stored in the setup.dat file.
-- Exit -button will end the program.

Feel free to use and modify this software to suit it better for your own projects, but please be mindful of not claiming this is completely your own creation. Please see the licence,txt for more information. Credits, feedbacks as well as constructive criticism and suggestions are greatly appreciated!


