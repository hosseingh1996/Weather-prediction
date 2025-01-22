import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox, QProgressBar, QGroupBox
)
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"I:\pay\python\air prediction.ui", self)
        self.temperature_data = []
        self.city_data = []


        self.fetch_button.clicked.connect(self.fetch_weather_data)
        self.input_group.setLayout(self.input_layout)
        self.result_label.setWordWrap(True)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)



    def fetch_weather_data(self):
        city_name = self.city_input.text().strip()
        if not city_name:
            QMessageBox.warning(self, "Input Error", "Please enter a city name!")
            return



        api_key = "e53d867f00443e8d8c29db49be0dd388"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                temperature = data["main"]["temp"]
                feels_like = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                sea_level = data["main"]["sea_level"]
                weather_description = data["weather"][0]["description"]


                result_text = (
                    f"City: {city_name}\n"
                    f"Temperature: {temperature}°C\n"
                    f"Feels Like: {feels_like}°C\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind Speed: {wind_speed} m/s\n"
                    f"sea level: {sea_level} m\n"
                    f"Weather: {weather_description.capitalize()}"
                )
                self.result_label.setText(result_text)

                if city_name not in self.city_data:

                    self.city_data.append(city_name)
                    self.temperature_data = [temperature]
                else:
                    self.temperature_data.append(temperature)


                self.plot_temperature()

            else:
                error_message = response.json().get("message", "Unable to fetch weather data.")
                QMessageBox.warning(self, "Error", error_message.capitalize())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


    def plot_temperature(self):
        self.figure.clear()


        ax = self.figure.add_subplot(111)


        if len(self.temperature_data) > 0:
            ax.plot(self.temperature_data, marker='o', linestyle='-', label='Temperature')


            ax.set_title('Temperature Over Time', fontsize=12)
            ax.set_xlabel('Fetch Count', fontsize=12)
            ax.set_ylabel('Temperature (°C)', fontsize=12)
            ax.axhline(y=sum(self.temperature_data)/len(self.temperature_data), color='r', linestyle='--', label='Average Temp')
            ax.grid(True)
            ax.legend()


        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
