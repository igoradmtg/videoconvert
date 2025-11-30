#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from moviepy.editor import *
from moviepy.editor import TextClip,VideoFileClip, concatenate_videoclips
from skimage.filters import gaussian
clip_finish_second = 5
video_resize_height = 320
clip_name = r"Z:\001\Video\watching-my-daughter-go-black-13-scene-3.540p.mp4"
fname_tmp_mp4 = r"test.mp4"
ffmpeg_params = ['-crf', '18']
font_name = 'lcdnova.ttf'
fontsize_intro = 100 # Размер шрифта для интро и аутро


def blur(image):
    """ Returns a blurred (radius=2 pixels) version of the image """
    return gaussian(image.astype(float), sigma=8)
    
    
def intro1(fps,text_intro) :
    global main_clip_size, fontsize_intro, font_name
    duration_intro = 3 # Длительность текстового клипа
    logo1 = (TextClip(txt=text_intro,color="#AA0000", align='West',fontsize=fontsize_intro,font = font_name).set_duration(duration_intro).margin(right=8, top=8, opacity=0).set_pos(("center","center"))) # (optional) logo-border padding.set_pos(("right","top")))
    return CompositeVideoClip([logo1.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255])], size=main_clip_size, bg_color = [255,255,255]).set_fps(fps)    

def intro_clip(fps,text_intro,start_intro,duration_intro) :
    global main_clip_size, fontsize_intro, font_name
    #duration_intro = 4 # Длительность каждого текстового клипа
    logo1 = (TextClip(txt=text_intro,color="#FFFFFF", align='West',fontsize=fontsize_intro,font = font_name).set_start(start_intro).set_duration(duration_intro).margin(right=8, top=8, opacity=0).set_pos(("center","center")).crossfadein(0.5).crossfadeout(0.5)) # (optional) logo-border padding.set_pos(("right","top")))
    return logo1

clip_tmp = VideoFileClip(clip_name).crop(x1=0, y1=0, x2=960,y2=507).resize(height = video_resize_height)
W = clip_tmp.w
H = clip_tmp.h
main_clip_size = (W, H)
fps = clip_tmp.fps
clipDuration = clip_tmp.duration 
print(f"Duration: {clipDuration}")

clip_time = 260
subclip = (clip_tmp.subclip(clip_time,(int(clip_time)+clip_finish_second)))

clip_time = 640
subclip2 = (clip_tmp.subclip(clip_time,(int(clip_time)+clip_finish_second))).fl_image(blur)

clip_time = 940
subclip3 = (clip_tmp.subclip(clip_time,(int(clip_time)+clip_finish_second))).fl_image(blur)

clip_time = 1240
subclip4 = (clip_tmp.subclip(clip_time,(int(clip_time)+clip_finish_second))).fl_image(blur)
subclip_out1 = concatenate_videoclips([subclip,subclip2,subclip3,subclip4])

intro_clips = []
intro_clips.append( subclip_out1 )
intro_clips.append( intro_clip(fps,'t.me/tnfun',0,3) )
intro_clips.append( intro_clip(fps,"жена",3,3) )
intro_clips.append( intro_clip(fps,"изменяет",6,3) )
intro_clips.append( intro_clip(fps,"мужу",9,3) )
intro_clips.append( intro_clip(fps,"с большими",12,3) )
intro_clips.append( intro_clip(fps,"с черными",15,3) )
intro_clips.append( intro_clip(fps,'t.me/tnfun',18,2) )

subclip_out2 = CompositeVideoClip(intro_clips)
subclip_out2.write_videofile(fname_tmp_mp4,temp_audiofile="test_concatenate.m4a",remove_temp=True, preset = "veryslow", ffmpeg_params = ffmpeg_params, audio_codec="aac", threads=3, write_logfile = True)

