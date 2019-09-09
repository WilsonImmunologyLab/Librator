load /Users/leil/Documents/Projects/Librator/Librator/PDB/4hmg.pdb
as cartoon
show mesh
bg_color white
color lightorange
sel ABS-A, resi 122+126+127+128+129+130+131+132+133+137+141+142+143+144
sel ABS-B, resi 155+156+157+158+159+160+164+186+188+189+190+191+192+193+194+195+196+197+198+201
sel ABS-C, resi 52+53+54+275+276
sel ABS-D, resi 174+182+207+220+226+229+230+242+244
sel ABS-E, resi 62+63+77+81+83
color purple, ABS-A
color yellow, ABS-B
color gray, ABS-C
color chocolate, ABS-D
color green, ABS-E
sel mutation, resi 
color red, mutation
label resi  and name C, ""
set label_size, 25
