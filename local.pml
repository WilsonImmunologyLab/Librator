load /Users/leil/Documents/Projects/Librator/Librator/PDB/4hmg.pdb
as cartoon
show mesh
bg_color white
color lightorange
sel ABS-A, chain A+C+E+G+I+K and (resi 122+126+127+128+129+130+131+132+133+137+141+142+143+144)
sel ABS-B, chain A+C+E+G+I+K and (resi 155+156+157+158+159+160+164+186+188+189+190+191+192+193+194+195+196+197+198+201)
sel ABS-C, chain A+C+E+G+I+K and (resi 52+53+54+275+276)
sel ABS-D, chain A+C+E+G+I+K and (resi 174+182+207+220+226+229+230+242+244)
sel ABS-E, chain A+C+E+G+I+K and (resi 62+63+78+81+83)
color purple, ABS-A
color yellow, ABS-B
color gray, ABS-C
color chocolate, ABS-D
color green, ABS-E
set label_size, 25
