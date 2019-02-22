import datetime
import json
import os
import re
import sys
import urllib
import urllib2
import uuid
import config
from traceback import format_exc

now = datetime.datetime.now()


def download(download_url, dir_name):
    """Downloads the file using the url"""
    try:
        dir_ = now.strftime("/Users/user/Desktop/%Y/%B/%d/{}/".format(dir_name))
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        download_file_name = '{}{}.gif'.format(dir_, uuid.uuid4().__str__())
        urllib.urlretrieve(str(download_url), download_file_name)
        print (".")
    except IOError as io:
        print (io)
        # print (format_exc())
    except OSError as o:
        print (o)
    except:
        print (sys.exc_info())
        print (format_exc())


def fetch_info(query_input, limit="1"):
    """Fetching the gif data using API and then proceeds to download"""
    url = (config.gify_url).format(query_input, config.api_key, limit)
    try:
        data = json.loads(urllib2.urlopen(url).read())# data_gathering
    except urllib2.HTTPError as he:
        print (he)
        print ("HTTP Error")
        return
    except urllib2.URLError as ue:
        print ue
        print ("Network down or Not connected to the internet")
        return
    except:
        print (sys.exc_info())
        return

    payload = data['data']

    if not payload:
        print ("Gif not found")
        return
    file_name = str(uuid.uuid4()) + ".csv" #file name generation
    dir_name = query_input + "_" + (str(uuid.uuid4())[-9:-1:]) #directory name generation
    with open(file_name, "w") as csvFile:
        print ("File Successfully created")
        print ("File name :" + file_name)
        print ("Directory name:" + dir_name)
        for l, i in enumerate(payload): #iteratin through the data
            try:
                gif_id = i.get('id')
                gif_url = i.get('url')
                if not gif_id or not gif_url:
                    print ("Key (id or url) Missing at gif {}".format(l))
                    continue
                csv_line = '{},{}\n'.format(gif_id, gif_url)
                csvFile.write(csv_line)   #writing it to the file
                download_url = i.get('images', {}).get('downsized', {}).get('url')
                if not download_url:
                    print ("Download url is missing")
                    continue
                download(download_url, dir_name)

            except KeyError as ke:
                print (ke)
                print ("Key error")
                continue
                # print format_exc()
            except:
                print (sys.exc_info())
                # print (format_exc())
        print ("Downloaded successfully!!!")


def input_function():
    """Gets the input from the user"""
    try:
        print ("Enter the query :")
        a = raw_input()
        a = re.sub(r'[\s]', '', a).strip()
        print ("Enter the limi""t:")
        b = raw_input()

        while not a or not a.isalnum():
            print ("Enter the query to be searched:")
            a = raw_input()
            a = re.sub(r'[\s]', '', a).strip()

        while not b or not b.isdigit() or 0 > int(float(b)) >= 30:
            print ("Enter the limit:")
            b = raw_input()

        if int(b) <= 0 or 0 > len(a) > 45:
            print ("Give a valid input.")
            input_function()

            return

        fetch_info(str(a), str(b))

    except ValueError as v:
        print (v)
        input_function()


try:
    input_function()
except Exception as e:
    print (format_exc(), str(e))
