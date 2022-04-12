from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table_eth = soup.find('table', attrs={'class':'table table-striped text-sm text-lg-normal'}).find('tbody').find_all('tr')

row_length = len(table_eth)

Date =[]
Volume = [] #initiating a list 

for i in table_eth:
    #Date
    Date.append(i.find_all('th')[0].get_text())
            
    #Volume
    Volume.append(i.find_all('td')[1].get_text().strip().replace('$','').replace(',','').replace('.',''))
    
    
#change into dataframe
result = pd.DataFrame({'Date': Date, 'Volume': Volume})

#insert data wrangling here
result['Date'] = result['Date'].astype('datetime64')
result['Volume'] = result['Volume'].astype('float64')
result = result.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{result["Volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = result.plot(figsize = (13,7)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)