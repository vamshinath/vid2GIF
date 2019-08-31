from moviepy.editor import VideoFileClip,concatenate,vfx
import sys,os

from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor

def isValid(vid):
	try:
		clp= VideoFileClip(vid)
		dur = clp.duration < 10
		del clp
		return [vid,dur]
	except Exception as e:
		return [False,False]

def time_symetrize(clip):
	return concatenate([clip, clip.fx( vfx.time_mirror )])

def rename(fl):

	clp= VideoFileClip(fl).resize(0.85).fx(time_symetrize)
	clp.write_gif("/media/vamshi/05FF22A33F497072/"+fl.replace(" ","_").split(".")[0]+".gif")
	del clp
	os.remove(fl)

dr = sys.argv[1]
os.chdir(dr)
files = os.listdir()
onlyFiles = list(filter(lambda x:os.path.isfile(x) and ".mp4" in x,files))

smallVids=[]

for vid in onlyFiles:
	if isValid(vid)[1]:
		smallVids.append(vid)

print("No.of Files:",len(smallVids))

executor = ProcessPoolExecutor(5)
future_to_url = {executor.submit(rename,vid): vid for vid in smallVids}

