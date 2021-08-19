import requests as r
from time import sleep
from bs4 import BeautifulSoup
import re
import os
import sys

#start of definition section
#cool down to give the target server a break.
def cooldown(time):
    for i in range(1,time+1):
        print(f'cooling down {i}')
        sleep(1)
    print('\n')
#simply create a folder
def new_folder(name):
    if not os.path.exists(str(name)):
        os.mkdir(str(name))
        print(f'"{name}" folder created')
    else:
        print(f'{name} already exists!')

def extract_Url(strings):
	#input
	#<span class="plid">#pl https://konachan.net/post/show/328775</span>
    holder = []
    for i in range(len(strings)):
        temp = str(strings[i])
        temp = temp.replace('<span class="plid">#pl ', '')
        temp = temp.replace('</span>', '')
        holder.append(temp)
    #output
    #https://konachan.net/post/show/328775
    return holder

def get_source(web, path):
    url = web

    #you can view headers on inspect > network > click a file > Headers
    #copy and paste it here
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    
    #The get() method will return a full HTML source from the url you input.
    #It can have optional parameters such as
    # params, allow_redirects, auth, cert
    # cookies, headers, proxies, stream
    # timeout, verify.
    #More at https://www.w3schools.com/PYTHON/ref_requests_get.asp
    response= r.get(url,headers=headers)

    #this line will convert the response received from the server. so we can filter out later
    Bsoup = BeautifulSoup(response.text, 'lxml')

    #this line will find and select all desired path from the big pieces
    urls = Bsoup.select(path)
    print('Requesting HTML source...')
    cooldown(3)
    #extract_Url() will extract the url from the smaller chunk
    #something like this<span class="plid">#pl https://konachan.net/post/show/328775</span>
    
    return extract_Url(urls)

def get_image_url(web, path):
    print('processing image url...')
    url = web
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
    response = r.get(url, headers=headers)
    Bsoup = BeautifulSoup(response.text, 'lxml')
    urls = Bsoup.select(path)

    # similar to get_source(), but specific to get the url. does not return more than 1 urls
    # (.*?) in re module finds the pattern of the link.
    link = re.findall(pattern='href="(.*?)"', string=str(urls))
    cooldown(3)
    return link


def save_image(url, name, folder):
    # print(f'Saving image from {url}')
    file_name = f'{name}.jpg'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
    img_data = r.get(url[0], headers=headers)
    savePath = f"{sys.path[0]}\\{folder}\\{file_name}"
    with open(savePath, 'wb') as f:
        f.write(img_data.content)
        f.close()
    print(f'{name} is saved.')
    cooldown(3)

def main(url, name):
	# Getting specific image links under 
	# #post-list-post > li > div > a > span
	# this will give me a whole bunch of links specific detailed image page.
    posts = get_source(url, path="#post-list-posts > li > div > a > span")

    #imgs check the imgs already exists in the folder,
    #if what is trying to save is already in 'imgs' it will not replace the existing one,
    #and will continue to the next img on line. 
    imgs = []
    for url in posts:
        name = url.split('/')

    #sys.path[0] return the folder this python code is running at.
        path = f"{sys.path[0]}\\{folder_name}"

    #this check the name of files already in the folder
        imgs = os.listdir(path)
        if name[-1]+'.jpg' in imgs:
            print(f'Warning: {name[-1]}.jpg is in folder{folder_name}!!')
            continue
        else:
    		#This line cite the specific image url to save,
    		#similar to get_sources() but this will only return one.
    		#specific url ending with .jpg
            image_url = get_image_url(url, '#highres-show')
            save_image(image_url, name[-1], folder_name)
#end of definition secion

#Start calling here
if __name__ == '__main__':
    print('program starting>>>\nat any time, press ctrl+c to stop the program\n')
    #creating a folder to save this images
    # + str(name) refers to the page number it is at.
    folder_name = 'Jul6_tag_industrial'
    new_folder(folder_name)

    url = input('url: ')
    holder = url
    print(f'\nyou have entered: {holder}\n')

    #how many pages to flip
    for page in range(1,14):
        try:
        #url would be the page to start 
            url = holder
            url = url.replace('1', str(page))
            print(f'\nprocessing url: {url}\n')
            main(url, page)
        except KeyboardInterrupt:
            print('\n\nSTOPING<<<\n\n')
            break