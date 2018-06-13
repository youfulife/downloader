import subprocess
import time
import sys
import os
import redis
import uuid

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

basedir = os.path.abspath(os.path.dirname(__file__))
# ret_code = subprocess.check_call(['ffmpeg', '-v', 'quiet', '-progress', '/dev/stdout', '-i', m3u8_url, prefix+filename])
url = "https://vdn.vzuu.com/Act-ss-m3u8-ld/48abe817b57f459f8644cadb2f8c8ee7/917d8956-59b4-11e8-888f-0242ac112a17None.m3u8?auth_key=1528885777-0-0-861fad7d58c6e305bf23e2a4a5cbc141&expiration=1528885777&disable_local_cache=0"
# output = basedir + "/test.mp4"
output="{}.mp4".format(uuid.uuid4())
print(output)
cmd = "ffmpeg -v quiet -progress /dev/stdout -i '{input}' {output}".format(input=url, output=output)

# cmd = "cat xxx.txt"
print(cmd)
child1 = subprocess.Popen(cmd, cwd=basedir, shell=True, stdout=subprocess.PIPE)
cmd2 = "grep -e out_time_ms -e progress"
print(cmd2)
child2 = subprocess.Popen(cmd2, shell=True, stdin=child1.stdout, stdout=subprocess.PIPE)
for line in iter(child2.stdout.readline, b''):
    tmp = line.decode('utf-8').strip().split('=')
    
    if tmp[0] == 'out_time_ms':
        out_time_ms = tmp[1]
        print(out_time_ms)
        r.set("x", out_time_ms)
    else:
        if tmp[1] == 'end':
            r.delete("x")
            print("download complete")    
        
    # time.sleep(1)