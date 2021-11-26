from PiicoDev_Buzzer import PiicoDev_Buzzer
import utime
import gc

def init_Buzzers(mul_addr = [0x5c]):
    buzz = []
    for i in mul_addr:
        buzz.append(PiicoDev_Buzzer(volume=2, addr = i))
    return buzz
        
def loadMusic(filename):
    f = open(filename,'r')
    music = []
    for x in f:
        x = x.replace('\r\n','')
        new_list = x.split(',')
        new_list = list(map(int, new_list))
        try:
            music.append(new_list)
        except MemoryError:
            print('MemErr')
            break
    f.close()
    return music

def playNote(noteLst, buzz):
    buzz[noteLst[0]].tone(noteLst[1],noteLst[3])
    
def playMusic(music, buzz):
    start = utime.ticks_ms()
    curr_time = utime.ticks_ms()
    end_ti = max(i[1] for i in  music)
    i = 0
    looping = True
    while looping: 
        for i,note in enumerate(music):
            curr_time = utime.ticks_ms()
            if utime.ticks_diff(curr_time, start) >= note[2]:
                playNote(note, buzz)
                music.pop(i)
            if len(music) <= 0:
                gc.collect()
                looping = False
                break

