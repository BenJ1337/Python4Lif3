import os, json, urllib2, time, random, datetime, re

def createResourceFolder( actual_dir, resource_dir ):
	path = os.path.join(actual_dir, resource_dir)
	#Erzeugt Resource Ordner, wenn noch nicht erzeugt.
	if not os.path.exists(path):
		os.makedirs(path)
	else:
		print("# Resource folder already exits.")

def createGameFolder( actual_dir, resource_dir, game_name ):
	path = os.path.join(actual_dir, resource_dir, game_name)
	#Erzeugt Game Ordner, wenn noch nicht erzeugt.
	if not os.path.exists(path):
		os.makedirs(path)
	else:
		print("# Game folder already exits.")

def createDownloadResourceFolder( actual_dir, resource_dir, game_name):
	content_of_gamefolder = os.listdir( os.path.join(actual_dir, resource_dir, game_name) )
	id = 0

	if ( len( content_of_gamefolder ) == 0):
		path = os.path.join( actual_dir, resource_dir, game_name, str(id) )
		os.makedirs(path)
		return 0
	else:
		path = os.path.join( actual_dir, resource_dir, game_name , str( len( content_of_gamefolder ) ) )
		os.makedirs(path)
		return len( content_of_gamefolder )

def downloadMarketResources( actual_dir, resource_dir, game_name, game_id, number_of_items_in_one_json, start_item ):

	id = createDownloadResourceFolder( actual_dir, resource_dir, game_name )
	content_of_gamefolder = os.path.join(actual_dir, resource_dir, game_name + str( id ) + "info.txt")

	startzeitpunkt = time.localtime()
	datei_out = open(content_of_gamefolder, "w")
	datei_out.write( "Startzeitpunkt: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" )
	datei_out.close()	

	content_of_gamefolder = os.path.join(actual_dir, resource_dir, game_name, str( id ))

	down_link = 'http://steamcommunity.com/market/search/render/?query=&start=' + str( start_item ) + '&count=' + str( number_of_items_in_one_json ) + '&search_descriptions=0&sort_column=price&sort_dir=asc&appid=' + str( game_id )

	try:	
		response 				= urllib2.urlopen( down_link )
		data 					= json.load(response)  		
	except Exception:
		print("site not available")

	number_of_sites = data["total_count"]
	print( str( number_of_sites ) )

	index = 0
	for i in range(0, number_of_sites, 100 ):
		print(str(i))

		down_link = 'http://steamcommunity.com/market/search/render/?query=&start=' + str( i ) + '&count=' + str( number_of_items_in_one_json ) + '&search_descriptions=0&sort_column=price&sort_dir=asc&appid=' + str( game_id )
		try:	
			response 				= urllib2.urlopen( down_link )
			data 					= json.load(response)  	

			content_of_gamefolder 	= os.path.join(actual_dir, resource_dir, game_name, str( id ), "items" + str( index ) + ".json")		
			datei_out = open(content_of_gamefolder, "w")
			datei_out.write(json.dumps(data))
			datei_out.close()	

		except Exception:
			print("site not available")

		index += 1
		time.sleep( random.randint(15,25) )

	endzeitpunkt = time.localtime()
	diffenenz = time.mktime( endzeitpunkt ) - time.mktime( startzeitpunkt )
	content_of_gamefolder = os.path.join(actual_dir, resource_dir, game_name + str( id ) + "info.txt")
	datei_out = open(content_of_gamefolder, "a")
	datei_out.write( "Endzeitpunkt: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n" + "Dauer: " + str( diffenenz/60 ) + " min" )
	datei_out.close()

def createList( actual_dir, resource_dir, game_name, game_id, id ):
		content_of_gamefolder = os.path.join( actual_dir, resource_dir, game_name, str( id ) )

		def stellen(wert):
			if (wert > 0):
				return 1+stellen(wert/10)
			else:
				return 0

		def sucheMatchingString(suchString, quellString):
			suchStringREG = re.compile(suchString)
			return ( ( re.findall( suchStringREG, quellString ) ) )

		def korrigiereNamen(quellStringArray):
			try: 
				for i in range(len(quellStringArray)):
					quellStringArray[i] = re.sub(r'%2A', '*', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%20', ' ', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%21', '!', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%26', '&', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%27', "'", quellStringArray[i])
					quellStringArray[i] = re.sub(r'%28', '(', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%29', ')', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%2C', ',', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%3A', ':', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%40', '@', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%7C', '|', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%E2%84%A2', '(TM)', quellStringArray[i])
					quellStringArray[i] = re.sub(r'%E2%98%85', '*', quellStringArray[i])
			except Exception:
				print("index out of range: ersetzen")

			return quellStringArray

		zusammenfassung_folder = os.path.join( actual_dir, game_name + ".txt")
		datei_out = open(zusammenfassung_folder , "w")
		datei_out.close()

		datei_out = open(zusammenfassung_folder , "a")

		items = os.listdir( content_of_gamefolder )
		for item in items:
			items_data = os.path.join(content_of_gamefolder, item)
			print( items_data )

			datei_in 	= open( items_data , "r")
			data 		= datei_in.read()
			data 		= json.loads(data)

			item_namen = sucheMatchingString('<a class=\\"market_listing_row_link\\" href=\\"http://steamcommunity.com/market/listings/' + str(game_id) + '/(.*)\\" id=\\"resultlink_', data["results_html"])			
			item_anzahl = sucheMatchingString('<span class=\\"market_listing_num_listings_qty\\">(.*)</span>', data['results_html'])
			item_preis = sucheMatchingString('<span class=\\"normal_price\\">(.*)</span>', data['results_html'])

			item_namen = korrigiereNamen( item_namen )
			
			abstandNachName = 75
			abstandNachPreis = 20

			for i in range( 0, len(item_namen) ):
				ausgabe = 'Name: '
				ausgabe += item_namen[i]
				index = len( item_namen[i] )
				while( index < abstandNachName ):
					ausgabe += ' '
					index += 1
				ausgabe += item_preis[i]
				index = len( item_preis[i] )
				while( index < abstandNachPreis ):
					ausgabe += ' '
					index += 1
				ausgabe += "#" + item_anzahl[i] + "\n"
				print( ausgabe )
				datei_out.write( ausgabe )


		datei_out.close()


if __name__ == "__main__":
	#properties
	#C:\....\folder
	actual_dir 	 				= os.path.abspath(".")
	resource_dir 				= "Resources"
	game_name 	 				= "PLAYERUNKNOWN'S BATTLEGROUNDS"
	game_id 	 				= "578080"
	number_of_items_in_one_json = 100
	start_item 					= 0
	

	#createResourceFolder( actual_dir, resource_dir )
	#createGameFolder( actual_dir, resource_dir, game_name )
	#downloadMarketResources( actual_dir, resource_dir, game_name, game_id, number_of_items_in_one_json, start_item )
	createList( actual_dir, resource_dir, game_name, game_id, 0 )
