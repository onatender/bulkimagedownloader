import json
import threading
import time
import requests
import os

def fetch_photos(per_page, page):
    print(f"Request: per_page={per_page} & page={page}")
    params["per_page"] = per_page
    params["page"] = page
    rq = requests.get(url, params)
    data = json.loads(rq.content)
    return data


def get_extension(link):
    extension = ""
    link = link[::-1]
    for char in link:
        if char == ".":
            return extension[::-1]
        else:
            extension += char


def get_max_resolution(photo):
    resolutions = ("l", "c", "z", "m", "w", "n", "s", "t", "q", "sq")
    for resolution in resolutions:
        if f"url_{resolution}" in photo:
            return photo[f"url_{resolution}"]

def download_photo(link, path):
    try:
        getphoto = requests.get(link).content
        with open(path, "wb") as file:
            file.write(getphoto)
    except:
        pass


def create_folder(path):
    global folder
    folder = f"{what.replace(' ','-')}_photos"
    if not os.path.exists(folder):
        os.mkdir(folder)

threads = []

def download_all_photos(photos, page, perpage):
    global photo_id
    photo_index = 1
    for photo in photos:
        link = get_max_resolution(photo)
        path = f"{folder}/{photo_id}.{get_extension(link)}"
        thread = threading.Thread(target=dfoto_thr, args=(link,path,page,perpage,photo_index,))
        thread.start()
        threads.append(thread)
        photo_index += 1
        photo_id += 1


def dfoto_thr(link,path,page,perpage,photo_index):
    download_photo(link, path)
    print(
        f"{path} downloaded. page={page} & per_page={perpage} & photo_index={photo_index}"
    )



def check_count():
    data = fetch_photos(0, 1)
    total_count = data["photos"]["total"]

    if howmany > total_count:
        print(
            f"{howmany} is greater than {total_count} which is present in the database. {total_count} photos will be downloaded."
        )
    else:
        print(
            f"{total_count} photos found in the database, {howmany} photos will be downloaded."
        )


def seperate(num):
    tofetch = {}
    perpages = [500, 1]
    for perpage in perpages:
        tofetch[str(perpage)] = num // perpage
        num = num % perpage
    return tofetch


def get_minimum_page(downloaded, todownload):
    if downloaded == 0: return 1
    multiplier = 1
    while multiplier * todownload < downloaded:
        multiplier += 1
    return multiplier + 1

def download_fetchlist(tofetch):
    for page in range(tofetch["500"]):
        data = fetch_photos(500, page + 1)
        photos = data["photos"]["photo"]
        print(page)
        download_all_photos(photos, page + 1, 500)

    downloaded = tofetch["500"] * 500

    page = get_minimum_page(downloaded, tofetch["1"])
    data = fetch_photos(tofetch["1"], page)
    photos = data["photos"]["photo"]
    download_all_photos(photos, page, tofetch["1"])

def set_resolution_limits(min,max):
    resolution_list = []
    flag = False
    for resolution in ('url_sq','url_q','url_t','url_s','url_n','url_w','url_m','url_z','url_c','url_l'):
        if resolution == min: flag=True
        if flag: resolution_list.append(resolution)
        if resolution == max: break
    params["extras"] = ",".join(resolution_list)  
    
def set_queries(wh,hm,ak):
    global what
    global howmany
    what = wh
    howmany = hm
    params["text"] = what
    params["api_key"] = ak

what = None
folder = None
howmany = 0
api_key = None
photo_id = 1
url = "https://api.flickr.com/services/rest"
params = {
    "sort": "relevance",
    "parse_tags": 1,
    "extras": "url_sq,url_q,url_t,url_s,url_n,url_w,url_m,url_z,url_c,url_l",
    "per_page": 1,
    "page": 1,
    "lang": "en-US",
    "text": what,
    "method": "flickr.photos.search",
    "api_key": api_key,
    "format": "json",
    "hermes": 1,
    "hermesClient": 1,
    "reqId": "bebfd350-fc39-43fe-85e1-7ab3c3f10650",
    "nojsoncallback": 1,
}


api_key = input("Flickr Api Key:")
obj = input("What do you want to download? :")
cnt = int(input("How many do you want to download? :"))+1
tstart = time.time()
set_queries(obj,cnt,api_key)
create_folder(folder)
set_resolution_limits('url_sq','url_l')
check_count()
tofetch = seperate(howmany)
download_fetchlist(tofetch)

for thread in threads:
    thread.join()

print("All images has been downloaded in ",time.time()-tstart)



