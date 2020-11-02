import folium 
import gpxpy
import os
import base64
from PIL import Image
import PIL
from image_edition import image_edition
from image_edition import image_edition_1
from image_edition import image_edition_2


def overlayGPX(gpxDataList, Colours, Labels, zoom):
	myMap = folium.Map(location=[51.10987325, 17.05046775],zoom_start=zoom)
	# add the layer control
	LC = folium.map.LayerControl(position = 'topleft', collapsed = True, autoZIndex = True)

	# deklaracja warstw
	L1 = folium.FeatureGroup()		# warstwa samej trasy z popupami
	L2 = folium.FeatureGroup()		# warstwa mpk
	L3 = folium.FeatureGroup()		# -- roweru
	L4 = folium.FeatureGroup()		# -- hulajnogi
	L5 = folium.FeatureGroup()		# -- samochodu
	L6 = folium.FeatureGroup()		# -- pieszo
	
	# tyt warstwy
	L1.layer_name = 'Trasa Plac Grunwaldzki - Galeria Dominikańska'
	L2.layer_name = 'Trasa MPK'
	L3.layer_name = 'Trasa rowerowa'
	L4.layer_name = 'Trasa hulajnogi'
	L5.layer_name = 'Trasa samochodu'
	L6.layer_name = 'Trasa piesza'

	# dodawanie tytułu
	title_html = '''
			 <h3 align="center" style="font-size:17px"><b>
			 Najlepszy środek transportu na trasie Plac 
			 Grunwaldzki - Galeria Dominikańska</b></h3>
			 '''
	myMap.get_root().html.add_child(folium.Element(title_html))

	Layers = [L2, L3, L4, L5, L6]
	# dodawanie szlakow z plików GPX
	for gpxData, color, label, layer in zip(gpxDataList, Colours, Labels, Layers):
		for k in range(0, len(gpxData)):
			gpx_file = open(gpxData[k], 'r')
			Lon = []
			Lat = []
			for line in gpx_file:
				X = line.split('"')
				
				for i in X:
					try:
						if float(i) < 20:
							Lon.append(float(i))
						elif float(i) > 20:
							Lat.append(float(i))
					except:
						pass
			points = [];
			for i, j in zip(Lat[4:], Lon[4:]):
				points.append([i, j])
			(folium.vector_layers.PolyLine(points, popup = None, tooltip = label, 
				smooth_factor = 14, color=color)).add_to(layer)

	# ramki informacyjne
	html_1 = '''
	<h1>MPK</h1>
	<ul>
	<li>odjazdy co kilka minut</li>
	<li>koszt: <br>
	- bilet 15-minutowy: (N 2.40 zł, U 1.20 zł), <br>
	- bilety semestralne,
	</li>
	<li>tramwaje: <br>
	- linie: 4, 33 (jadące przez Most Grunwaldzki) – 7 minut (1.5 km), <br>
	- linie 2, 10 (jadące przez Katedrę) – 9 minut (2.0 km), <br>
	</li>
	<li>autobusy: linia D – 7 minut (1.5 km), odjazdy co około 18 minut.
	</li>
	</ul>  '''
	html_2 = '''
	<h1>Rower</h1>
	<ul>
	<li>trasa: <br>
	- w stronę Mostu Grunwaldzkiego, bulwarem na Most Pokoju, parkiem Słowackiego
	do celu. Czas: 9 minut, dystans: 1.9 km, <br>
	- Szczytnicką w Wyszyńskiego, na Most Pokoju, Jana Ewangelisty i Bernardyńską do
	celu. Czas: 9 minut, dystans: 1.9 km,
	</li>
	<li>koszt: <br>
	- własny: za darmo, <br>
	- miejski: 20 pierwszych minut jest za darmo. Koszt aktywacyjny 10 zł. Może się
	zdarzyć brak rowerów w najbliższej okolicy i konieczność podejścia. <br>
	</li>
	</ul>'''
	html_3 = '''
	<h1>Hulajnoga</h1>
	<ul>
	<li>dojście do najbliższej hulajnogi (stan na wtorek godz. 13:30) to około 3 minuty,
	następnie Szczytnicką, Wyszyńskiego, Mostem Pokoju, Jana Ewangelisty i
	Bernardyńską.,</li>
	<li>-koszt (według Google) to około 6-7 zł.
	</li>
	</ul> '''
	html_4 = '''
	<h1>Samochód</h1>
	<ul>
	<li>trasa: <br>
	- przez Most Grunwaldzki, Plac Społeczny, Oławską,
	</li>
	<li>koszt: <br>
	- wg spalania,
	</li>
	<li>czas: <br>
	- 4 minuty (stan wtorek 13:30, „ruch mniejszy niż zwykle”)
	</li>
	</ul>
	'''
	html_5 = '''
	<h1>Pieszo</h1>
	<ul>
	<li>trasa: <br>
	- przez most Grunwadzki, następnie wzdłuż Urzędu Wojewódzkiego, przez Park
	Słowackiego i Aleję Słowackiego. <br> Czas: 21 minut, dystans 1.6 km. <br>
	- przez most Grunwaldzki, następnie przez Plac Powstańców Warszawy i Aleję
	Słowackiego. <br> Czas: 21 minut, dystans: 1.6 km. <br>
	- most Grunwaldzki, plac Powstańców Warszawy, Zygmunta Krasińskiego, Traugutta,
	Podwale, Promenada Staromiejska. <br> Czas: 22 minuty, dystans: 1.6 km.
	</li>
	</ul>
	'''
	Html = [html_1, html_2, html_3, html_4, html_5]
	Heights = [320, 380, 230, 250, 350]
	icons = ['fa-bus', 'fa-bicycle', 'fa-lemon', 'fa-car', 'fa-male']
	for html, layer, h, i in zip(Html, Layers, Heights, icons):
		iframe = folium.IFrame(html,
							width = 400,
							height = h)
		popup = folium.Popup(iframe,
							max_width = 400)
		icon = folium.Icon(color = "green", icon = i, prefix = 'fa')
		if i == 'fa-lemon':
			icon = folium.Icon(color = "lightgreen")
		marker = folium.Marker([51.1114585, 17.0602199],
						popup = popup, icon = icon).add_to(layer)

	# dodawanie warstw do mapy
	L1.add_to(myMap)
	L2.add_to(myMap)
	L3.add_to(myMap)
	L4.add_to(myMap)
	L5.add_to(myMap)
	L6.add_to(myMap)
	LC.add_to(myMap)
	return(myMap)

overlayGPX([['auto1.gpx', 'auto2.gpx', 'auto3.gpx'], 
	['rower1.gpx', 'rower2.gpx', 'rower3.gpx'], 
	['pieszo1.gpx', 'pieszo2.gpx', 'pieszo3.gpx'], 
	['auto1.gpx', 'auto2.gpx', 'auto3.gpx'],
	['pieszo1.gpx', 'pieszo2.gpx', 'pieszo3.gpx']], 
	['#0033ff', '#336600', '#00FF00', '#FF0000', '#00ff33'], 
	['Trasa MPK', 'Trasa rowerowa', 'Trasa hulajnogi', 
	'Trasa samochodu', 'Trasa piesza'], 16).save("map.html")
