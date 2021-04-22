import requests
import json
import random
import shutil
import gzip
import re
import sys
from urllib.parse import urljoin
from urllib.request import Request, urlopen

url = 'https://webapi.ctfile.com/getfile.php?path=f&f=402712-493096506-583e68&passcode=2021&token=false&r=0.8967800232997811&ref='

headers = {
           # 'accept': '*/*',
           # 'accept-encoding': 'gzip, deflate, br',
           # 'accept-language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2',
           # 'content-length': '0',
           # 'content-type': 'application/x-www-form-urlencoded;',
           #'cookie':'PHPSESSID=in73uhbu439pg7flt8k1s41f53; pass_f493096506=2021',
           'host':'webapi.ctfile.com',
           'origin':'http://down.yabook.org',
           'referer':'http://down.yabook.org/f/402712-493096506-583e68',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}


resp=requests.get(url, headers=headers)
file_link = resp.json()
print(file_link)
#print(file_link['file_chk'])


def parse_params(file):
    """
    Get required params from webpage.
    """
    file_data = file
    filename = file_data['file_name']
    userid = file_data['userid']
    file_id = file_data['file_id']
    folder_id = file_data['file_dir']
    file_chk = file_data['file_chk']
    mb = 0  # not mobile
    app =0
    code = 200

    verifycode = ''
    rd = random.random()

    return userid, filename, file_id, folder_id, file_chk, mb, app, verifycode, rd

userid, filename, file_id, folder_id, file_chk, mb, app, verifycode, rd = parse_params(file_link)
get_file_api = f"/get_file_url.php?uid={userid}&fid={file_id}&folder_id={folder_id}&file_chk={file_chk}&mb={mb}&app={app}&acheck=1&verifycode={verifycode}&rd={rd}"
baseurl="https://webapi.ctfile.com"+get_file_api
print(baseurl)
baseurl2='https://webapi.ctfile.com/get_file_url.php?uid=402712&fid=493096506&folder_id=0&file_chk=8f1c7609cec0e043049d646914dbc84e&mb=0&app=0&acheck=1&verifycode=&rd=0.015085460542676454'

resp3=requests.get(baseurl)
file_link2 = resp3.json()
print(file_link2['downurl'])

def download_file(url, file):
    local_filename = filename
    # NOTE the stream=True parameter below
    # with requests.get(url, stream=True) as r:
    #     with open(local_filename, 'wb') as f:
    #         shutil.copyfileobj(r.raw, f)
    with requests.get(url,  stream=True) as r:
        r.raise_for_status()

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                if chunk:
                    f.write(chunk)
    return local_filename

download_file(file_link2['downurl'], filename)
# request = Request(baseurl,headers=headers)
# data_bytes = gzip.decompress(urlopen(request).read())
# data = json.loads(data_bytes)
# downurl = data.get('downurl')
# if downurl:
#     results.append(downurl)
#
# print("\t".join(results), file=output_stream)
# output_stream.close()
