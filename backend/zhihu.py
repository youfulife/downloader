import re
import uuid
import subprocess
import json

import requests

# 下边 cookie 请打开知乎打开浏览器开发者工具随便找一个请求复制 cookie，千万不要泄露出去
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}
# 支持是 'ld' 'sd' 'hd' 分别是低清、中清、高清
QUALITY = 'ld'


def get_video_ids_from_url(url):
    """
    回答或者文章的 url
    """
    html = requests.get(url, headers=HEADERS).text
    # print(html)
    video_ids = re.findall(r'data-lens-id="(\d+)"', html)
    print(video_ids)
    if video_ids:
        return set([int(video_id) for video_id in video_ids])
    return []


def yield_video_m3u8_url_from_video_ids(video_ids):
    for video_id in video_ids:
        HEADERS['Referer'] = 'https://v.vzuu.com/video/{}'.format(video_id)
        HEADERS['Origin'] = 'https://v.vzuu.com'
        HEADERS['Host'] = 'lens.zhihu.com'
        HEADERS['Content-Type'] = 'application/json'
        HEADERS['Authorization'] = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'

        api_video_url = 'https://lens.zhihu.com/api/videos/{}'.format(int(video_id))

        r = requests.get(api_video_url, headers=HEADERS)
        # print(json.dumps(dict(r.request.headers), indent=2, ensure_ascii=False))
        # print(r.text.encode('utf-8').decode('unicode_escape'))
        playlist = r.json()['playlist']
        m3u8_url = playlist[QUALITY]['play_url']
        yield video_id, m3u8_url


def download(url, directory):
    video_ids = get_video_ids_from_url(url)
    m3u8_tuples = list(yield_video_m3u8_url_from_video_ids(video_ids))
    rets = []

    for idx, m3u8_url in m3u8_tuples:
        prefix = directory + '/dist/'
        filename = 'static/video/zhihu/{}.mp4'.format(uuid.uuid4())
        print('download {}'.format(m3u8_url))
        # subprocess.call(['ffmpeg', '-i', m3u8_url, filename])
        ret_code = subprocess.check_call(['ffmpeg', '-i', m3u8_url, prefix+filename])
        if ret_code == 0:
            ret = {
                'status': 'success',
                'video': filename,
                "message": "下载成功"
            }
        else:
            ret = {
                'status': 'error',
                "message": "下载失败，请稍后再试"
            }
        rets.append(ret.copy())
    else:
        return rets


if __name__ == '__main__':
    # 贴上你需要下载的 回答或者文章的链接
    seed = 'https://www.zhihu.com/question/277411517/answer/394112534'
    download(seed)
