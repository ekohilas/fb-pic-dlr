# fb-pic-dlr
**Facebook conversation mass picture downloader**

The Program consists of 11 modules which will be stated in order that they are used.

Before delving into the program, please note that this was first made for personal use, after being frustrated with not being able to mass download pictures from a facebook conversation, and as such, its techniques may not be up to standards.



**Aquiring the needed sources**

I understand this is a hassle and not user friendly, but its the best I've got.

1. Open a Facebook conversation on m.facebook.com
2. Open the developer tools of your browser and run this script in the console:

    ```
    setInterval(function () {
        document.getElementById('see_older')
            .getElementsByClassName('content')[0].click();
    }, 100);
    ```
3. Depending on the size of the conversation, this may take some time. My conversation was 40,000 messages long, and froze halfway, so I had to do it in 2 chunks. You can leave this running in the background.
4. Save the webpages as html



**Download and installing modules**

For this program you will need:

1. selenium
2. bs4
3. pyexiv2
4. Monzilla Firefox installed into the defualt directory (PATH) unless you somehow bother to get chrome working



**Explaining modules**

1. Logging into m.facebook using selenium

    we use selenium to log into facebook through firefox to be able to access the links from the source file(s).

2. Scraping the data from your html file(s).

    Using beautiful soup we scan throughout the files and return an array of tuples as (name, link, timestamp)
    this may take some time depending on the size of your html file(s).

3. Setting the filename for the file.

    We take in a foldername to save the files to, and use the iteration number and the sender's name for the filename of the pictures.

4. Getting the download link

    We navigate to the link provided by the scraper and effectively "download" the image by taking the link using bs4

5. Downloading the picture using urllib

    now that we have a filename, we use the link provided by the scraper and download the image

6. Setting dateTaken to the image's Exif

    for extra style points, we take the timestamp from the scraper, run it through datetime module and save it to the exif of the image through pyexiv2

7. rinse, repeat, end.

    do all this through a for loop and ending the driver once we have finished.
