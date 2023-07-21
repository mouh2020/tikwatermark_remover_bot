from requests import get,Response,post
import random,time,re

def download_video(tiktok_link) : 
    url = "https://tikwatermark.p.rapidapi.com/video_without_watermark"
    querystring = {"video_link":tiktok_link,
                   "is_share_link":"false"}

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "c646e4968amsh1a35028fd78eca6p170e36jsn1a2cd1eb640b",
        "X-RapidAPI-Host": "tikwatermark.p.rapidapi.com"
    }
    try :
        response = post(url=url,
                        params=querystring,
                        headers=headers)
        return response.json().get("no_watermark_video_link")
    except  :
        pass


def get_video_link_from_share_link(tiktok_link) : 
    attempts = 0 
    while attempts < 3 :
        try : 
            response = get(url=tiktok_link,
                           allow_redirects=True)
            return response.url
        except Exception as e :
            attempts+=1
            time.sleep(1)
            pass    

def get_valid_link(tiktok_link):
    pattern = r"video/(\d+)"
    match = re.search(pattern, tiktok_link)
    if match:
        video_id = match.group(1)
        return tiktok_link
    return  get_video_link_from_share_link(tiktok_link)