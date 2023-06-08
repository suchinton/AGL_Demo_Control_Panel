import os
import requests
import sys

import folium
from PyQt5.QtCore import Qt, QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QListWidget, QPushButton


def main():
    app = QApplication(sys.argv)
    widget = AddressSearchWidget()
    widget.show()
    sys.exit(app.exec_())


class AddressSearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Address Search")
        self.setWindowIcon(QIcon("icon.png"))

        self.address_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.suggestions_list = QListWidget()
        self.map_view = QWebEngineView(self)
        self.map_view.setMinimumSize(800, 600)
        self.latitude_label = QLabel("Latitude:")
        self.latitude_input = QLineEdit()
        self.longitude_label = QLabel("Longitude:")
        self.longitude_input = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Address:"))
        layout.addWidget(self.address_input)
        layout.addWidget(self.search_button)
        layout.addWidget(QLabel("Suggestions:"))
        layout.addWidget(self.suggestions_list)
        layout.addWidget(self.map_view)
        layout.addWidget(self.latitude_label)
        layout.addWidget(self.latitude_input)
        layout.addWidget(self.longitude_label)
        layout.addWidget(self.longitude_input)

        self.setLayout(layout)

        self.search_button.clicked.connect(self.search_address)
        self.suggestions_list.itemClicked.connect(self.select_suggestion)

    def search_address(self):
        query = self.address_input.text()
        suggestions = self.fetch_address_suggestions(query)
        self.show_suggestions(suggestions)

    def fetch_address_suggestions(self, query):
        url = f"https://nominatim.openstreetmap.org/search?format=json&limit=5&q={requests.utils.quote(query)}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def show_suggestions(self, suggestions):
        self.suggestions_list.clear()
        for suggestion in suggestions:
            address = suggestion.get("display_name", "")
            self.suggestions_list.addItem(address)

    def select_suggestion(self, item):
        address = item.text()
        self.address_input.setText(address)
        self.show_location()

    def show_location(self):
        query = self.address_input.text()
        url = f"https://nominatim.openstreetmap.org/search?format=json&limit=1&q={requests.utils.quote(query)}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = data[0]["lat"]
                lon = data[0]["lon"]
                location = [float(lat), float(lon)]

                self.update_map(location)
                self.latitude_input.setText(lat)
                self.longitude_input.setText(lon)

    def update_map(self, location):
        map_html = self.create_map_html(location)
        file_path = os.path.abspath("map.html")
        with open(file_path, "w") as f:
            f.write(map_html)
        self.map_view.load(QUrl.fromLocalFile(file_path))

    def create_map_html(self, location):
        map = folium.Map(location=location, zoom_start=15)
        marker = folium.Marker(location=location)
        marker.add_to(map)
        return map._repr_html_()


if __name__ == '__main__':
    main()
