from MidiParser import MidiParser
from MidiData import MidiData
from MidiEventDecoder import MidiEventDecoder
import math
import csv

file_path_midis = 'Midis/'
file_to_convert = 'Midis/MovingCastle'

def midicsv_note_freq(note_num):  # Where mid C is 60
    off_st = -20
    freq = math.pow(2, ((note_num - 49 + off_st)) / 12) * 440
    return freq

def channelise_list(midi_list, channels = 1):
    # Convert from human readable channels to a 0 reference array
    channels = channels - 1
    if channels <= -1:
        print('Too few channels, the function argument "channels" is how many buzzer modules you have')

    if channels > 4:
        print('I havent tested this, let me know how it goes!')
    # Output a list with x channels
    list_w_channels = []    # Send to PiicoDev Buzzers in the form of
                            # [CHx, Frequency;Hz, Start Time;ms, End time;ms]
    channel_OL_flag = False
    channel_counter = [0]
    # Note colision detection - checks if two notes overlap
    while len(midi_list) > 1:    # For all notes check if there is a channel collision
        curr_note_start = midi_list[0][1]
        curr_note_dur = midi_list[0][2]
        removed_note = midi_list.pop(0)
        for j in midi_list:    # Check against all other notes in list
            testing_note_start = j[1]
            testing_note_dur = j[2]
            given_channel = channel_counter
            if (curr_note_start < (testing_note_start + testing_note_dur)) and ((curr_note_start + curr_note_dur) > testing_note_start):
                # A note 'collision' has occurred
                if given_channel[0] <= channels:
                    # Add item to the list that will be output
                    list_w_channels.append(given_channel + removed_note)
                    # Iterate channel counter
                    channel_counter[0] += 1
                    break
                else:
                    # Discard note
                    #Reset channel counter
                    channel_counter[0] = 0
                    channel_OL_flag = True
                    break
            else:
                # No note 'collision' has occurred
                # Continue playing on the next buzzer if available
                if given_channel[0] <= channels:
                    # Add item to list w channels
                    list_w_channels.append(given_channel + removed_note)
                    # Restart channel counter
                    channel_counter[0] = 0
                    break
                else:
                    # Restart channel counter
                    channel_counter[0] = 0
                    channel_OL_flag = True
                    break
    return list_w_channels

def note_lst_create():
    midi_str = file_to_convert + '.mid'
    midiData = MidiData(midi_str)
    note_list = []
    for i in range(midiData.getNumTracks()):
        track = midiData.getTrack(i)
        for note in track.notes:
            # Create data with the notes freq.[Hz] , Start time[ms] and duration[ms]
            parse_list = [round(midicsv_note_freq(note.pitch)), round(note.startTime), round((note.endTime - note.startTime))]
            note_list.append(parse_list)
    return note_list

def lst_to_csv(str_parse):
    csv_str = file_to_convert + '.csv'
    with open(csv_str, "w") as f:
        wr = csv.writer(f, lineterminator='\n')
        wr.writerows(str_parse)
    return 0

lst_to_csv(channelise_list(note_lst_create(), channels = 3))

print('fin')
