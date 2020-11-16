from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase 
import datetime
import station


class mainApp(MDApp):
    def on_start(self):
        self.theme_cls.primary_palette = "BlueGray"
        self.ft = station.EC_Station('CVTF','-minute')
        self.cyvr = station.NC_Station('CYVR')
        self.czbb = station.NC_Station('CZBB')
        self.root.ids.tabs.add_widget(Tab(self.ft))
        self.root.ids.tabs.add_widget(Tab(self.czbb))
        self.root.ids.tabs.add_widget(Tab(self.cyvr))

        #
        #
        #self.root.id.FT.windspeed.text = 'THIS IS A TEST'

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        instance_tab.tab_update()
        print('TAB SWITCH')
        """Class implementing content"""    

class Tab(FloatLayout, MDTabsBase):   
    def __init__(self,station):
        super().__init__(text= station.location)
        self.station = station
        self.ids.windspeed.text += station.wndspd
        self.ids.maxgust.text += station.maxspd
        self.ids.direction.text +=  station.wnddir
        self.ids.tmstp.text += str(station.tmstp.time())
        print('IN TAB',type(station.tmstp.time()))

    def tab_update(self):
        if datetime.datetime.now().timestamp() - self.station.tmstp.timestamp() > 300: 
            self.station.update()
            print('5 min since last update')
        self.ids.windspeed.text = ' Wind Speed: ' + self.station.wndspd
        self.ids.maxgust.text = ' Gust: ' + self.station.maxspd
        self.ids.direction.text = ' Direction: ' + self.station.wnddir
        self.ids.tmstp.text = ' Last Update: ' + str(self.station.tmstp.time())
        print('tab update')
    """Class implementing content"""

mainApp().run()