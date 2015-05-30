from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import pyexiv2
import datetime
import urllib
#import re

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
    
    print "Loading File into BSoup..."
    soup = BeautifulSoup(open(filename))
    print "File Loaded."
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
        
        print 'Loading... {}'.format(len(a)) #pretty loading formatting for debug
        
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
    href = soup.find('a', 'bq z br bw') #find the <a class="bs bt by"> tag, WARNING, can change
    if href == None:
        href = soup.find('a', 'bp z bq bv')

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

def initiateDownload(continueNumber, countNumber, foldername, username, password, sourceArray):
    print 'Logging in...'
    mfbLogin(username, password) #login
    #because the program would sometimes halt halfway, I edited the loop to be able to retart from a certain photo
    for i in range(len(sourceArray)-continueNumber):
        name, link, time = sourceArray[i+continueNumber] #unpack
        filename = setFilename(i+1+continueNumber+countNumber, name, foldername) #+1 means the images will start from 0001
        downloadPicture(getLink(link), filename)
        setDate(filename, time)
        print "Photo {0} of {1} downloaded.".format(i+1+continueNumber, len(sourceArray))
        
    end()

stringInput = str(raw_input("One line input, leave blank for line by line\nFileName1, FileName2, FolderName, Count from, Continue From, Username, Password\n: "))
if stringInput == '':
    
    fileOne = str(raw_input('First html file: ')) + '.html'
    fileTwo = str(raw_input('Second html file: ')) + '.html'
    #create our array of values, first file, second file
    arrayOne = scrapeMessages(fileOne)
    arrayTwo = scrapeMessages(fileTwo)
    messageArray = arrayOne + arrayTwo
    print 'Total Images: ' + str(len(messageArray))

    foldername = str(raw_input('Foldername: '))
    countStart = int(raw_input('Count from (Filename number start): '))
    contNum    = int(raw_input('Continue from (Array count start, 0 if begining): '))
    username   = str(raw_input('Username: '))
    password   = str(raw_input('Password: '))

else:
    fileOne, fileTwo, foldername, countStart, contNum, username, password = stringInput.split(',')
    fileOne = fileOne + '.html'
    fileTwo = fileTwo + '.html'
    countStart = int(countStart)
    contNum = int(contNum)

arrayOne = scrapeMessages(fileOne)
arrayTwo = scrapeMessages(fileTwo)
messageArray = arrayOne + arrayTwo

print 'Total Images: ' + str(len(messageArray))

initiateDownload(contNum, countStart, foldername, username, password, messageArray)
print "Download Complete"

'''  replacement module for when FB's class names aren't constant
def getLinkRegex(pictureURL):
    driver.get(pictureURL)
    html = driver.page_source
    regex = re.compile('<a href="(https://fbcdn-sphotos-h-a\.akamaihd\.net/[^"]*)')
    rawphotolink = regex.findall(html)
    return parseLink(rawphotolink[0])
'''
