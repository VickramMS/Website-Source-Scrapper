import re
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import requests
import base64
import os


print("------------------------------------------------------------------------")
source = input("Enter the url to scrap: ")
print("------------------------------------------------------------------------")
domain = '/'.join(source.split('/')[:-1]) + '/'
os.makedirs('source')
file = open('source/index.html', 'a')
webUrl = urllib.request.urlopen(source)
file.write(webUrl.read().decode("utf-8"))
c = 0
links = []
f = open("source/index.html", "r")
for line in f:
    css = re.findall(r'<link rel="stylesheet" href="(.*?)"',line)
    if css and not css[0] == '#':
        links.append(css[0])

    js = re.findall(r'<script src="(.*?)"',line)
    if js and not js[0] == '#':
        links.append(js[0])

    img = re.findall(r'<img src="(.*?)"',line)
    if img and not img[0] == '#':
        links.append(img[0])

    html = re.findall(r'<a href="(.*?)"',line)
    if html and not html[0] == '#':
        links.append(html[0])

links = list(set(links))
print("------------------------------------------------------------------------")
print("Source Bucket : %s" %(domain))     
print("------------------------------------------------------------------------")
print("Total number of resources %d" %(len(links)))
print('\n'*2)


for link in links:
    #Creating Paths
    if link and not link == '#':
        if len(link.split('/')) != 1:
            filepath = link.split('/')[:-1]
            filepath = '/'.join(filepath)
        else:
            filepath = '.'
        
        filename =  link.split('/')[-1]
        if not os.path.exists('source/' + filepath):
            os.makedirs('source/' + filepath)

    #Creating Files
    if link and not link == '#':
        if filename.split('.')[1] == 'png' or filename.split('.')[1] == 'jpg':
            img_data = base64.b64encode(requests.get(domain + link).content)
            with open('source/' + link, "wb") as fh:
                fh.write(base64.decodebytes(img_data))
        else:
            webUrl = urllib.request.urlopen(domain + link)
            with open('source/' + link, "w") as fh:
                fh.write(webUrl.read().decode("utf-8"))
    c += 1
    print("Resource |%d| collected from %s" %(c, domain + link))
print("Resources Ready")
