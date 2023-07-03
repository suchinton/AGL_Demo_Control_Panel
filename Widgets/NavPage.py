"""
    Copyright 2023 Suchinton Chakravarty

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at 

        http://www.apache.org/licenses/LICENSE-2.0  
        
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import os
import sys
import requests
import folium
from PyQt5 import uic, QtCore

from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QListWidget, QLineEdit
from PyQt5.QtGui import QPainterPath, QRegion
from PyQt5.QtCore import QRectF

current_dir = os.path.dirname(os.path.abspath(__file__))

# ========================================

sys.path.append(os.path.dirname(current_dir))

import extras.Kuksa_Instance as kuksa_instance

Form, Base = uic.loadUiType(os.path.join(current_dir, "../ui/Nav.ui"))

# ========================================

class NavWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.set_instance()

        self.From_address = self.findChild(QLineEdit, "From_address")
        self.To_address = self.findChild(QLineEdit, "To_address")
        self.Suggestions = self.findChild(QListWidget, "Suggestions")
        self.map_view = self.findChild(QWebEngineView, "map_view")
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.map_view.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        self.map_view.setMask(mask)

        # create two QThreads to run the search_address function for each text field
        self.searching_thread = QThread()

        self.From_address.textChanged.connect(lambda: self.start_search(self.From_address.text()))
        self.To_address.textChanged.connect(lambda: self.start_search(self.To_address.text()))

        self.Suggestions.itemClicked.connect(self.select_suggestion)

    def start_search(self, query):

        self.searching_thread.run = lambda: self.search_address(query)
        self.searching_thread.start()

        # When search address is finished, print "Search finished" to the console and end the thread'
        self.searching_thread.finished.connect(lambda: print("Search finished"))

    def search_address(self, query):
        options = self.fetch_address_suggestions(query)
        self.show_suggestions(options)

    def fetch_address_suggestions(self, query):
        url = f"https://nominatim.openstreetmap.org/search?format=json&limit=5&q={requests.utils.quote(query)}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def show_suggestions(self, options):
        self.Suggestions.clear()
        for suggestion in options:
            address = suggestion.get("display_name", "")
            self.Suggestions.addItem(address)

    def select_suggestion(self, item):
        address = item.text()
        # self.address_input.setText(address)
        self.show_location(address)

    def show_location(self, query):
        url = f"https://nominatim.openstreetmap.org/search?format=json&limit=1&q={requests.utils.quote(query)}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = data[0]["lat"]
                lon = data[0]["lon"]
                location = [float(lat), float(lon)]

                self.update_map(location)
                print(location)

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
    
    def set_instance(self):
        self.kuksa = kuksa_instance.KuksaClientSingleton.get_instance()
        self.client = self.kuksa.get_client()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = NavhWidget()
    w.show()
    sys.exit(app.exec_())
