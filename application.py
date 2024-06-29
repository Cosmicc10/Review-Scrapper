from flask import Flask,render_template,request
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import requests
from flask_cors import CORS,cross_origin

application=Flask(__name__)
app=application

@app.route('/',methods=['GET','POST'])
def home_page():
    return render_template('index.html')

@app.route('/route',methods=['POST'])
def scrap():
    if(request.method=='POST'):
        try:
            search_string=request.form['search_string'].replace(" ","")
            flipkart_url="https://www.flipkart.com/search?q="+search_string
            link=uReq(flipkart_url)
            flipkartpage=link.read()
            link.close()
            flipkat_html=bs(flipkartpage,"html.parser")
            product_link_maindiv=flipkat_html.find_all("div",{"class":"cPHDOP col-12-12"})
            plink=product_link_maindiv[2]
            halflink=plink.div.div.div.a['href'] 
            product_page_link="https://www.flipkart.com"+halflink
            HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}) 
            product1=requests.get(product_page_link,headers=HEADERS)
            product_html=bs(product1.text,"html.parser") 
            review_class=product_html.find_all("div",{"class":"RcXBOT"})

            filename=search_string+".csv"
            f=open(f"D:/CODING VS/python/Flipkart Scrapper/search history/{filename}",'w+')
            f.close()
        except Exception as stt:
            print("error in scrapper",stt)


        try:
            reviews=[]
            for i in review_class:
                reviews.append(i.div.div.find_all("div",{"class":""})[0].div.text)
        except Exception as at:
            print("reached end",at)
        

        return render_template('result.html',reviews=reviews)
    #reviews[0:(len(reviews)-1)] can also pass this in reviews!
        


if __name__=='__main__':
    app.run(debug=True)
