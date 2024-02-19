import json
import requests
import os

class ImageDownloader:

    def fetch_photos(self,per_page, page):
        print(f"Request: per_page={per_page} & page={page}")
        self.params["per_page"] = per_page
        self.params["page"] = page
        rq = requests.get(self.url, self.params)
        data = json.loads(rq.content)
        return data


    def get_extension(self,link):
        extension = ""
        link = link[::-1]
        for char in link:
            if char == ".":
                return extension[::-1]
            else:
                extension += char


    def get_max_resolution(self,photo):
        resolutions = ("l", "c", "z", "m", "w", "n", "s", "t", "q", "sq")
        for resolution in resolutions:
            if f"url_{resolution}" in photo:
                return photo[f"url_{resolution}"]

    def download_photo(self,link, path):
        getphoto = requests.get(link).content
        with open(path, "wb") as file:
            file.write(getphoto)


    def create_folder(self):
        global folder
        folder = f"{what.replace(' ','-')}_photos"
        if not os.path.exists(folder):
            os.mkdir(folder)


    def download_all_photos(self,photos, page, perpage):
        photo_index = 1
        for photo in photos:
            link = self.get_max_resolution(photo)
            path = f"{folder}/{self.photo_id}.{self.get_extension(link)}"
            self.download_photo(link, path)
            print(
                f"{path} downloaded. page={page} & per_page={perpage} & photo_index={photo_index}"
            )
            self.photo_id += 1
            photo_index += 1


    def check_count(self):
        data = self.fetch_photos(0, 1)
        self.total_count = data["photos"]["total"]

        if howmany > self.total_count:
            print(
                f"{howmany} is greater than {self.total_count} which is present in the database. {self.total_count} photos will be downloaded."
            )
        else:
            print(
                f"{self.total_count} photos found in the database, {howmany} photos will be downloaded."
            )


    def seperate(self,num):
        tofetch = {}
        perpages = [500, 1]
        for perpage in perpages:
            tofetch[str(perpage)] = num // perpage
            num = num % perpage
        return tofetch


    def get_minimum_page(self,downloaded, todownload):
        if downloaded == 0: return 1
        multiplier = 1
        while multiplier * todownload < downloaded:
            multiplier += 1
        return multiplier + 1

    def download_fetchlist(self,tofetch):
        for page in range(tofetch["500"]):
            data = self.fetch_photos(500, page + 1)
            photos = data["photos"]["photo"]
            print(page)
            self.download_all_photos(photos, page + 1, 500)

        downloaded = tofetch["500"] * 500

        page = self.get_minimum_page(downloaded, tofetch["1"])
        data = self.fetch_photos(tofetch["1"], page)
        photos = data["photos"]["photo"]
        self.download_all_photos(photos, page, tofetch["1"])

    def set_resolution_limits(self,min,max):
        resolution_list = []
        flag = False
        for resolution in ('url_sq','url_q','url_t','url_s','url_n','url_w','url_m','url_z','url_c','url_l'):
            if resolution == min: flag=True
            if flag: resolution_list.append(resolution)
            if resolution == max: break
        self.params["extras"] = ",".join(resolution_list)  
        
    def set_queries(self,wh,hm):
        global what
        global howmany
        what = wh
        howmany = hm
        self.params["text"] = what
        
    def __init__(self,what,howmany,minres,maxres):
        self.what = what
        self.folder = None
        self.howmany = howmany
        self.api_key = "91e84aadbea4c0809f377b52a306b009"
        self.photo_id = 1
        self.url = "https://api.flickr.com/services/rest"
        self.params = {
            "sort": "relevance",
            "parse_tags": 1,
            "extras": "url_sq,url_q,url_t,url_s,url_n,url_w,url_m,url_z,url_c,url_l",
            "per_page": 1,
            "page": 1,
            "lang": "en-US",
            "text": what,
            "method": "flickr.photos.search",
            "api_key": self.api_key,
            "format": "json",
            "hermes": 1,
            "hermesClient": 1,
            "reqId": "bebfd350-fc39-43fe-85e1-7ab3c3f10650",
            "nojsoncallback": 1,
        }

        self.set_queries(self.what,self.howmany)
        self.create_folder()
        self.set_resolution_limits(minres,maxres)
        self.check_count()
        self.tofetch = self.seperate(howmany)
        self.download_fetchlist(self.tofetch)
        print("All images has been downloaded!")


wh = input("What do you want to download? :")
hm = input("How many do you want to download? :")
doit = ImageDownloader(wh,hm,"url_sq","url_l")



