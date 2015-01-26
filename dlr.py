from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import pyexiv2
import datetime
import urllib

def mfbLogin(username, password):
    # initiate
    global driver # make it global so that getlink() can use it later
    driver = webdriver.Firefox() # initiate a driver, in this case Firefox
    driver.get('https://m.facebook.com') # go to the url

    # log in
    username_field = driver.find_element_by_name("email") # get the username field
    password_field = driver.find_element_by_name("pass") # get the password field
    username_field.send_keys(username) # enter in your username
    password_field.send_keys(password) # enter in your password
    password_field.submit() # submit it

def scrapeMessages(filename):
    #with help from go|dfish from regex irc
    soup = BeautifulSoup(open(filename))
    
    a = []

    for div in soup.select('div.c'): #find all <div class="c"> tags
        
        href  = div.select('div.messageAttachments > a') #set the href to the selection of messagettachments that is a child of a
        try:
            link = str(href[0]['href']) 
        except IndexError: # if it doesnt exist, continue to the next link, otherwise, convert to string.
            continue
        
        name = str(div.find('strong').text.strip().split()[0]) #find the <strong> tag, strip and split it to get the name of the sender

        abbr = div.find('abbr') #find the abbr tag
        s = abbr['data-store'] #navigate to the datastore
        unixTime   = int(''.join(c for c in s if c.isdigit())) #find the section of numbers, which is our timestamp
        
        a.append((name, link, unixTime)) #append it to the array as a tuple

    return a

def setFilename(number, sender, foldername):
    #take in the foldername, then pad the image number, and add in the senders name
    return '{2}/IMG_{0} - {1}.jpg'.format(str(number).zfill(4), sender, foldername)

def downloadPicture(link, filename):
    # Download the file from `url` and save it locally under `file_name`:
    urllib.urlretrieve(link, filename)

def getLink(pictureURL):
    driver.get(pictureURL) #navigate to the link
    html = driver.page_source #get the source
    
    soup = BeautifulSoup(html) #run it trhough bs
    href = soup.find('a', 'bs bt by') #find the <a class="bs bt by">

    link = str(href['href']) #take the href component from it (our link)
    return link

def setDate(filename, unixTime):
    metadata = pyexiv2.ImageMetadata(filename) #load in the metadata using pyexiv2
    metadata.read() #read it
    key = 'Exif.Photo.DateTimeOriginal' #we want to create this tag

    dateTaken = (datetime.datetime.fromtimestamp(unixTime)) 
    #create a new tag under the key name and set it to the datetime unixtimestamp
    metadata[key] = dateTaken
    metadata.write() #write our changes
    
def end():    
    driver.quit() #easy way to end



def initiateDownload(start, foldername, username, password, sourceArray):
    mfbLogin(username, password) #login
    #because the program would sometimes halt halfway, I edited the loop to be able to retart from a certain step
    for i in range(len(sourceArray)-start):
        name, link, time = sourceArray[i+start] #unpack
        filename = setFilename(i+1+start, name, foldername) #+1 means the images will start from 0001
        downloadPicture(getLink(link), filename)
        setDate(filename, time)

    end()

#create our array of values
messageArray = scrapeMessages('file2.html')#+ scrapeMessages('file1.html')

foldername = str(raw_input('Foldername: '))
start = int(raw_input('Start from: '))
username = str(raw_input('Username: '))
password = str(raw_input('Password: '))

initiateDownload(start, foldername, username, password, messageArray)
