from django.shortcuts import render
from django.http.response import StreamingHttpResponse
import cv2
import threading
from django.views.decorators import gzip
import face_recognition

def face(request):
    try:
        c=cideo()
        print('hi')
        print('hi1')
        return StreamingHttpResponse(live(c),
					content_type='multipart/x-mixed-replace; boundary=frame')
    except:
        pass

class cideo(object):
    def __init__(self) -> None:
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,f=self.video.read()
        f_small=cv2.resize(f,(0,0),fx=0.25,fy=0.25)
        all=face_recognition.face_locations(f_small,model='hog',number_of_times_to_upsample=1)
        all_enc=face_recognition.face_encodings(f_small,all)
        for cur_loc,cur_enc in zip(all,all_enc):
            t,r,b,l=cur_loc
            name='unknown'
            t*=4
            r*=4
            b*=4
            l*=4
            cv2.rectangle(f,(l,t),(r,b),(0,0,255),2)
            font=cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(f,name,(l,b),font,0.5,(255,255,255),1)
        _,jpeg=cv2.imencode('.jpg',f)
        return jpeg.tobytes()


def hm(request):
    return render(request,'face/face.html')

def live(camera):
    print('hi2')
    while(True):
        f=camera.get_frame()
        yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n\r\n')

# Create your views here.
