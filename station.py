import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import maya

class Station():
    def __init__(self):
        self.wndspd = 'NA'
        self.maxspd = 'NA'
        self.wnddir = 'NA'
        self.tmstp = maya.parse('1999-01-01T00:00:00+00:00').datetime()
        self.location = "NA"
        #self.update()

    def update(self):
        pass

    def print(self):
        print(self.location)
        print('Time:',self.tmstp.time())
        print('Wind Speed knts:',self.wndspd)
        print('Max Gust:',self.maxspd)
        print('Direction:',self.wnddir)
        print('TIMESTAMP: ',type(self.tmstp.time()))

    @staticmethod
    def get_direction_str(direction):
        d = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
        try:
            t = float(direction)
        except:
            return('NONE')
        if t >= 348.75:
            t = t - 360
        t += 11.25
        i = int(t/22.5)
        return str(d[i] +' '+ direction)

class EC_Station(Station):
    
    def __init__(self,name='CVTF',min=''):  
        Station.__init__(self)    
        self.path = 'https://dd.weather.gc.ca/observations/swob-ml/latest/{0}-AUTO{1}-swob.xml'.format(name,min)
        self.update()

    def update(self):
        
        res = requests.get(self.path)
        soup = BeautifulSoup(res.text,'lxml')

        try:
            u_wndspd = soup.elements(attrs={'name' : 'avg_wnd_spd_10m_pst10mts'})
        except:
            self.wndspd = '0'
        else:
            self.wndspd = str(round(float(u_wndspd[0].get('value'))*.54) )
        
        try:
            u_maxspd = soup.elements(attrs={'name' : 'max_wnd_spd_10m_pst10mts'})
        except:
            self.maxspd = '0'
        else:
            self.maxspd = str(round(float(u_maxspd[0].get('value'))*.54))
        
        try:
            u_wnddir = soup.elements(attrs={'name' : 'wnd_dir_10m_pst10mts_max_spd'})
        except:
            self.wnddir = '0'
        else:
            self.wnddir = self.get_direction_str(u_wnddir[0].get('value')) 
        
        try:
            u_lstupdate = soup.find(attrs={'name':'date_tm'})
        except:
            self.tmstp =  maya.parse('1999-01-01T00:00:00+00:00').datetime()
            return
            
        
        try:
            u_location = soup.find(attrs={'name':'stn_nam'})
        except:
            self.location = 'No Info'
            return
        
        self.location = u_location.get('value')

        self.tmstp = maya.parse(u_lstupdate.get('value')).datetime(to_timezone='Canada/Pacific',naive=False)
        
        
        
        

class NC_Station(Station):
    def __init__(self,name='CZBB'):
        Station.__init__(self)
        self.path='https://atm.navcanada.ca/atm/iwv/{0}'.format(name)
        self.update()

    def update(self):
        session = HTMLSession()
        resp = session.get(self.path)
        resp.html.render()
        soup = BeautifulSoup(resp.html.html,'lxml')
        
        resp.close()
        session.close()
        
        #get location string first
        location = soup.find(attrs={'class':'display-2'})
        self.location = location.text
        #direction string is next tag
        data = location.find_next(attrs={'class':'display-2'})
    
        #format wind direction string
        p = data.text.split(' ')
        p = [name.strip() for name in p]
        q = [x for x in p if x != '']
        
        if q[0] == 'CALM':
            self.wnddir = 'CALM'
            self.wndspd = '0'
        else:
            d = q[0].strip('°')
            self.wnddir = self.get_direction_str(d)                
            self.wndspd = q[1].strip('kts')
        
        #make sure there is a returned result for max speed
        if len(q) > 2:
            self.maxspd = q[2].strip('kts')
        else:
            self.maxspd = 'NA'

        #Get timestamp info
        a = soup.find(attrs={'class':'headline'})
        #loop to get timestamp tag
        for i in range(3):
            a = a.find_next(attrs={'class':'headline'})
        #a is now the timestamp tag
        self.tmstp = maya.parse(a.text).datetime(to_timezone='Canada/Pacific',naive=False)
        

ft = EC_Station('CVTF','-minute')
#czbb = NC_Station('CZBB')

ft.print()
#czbb.print()

