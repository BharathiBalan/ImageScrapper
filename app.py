from mimetypes import guess_extension

from selenium import webdriver
import os
from urllib.request import urlretrieve, Request
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route('/')  # route for redirecting to the home page
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/searchImages', methods=['GET','POST'])
@cross_origin()
def searchImages():
    # driver = webdriver.Chrome('E:\Machine Learning\Softwares/chromedriver')
    if request.method == 'POST':
        print("entered post")
        keyWord = request.form['keyword'] # assigning the value of the input keyword to the variable keyword
        keyWord=keyWord.replace(' ','_')
        noofImages = int(request.form['noofImages'])
        print('keword is:',keyWord,' noofImages is:',noofImages)

    else:
        print("did not enter post")
    url = "https://www.google.com/search?q=" + keyWord + "&source=lnms&tbm=isch"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    #driver = webdriver.Chrome(executable_path='E:\Machine Learning\Softwares\chromedriver', chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    #driver=webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(2)
    #data = driver.page_source
    for del_file in os.listdir('static/'):
        #print(del_file)
        if del_file.endswith('.jpeg'):
            #print("need to delete")
            os.remove('static/'+del_file)
    imgs = []
    imgnames=[]
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    a = driver.find_elements_by_css_selector('img.Q4LuWd')
    print(len(a))
    #print('[DRIVER]', a, type(a))
    for b in a:
        #print('[Driver]', b)
        b.click()
        driver.implicitly_wait(1)
        c = driver.find_elements_by_css_selector('img.n3VNCb')
        for d in c:
            e = d.get_attribute('src')
            #print(e, type(e))
            if e not in imgs and 'http' in e:
                #print(len(imgnames),e)
                imgs.append(e)
                imgname=keyWord + str(len(imgs)) + '.jpeg'
                filename = 'static/' + imgname
                #print(filename)
                try:
                    urlretrieve(e,filename)
                    #Request(e, filename, headers={"User-Agent": "Chrome"})
                    imgnames.append(imgname)
                except Exception as abcd:
                    print("error while downloading the image ",e,"\nwith error ",abcd)
            if (len(imgnames)) == noofImages:
                break
        if (len(imgnames)) == noofImages:
            break
        #print("done with this image")
    return render_template('showImage.html', user_images=imgnames)


port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8000) # port to run on local machine
    #app.run(debug=True) # to run on cloud
    app.run(host='0.0.0.0', port=port)