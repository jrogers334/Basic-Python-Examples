'Most of this code is not original to me.'
'pip install geopy and googlemaps'
'register for a google API and use your key where it says 'YOUR_API_KEY')'
'this code uses the Boston Convention Center as the calcualted from location'
'once promted to enter an address googlemaps will take the first location based on what was entered'
'the more accurate the address the better the results'
'the distance is used using vincenty's formula'

import os
import googlemaps
from geopy.distance import vincenty

gm = googlemaps.Client(key='YOUR_API_KEY')

#The Address for the Boston Convention Center
control = gm.geocode('415 Summer St, Boston, MA 02210')[0]
bosdict = control['geometry']['location']
blat = bosdict.get('lat')
blng = bosdict.get('lng')
btup = (blat, blng)

x = input('Enter in address: ')
def dist_calc(x):
	geocode_result = gm.geocode(str(x))[0]
	geodict = geocode_result['geometry']['location']
	lat = geodict.get('lat')
	lng = geodict.get('lng')
	gtup = (lat, lng)

	print('Lat & Lng for Boston Convention Center: ' + str(btup))
	print('Lat & Lng for ' + x + ':' + str(gtup))
	print(vincenty(gtup, btup).miles)

dist_calc(x)
