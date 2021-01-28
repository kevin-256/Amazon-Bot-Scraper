import requests
from bs4 import BeautifulSoup
array=[]
url1 = 'https://www.amazon.it/gp/goldbox/ref=gbps_ftr_s-5_8ffd_page_'
url2 = '?gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT,page:'
url3 = ',sortOrder:BY_SCORE,enforcedCategories:425916031,dealsPerPage:60&pf_rd_p=3dcc9ba5-cb56-42e1-ac1e-c26f3b278ffd&pf_rd_s=slot-5&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A11IL2PNWYJU7H&pf_rd_r=DF35VTKNSSCKRR8J0478&ie=UTF8'
product = 'https://www.amazon.it/deal/'
headers = { "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15' }
for i in range(1,500):
	page =requests.get(url1 + str(i) + url2 + str(i) + url3, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	IDs = str(soup)[str(soup).find('sortedDealIDs')+19:str(soup).find('customResponseAttributes')-11]
	IDs = IDs.replace('"',"")
	IDs = IDs.replace(' ',"")
	IDs = IDs.replace('\n',"")
	IDs = IDs.split(",")
	if IDs==['']:
		break
	for ID in IDs:
		page =requests.get(product + ID, headers=headers)
		soup = BeautifulSoup(page.content, 'html.parser')
		file = open("index.html", "w")
		file.write(str(soup))
		file.close()
		title=""
		price=""
		discount=""

		try:
			title = soup.find(id="productTitle").get_text()
			title = title.replace("\n", "")
		except:
			1+1
		try:
			price = soup.find(id="priceblock_dealprice").get_text()
			price = price.replace("\n", "")
			price = price.replace(",", ".")
			price = price[0:len(price)-2]
		except:
			1+1
		try:
			discount = soup.find(id="dealprice_savings")
			discount = discount.text.replace('Risparmi:', '')
			discount = discount.replace("\n", "")
			discount = discount[0:discount.find(",")+3]
			discount = discount.replace(",", ".")
		except:
			1+1
		imageLink = soup.find(id="imgTagWrapperId").img.get('src')
		response = requests.get(imageLink)
		file = open("image.png", "wb")
		file.write(response.content)
		file.close()
		if title!='' or price!='' or discount!=None:
			print(str(title) + '\n' + str(price) + '\n' + str(discount) + '\n')
			if title not in array and price!=None and discount!=None:
				percentage=float(discount)/float(price)*100
				array.append([str(title),str(price),str(discount),str(percentage)+"%"])
			else:
				array.append([str(title),str(price),str(discount),None])
	print(array)


