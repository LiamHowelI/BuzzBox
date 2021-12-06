import BuzzerBox # Importing the module for this project

Buzz_addr = [0x5c, 0x09, 0x0a] # Pop in all of the addresses of the buzzer modules

buzz = BuzzerBox.init_Buzzers(Buzz_addr)

music = BuzzerBox.loadMusic('MovingCastle.csv')
BuzzerBox.playMusic(music, buzz)
