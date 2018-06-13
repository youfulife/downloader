import subprocess
import json


def exec_output(command):
    """
    执行ffmpeg命令并返回所有输出，如果执行失败，抛出FfmpegException
    :param command: ffmpeg命令
    :return: ffmpeg标准输出
    """
    try:
        process = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return process
    except subprocess.CalledProcessError as err:
        raise FfmpegException(err.returncode, err.cmd, err.output)


class FfmpegException(Exception):
    """
    使用ffmpeg报错时抛出
    """

    def __init__(self, returncode, cmd, output=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output

    def __str__(self):
        return "Command '%s' returned non-zero exit status %d" % (self.cmd, self.returncode)


def duration_seconds(url): 
    result = exec_output("ffprobe -v quiet -print_format json -show_format {}".format(url))
    video_info = json.loads(str(result.decode('utf8')))
    duration_seconds = video_info['format'].get("duration", None)
    if duration_seconds is not None:
        return round(float(duration_seconds))
    else:
        return 0


if __name__ == '__main__':
    url = "https://vdn.vzuu.com/Act-ss-m3u8-ld/48abe817b57f459f8644cadb2f8c8ee7/917d8956-59b4-11e8-888f-0242ac112a17None.m3u8?auth_key=1528856898-0-0-6b355374a747cf586f9829125a79ae0f&expiration=1528856898&disable_local_cache=0"
    duration_seconds(url)
    
    