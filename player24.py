#!/usr/bin/python
# RaspiPlayer 480x320
# This is to be used with a 3.5" HDMI touchscreen or equivalent
# Tested with the Raspberry pi 2 and raspbian stretch
# The program must be run within the Lxterminal.
# Current changes include: Selection of folders to be played, or Play everything
# in the USB drive by clicking on Mp3 button.
# Rev2.41 by Granpino

 
import sys, pygame
from pygame.locals import *
import time
import datetime
import subprocess
import os
import glob
import random
#import requests # check internet connection
import socket

pygame.init()

#define colors
cyan = 50, 255, 255
blue = 26, 0, 255
black = 0, 0, 0
white = 255, 235, 235
red = 255, 0, 0
green = 0, 255, 0
silver = 192, 192, 192
gray = 40, 40, 40

#other
#os.system("mount /dev/sda1 /mnt/usbdrive") #setup for USB drive # comes from the mpd-serverice!!! don't use this line!
subprocess.call("mpc random off", shell=True)
subprocess.call("mpc clear", shell=True)
#subprocess.call("mpc volume 65", shell=True) ## use the last Volume set
subprocess.call("mpc update ", shell=True)
subprocess.call("mpc load Radio", shell=True) # nice :D but we would use default MP3

clock = pygame.time.Clock()

mp3 = False
shuffle = False
x = 0
PlsPath = "/var/lib/mpd/playlists/"
PlayList = os.listdir( PlsPath )
CurrPlaylist = " "
play = False

keyboard_open = False
searchstring = ""
search_output_rect = None
search_output_open = False
search_count = 0
search_offset = 0
search_offset_add = 0
search_result_sng = None
search_result_art = None
search_result_alb = None
search_result_yr = None
search_result_list = None
search_select = None


#global album_img
_image = ('/tmp/kunst.png')
album_img = ('150x112.png')
connection = None

#set size of the screen
size = width, height = 480, 320
### change screen mode for troubleshooting purposes
#screen = pygame.display.set_mode(size) #,pygame.FULLSCREEN)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

def search_clean():
	global search_result_sng
	global search_result_art
	global search_result_alb
	global search_result_yr
	global search_result_list
	global search_count
	
	if search_count > 0:
		print("clear lists")
		#search_result_sng.clear()
		#search_result_art.clear()
		#search_result_alb.clear()
		#search_result_yr.clear()
		#search_result_list.clear()
		del search_result_sng[:]
		del search_result_art[:]
		del search_result_alb[:]
		del search_result_yr[:]
		del search_result_list[:]
		search_select = None


def search_output():
	global search_output_open
	global searchstring
	global keyboard_open
	global search_count
	global search_output_rect
	
	global search_result_sng
	global search_result_art
	global search_result_alb
	global search_result_yr
	global search_result_list
	
	global search_offset
	global search_offset_add
	global search_select
	
	search_output_open = True
	keyboard_open = False
	
	screen.fill(black)
	
	y_off = 10
	
	if search_count > 0:
		search_offset_add_cnt = 0
		#13 lines
		line_counter = 0
		for x in search_result_sng:
			if search_offset_add == 0:
				font=pygame.font.Font(None,24)
				label_data=font.render(x, 1, (white))
				screen.blit(label_data,(7,y_off))
				y_off += 20
				
				if line_counter == search_offset:
					print( "SNG : " + search_result_sng[search_offset])
					print( "ART : " + search_result_art[search_offset])
					print( "ALB : " + search_result_alb[search_offset])
					print( "YR  : " + search_result_yr[search_offset])
					print( "LIST: " + search_result_list[search_offset])
					search_select = search_result_list[search_offset]
				line_counter +=1
			else:
				if search_offset_add == search_offset_add_cnt:
					font=pygame.font.Font(None,24)
					label_data=font.render(x, 1, (white))
					screen.blit(label_data,(7,y_off))
					y_off += 20
					line_counter +=1
					
					print( "SNG : " + search_result_sng[search_offset + search_offset_add])
					print( "ART : " + search_result_art[search_offset + search_offset_add])
					print( "ALB : " + search_result_alb[search_offset + search_offset_add])
					print( "YR  : " + search_result_yr[search_offset + search_offset_add])
					print( "LIST: " + search_result_list[search_offset + search_offset_add])
					search_select = search_result_list[search_offset + search_offset_add]
				else:
					search_offset_add_cnt += 1
				
			if line_counter == 11:
				break
		
		y_off += 5
		# #Art:
		# font=pygame.font.Font(None,24)
		# label_data=font.render("Art: " + search_result_art[search_offset], 1, (white))
		# screen.blit(label_data,(20,y_off))
		# y_off += 20
		#Alb:
		#print("ALB_OFFSET:" + str(y_off))
		y_off = 235
		font=pygame.font.Font(None,24)
		label_data=font.render("Album: " + search_result_alb[search_offset + search_offset_add], 1, (white))
		screen.blit(label_data,(30,y_off))
		y_off += 20
		#Yr:
		font=pygame.font.Font(None,24)
		label_data=font.render("Year: " + search_result_yr[search_offset + search_offset_add], 1, (white))
		screen.blit(label_data,(30,y_off))
		y_off += 20
	
	
	else:
		font=pygame.font.Font(None,36)
		label_data=font.render("Nothing found", 1, (white))
		screen.blit(label_data,(100,120))
		y_off += 20
	
	pygame.draw.rect(screen, silver, ( 22, 280, 100, 30),0)
	pygame.draw.rect(screen, silver, (134, 280, 100, 30),0)
	pygame.draw.rect(screen, silver, (246, 280, 100, 30),0)
	pygame.draw.rect(screen, silver, (358, 280, 100, 30),0)
	
	if search_count > 0:
		font=pygame.font.Font(None,36)
		label_data=font.render("UP", 1, (black))
		screen.blit(label_data,(54,282))
		
		font=pygame.font.Font(None,36)
		label_data=font.render("DOWN", 1, (black))
		screen.blit(label_data,(145,282))
		
		font=pygame.font.Font(None,36)
		label_data=font.render("ABORT", 1, (black))
		screen.blit(label_data,(253,282))
		
		font=pygame.font.Font(None,36)
		label_data=font.render("OK", 1, (black))
		screen.blit(label_data,(390,282))
		
		#hinten sauber machen
		pygame.draw.rect(screen, black, ( 480-7, 0, 7, 320),0)
		
		#Rect(left, top, width, height)
		if search_output_rect is None:
			#search_output_rect = pygame.rect.Rect(18, 8, 458, 21)
			search_output_rect = pygame.rect.Rect(5, 8, 458+13, 21)			
		pygame.draw.rect(screen, white, search_output_rect,1)
		
	else:
		font=pygame.font.Font(None,36)
		label_data=font.render("UP", 1, (120,120,120))
		screen.blit(label_data,(54,282))
		
		font=pygame.font.Font(None,36)
		label_data=font.render("DOWN", 1, (120,120,120))
		screen.blit(label_data,(145,282))
		
		font=pygame.font.Font(None,36)
		label_data=font.render("ABORT", 1, (black))
		screen.blit(label_data,(253,282))
		
		font=pygame.font.Font(None,36)
		label_data=font.render("OK", 1, (120,120,120))
		screen.blit(label_data,(390,282))
	
	pygame.display.flip()


def keyboard_key(kb_key):
	global searchstring
	global keyboard_open
	
	#print(kb_key)
	if kb_key is "SPACE":
		searchstring = searchstring + " "
		#print("ADD SPACE")
	else:
		if kb_key == "BACK":
			searchstring = searchstring[:-1]
		else:
			if kb_key == "RETURN":
				
				global search_offset
				global search_count
	
				global search_result_sng
				global search_result_art
				global search_result_alb
				global search_result_yr
				global search_result_list
				global search_select
				
				print("S:=>" + searchstring)
				
				#print("RETURN")
				
				
				search_pattern_list = []
				unwanted_idx = []
				unwanted_idx_cnt = 0
				search_offset = 0
				search_offset_add = 0
				search_count  = 0
				
				search_select = None
				
				
				#search_command = "roll*int"
				#search_command = "roll"
				
				search_command = searchstring
				
				search_command2 = search_command.split("*")
				
				search_command = ""				
				i = 0
				for x in search_command2:
					if i == 0:
						search_command += "\"" + x.lower().strip() + "\""
					else:
						#search_command += "|grep -i \"" + x + "\""
						search_pattern_list += [x.lower().strip()]
					i += 1
				
				print("SEARCH FILE FOR: " + search_command)
				if len(search_pattern_list) > 0:
					print("SEARCH PATTERN :")
					print(search_pattern_list)
				
				if search_command == "\"\"":
					search_count = 0
					search_output()
					return False
				
				#todo: split searchstring and find * to split and grep on it
				#mpc searchplay filename "The Rolling Stones/No Security/01 Intro.mp3"
				#
				#shell_out = subprocess.check_output("mpc -f \"%album% - %artist% - %title%\" search filename roll|grep -i intro", shell=True)
				#shell_out = subprocess.check_output("mpc -f \"%album% - %artist% - %title%\" search filename roll", shell=True)
				#shell_out = subprocess.check_output("mpc -f \"%artist% - %title%\" search filename roll", shell=True)
				#print(shell_out)
				#shell_data = shell_out.splitlines()
				#%originaldate% << not working
				#%date%
				
				#erst mit dem suchmuster auf die blanken dateinamen
				#und mit diesem ergebnis dann die dateils holen
				
				#all(xy in <ERGEBNIS> for xy in <LISTE>
				
				shell_out = subprocess.check_output("mpc search filename " + search_command, shell=True)
				search_result_list = shell_out.splitlines()
				
				shell_out = subprocess.check_output("mpc -f \"%artist% - %title%\" search filename " + search_command, shell=True)
				search_result_sng = shell_out.splitlines()
				
				shell_out = subprocess.check_output("mpc -f \"%artist%\" search filename " + search_command, shell=True)
				search_result_art = shell_out.splitlines()
				
				shell_out = subprocess.check_output("mpc -f \"%album%\" search filename " + search_command, shell=True)
				search_result_alb = shell_out.splitlines()
				
				shell_out = subprocess.check_output("mpc -f \"%date%\" search filename " + search_command, shell=True)
				search_result_yr = shell_out.splitlines()
	
				search_count = len( search_result_list )
				
				if search_count > 0:
					if len(search_pattern_list) > 0:
						print("USE SEARCHPATTERN")
						for search_entry in search_result_list:
							#print(search_entry)
							# if all(search_pattern in search_entry.lower() for search_pattern in search_pattern_list):
								# print("IN :" + search_entry)
							# else:
								# #print("OUT:" + search_entry)
								# unwanted_idx += [unwanted_idx_cnt]
							if not all(search_pattern in search_entry.lower() for search_pattern in search_pattern_list):
								unwanted_idx += [unwanted_idx_cnt]
							unwanted_idx_cnt += 1
					
						for idx in sorted( unwanted_idx, reverse=True):
							del search_result_list[idx]
							del search_result_sng[idx]
							del search_result_art[idx]
							del search_result_alb[idx]
							del search_result_yr[idx]
					else:
						print("NO SEARCHPATTERN")
				
				search_count = len( search_result_list )
				
				# print( "A:" + str(len(search_result_list)))
				# print(unwanted_idx)
				# print(search_result_list)
				# print(search_result_sng)
				# print(search_result_art)
				# print(search_result_alb)
				# print(search_result_yr)
				# print("ENDE")
				# return True
				
				
				# shell_out = subprocess.check_output("mpc -f \"%artist% - %title%\" search filename " + search_command, shell=True)
				# search_result_sng = shell_out.splitlines()
				
				# shell_out = subprocess.check_output("mpc -f \"%artist%\" search filename " + search_command, shell=True)
				# search_result_art = shell_out.splitlines()
				
				# shell_out = subprocess.check_output("mpc -f \"%album%\" search filename " + search_command, shell=True)
				# search_result_alb = shell_out.splitlines()
				
				# shell_out = subprocess.check_output("mpc -f \"%date%\" search filename " + search_command, shell=True)
				# search_result_yr = shell_out.splitlines()
				
				
				
				
				search_output()
				return False
			else:
				searchstring = searchstring + kb_key
	
	skin_kb = pygame.image.load("Tastatur_de.png")
	screen.blit(skin_kb,(0,0))
	pygame.display.flip()
	
	font=pygame.font.Font(None,30)
	label=font.render(searchstring, 1, (white))
	screen.blit(label,(16,267))
	pygame.display.flip()
	#libpng warning: Interlace handling should be turned on when using png_read_image
	


def keyboard_button():
	#1
	if 11 <= click_pos[0] <= 42 and 14 <= click_pos[1] <= 50:
		#print("1")
		keyboard_key("1")
	#2
	if 53 <= click_pos[0] <= 89 and 14 <= click_pos[1] <= 50:
		#print("2")
		keyboard_key("2")
	#3
	if 100 <= click_pos[0] <= 136 and 14 <= click_pos[1] <= 50:
		#print("3")
		keyboard_key("3")
	#4
	if 147 <= click_pos[0] <= 183 and 14 <= click_pos[1] <= 50:
		#print("4")
		keyboard_key("4")
	#5
	if 194 <= click_pos[0] <= 230 and 14 <= click_pos[1] <= 50:
		#print("5")
		keyboard_key("5")
	#6
	if 241 <= click_pos[0] <= 277 and 14 <= click_pos[1] <= 50:
		#print("6")
		keyboard_key("6")
	#7
	if 288 <= click_pos[0] <= 324 and 14 <= click_pos[1] <= 50:
		#print("7")
		keyboard_key("7")
	#8
	if 335 <= click_pos[0] <= 371 and 14 <= click_pos[1] <= 50:
		#print("8")
		keyboard_key("8")
	#9
	if 382 <= click_pos[0] <= 418 and 14 <= click_pos[1] <= 50:
		#print("9")
		keyboard_key("9")
	#0
	if 429 <= click_pos[0] <= 465 and 14 <= click_pos[1] <= 50:
		#print("0")
		keyboard_key("0")
	###########################################################
	#Q
	if 11 <= click_pos[0] <= 42 and 61 <= click_pos[1] <= 97:
		#print("Q")
		keyboard_key("Q")
	#W
	if 53 <= click_pos[0] <= 89 and 61 <= click_pos[1] <= 97:
		#print("W")
		keyboard_key("W")
	#E
	if 100 <= click_pos[0] <= 136 and 61 <= click_pos[1] <= 97:
		#print("E")
		keyboard_key("E")
	#R
	if 147 <= click_pos[0] <= 183 and 61 <= click_pos[1] <= 97:
		#print("R")
		keyboard_key("R")
	#T
	if 194 <= click_pos[0] <= 230 and 61 <= click_pos[1] <= 97:
		#print("T")
		keyboard_key("T")
	#Z
	if 241 <= click_pos[0] <= 277 and 61 <= click_pos[1] <= 97:
		#print("Z")
		keyboard_key("Z")
	#U
	if 288 <= click_pos[0] <= 324 and 61 <= click_pos[1] <= 97:
		#print("U")
		keyboard_key("U")
	#I
	if 335 <= click_pos[0] <= 371 and 61 <= click_pos[1] <= 97:
		#print("I")
		keyboard_key("I")
	#O
	if 382 <= click_pos[0] <= 418 and 61 <= click_pos[1] <= 97:
		#print("O")
		keyboard_key("O")
	#P
	if 429 <= click_pos[0] <= 465 and 61 <= click_pos[1] <= 97:
		#print("P")
		keyboard_key("P")
	###########################################################
	#A
	if 33 <= click_pos[0] <= 64 and 108 <= click_pos[1] <= 144:
		#print("A")
		keyboard_key("A")
	#S
	if 75 <= click_pos[0] <= 111 and 108 <= click_pos[1] <= 144:
		#print("S")
		keyboard_key("S")
	#D
	if 122 <= click_pos[0] <= 158 and 108 <= click_pos[1] <= 144:
		#print("D")
		keyboard_key("D")
	#F
	if 169 <= click_pos[0] <= 205 and 108 <= click_pos[1] <= 144:
		#print("F")
		keyboard_key("F")
	#G
	if 216 <= click_pos[0] <= 252 and 108 <= click_pos[1] <= 144:
		#print("G")
		keyboard_key("G")
	#H
	if 263 <= click_pos[0] <= 299 and 108 <= click_pos[1] <= 144:
		#print("H")
		keyboard_key("H")
	#J
	if 310 <= click_pos[0] <= 346 and 108 <= click_pos[1] <= 144:
		#print("J")
		keyboard_key("J")
	#K
	if 357 <= click_pos[0] <= 393 and 108 <= click_pos[1] <= 144:
		#print("K")
		keyboard_key("K")
	#L
	if 404 <= click_pos[0] <= 440 and 108 <= click_pos[1] <= 144:
		#print("L")
		keyboard_key("L")
	###########################################################
	#&
	if 11 <= click_pos[0] <= 42 and 155 <= click_pos[1] <= 191:
		#print("&")
		keyboard_key("&")
	#Y
	if 53 <= click_pos[0] <= 89 and 155 <= click_pos[1] <= 191:
		#print("Y")
		keyboard_key("Y")
	#X
	if 100 <= click_pos[0] <= 136 and 155 <= click_pos[1] <= 191:
		#print("X")
		keyboard_key("X")
	#C
	if 147 <= click_pos[0] <= 183 and 155 <= click_pos[1] <= 191:
		#print("C")
		keyboard_key("C")
	#V
	if 194 <= click_pos[0] <= 230 and 155 <= click_pos[1] <= 191:
		#print("V")
		keyboard_key("V")
	#B
	if 241 <= click_pos[0] <= 277 and 155 <= click_pos[1] <= 191:
		#print("B")
		keyboard_key("B")
	#N
	if 288 <= click_pos[0] <= 324 and 155 <= click_pos[1] <= 191:
		#print("N")
		keyboard_key("N")
	#M
	if 335 <= click_pos[0] <= 371 and 155 <= click_pos[1] <= 191:
		#print("M")
		keyboard_key("M")
	#BACK
	if 382 <= click_pos[0] <= 418 and 155 <= click_pos[1] <= 191:
		#print("BACK")
		keyboard_key("BACK")
	#RETURN
	if 429 <= click_pos[0] <= 465 and 155 <= click_pos[1] <= 191:
		#print("RETURN")
		keyboard_key("RETURN")
	###########################################################
	#*
	if 22 <= click_pos[0] <= 58 and 202 <= click_pos[1] <= 238:
		#print("*")
		keyboard_key("*")
	#SPACE
	if 69 <= click_pos[0] <= 328 and 202 <= click_pos[1] <= 238:
		#print("SPACE")
		keyboard_key("SPACE")
	#+
	if 339 <= click_pos[0] <= 375 and 202 <= click_pos[1] <= 238:
		#print("+")
		keyboard_key("+")
	#-
	if 386 <= click_pos[0] <= 422 and 202 <= click_pos[1] <= 238:
		#print("-")
		keyboard_key("-")
	#_
	if 433 <= click_pos[0] <= 469 and 202 <= click_pos[1] <= 238:
		#print("_")
		keyboard_key("_")
	###########################################################


def search_button():
	
	global search_output_rect
	global search_output_open
	global search_offset
	global search_offset_add
	global search_count
	
	if search_count > 0:
		#UP
		if 22 <= click_pos[0] <= 122 and 280 <= click_pos[1] <= 310:
			print("UP")
			if search_offset == 0:
				if search_offset_add > 0:
					search_offset_add -= 1
				else:
					print("NOTHING")
					return False
			else:
				search_offset -= 1
				search_output_rect.move_ip(0,-20)
			# print("search off:" + str(search_offset))
			# print("search off add:" + str(search_offset_add))
			# print("search cnt:" + str(search_count))
			search_output()
		#DOWN
		if 134 <= click_pos[0] <= 234 and 280 <= click_pos[1] <= 310:
			print("DOWN")
			if search_offset == 10: # or (search_offset +1) == search_count:
				if (search_offset +1 + search_offset_add) == search_count:
					print("NOTHING")
					return False
				else:
					print("ADD OFFSET")
					search_offset_add += 1
					#return False
			else:
				search_offset += 1
				search_output_rect.move_ip(0,20)
			# print("search off:" + str(search_offset))
			# print("search off add:" + str(search_offset_add))
			# print("search cnt:" + str(search_count))
			search_output()
		#ABORT
		if 246 <= click_pos[0] <= 346 and 280 <= click_pos[1] <= 310:
			print("ABORT")
			search_clean()
			search_output_rect = None
			search_output_open = False
			refresh_menu_screen()
		#OK
		if 358 <= click_pos[0] <= 458 and 280 <= click_pos[1] <= 310:
			print("OK")
			#CurrPlaylist = "USB" < #mpc searchplay filename "The Rolling Stones/No Security/01 Intro.mp3"
			#CurrPlaylist = "USB" < 
			#mpc search filename "The Rolling Stones/No Security/01 Intro.mp3" |mpc add
			#mpc searchplay filename "The Rolling Stones/No Security/01 Intro.mp3"
			global search_select
			if CurrPlaylist == "USB":
				print("mpc searchplay filename \"" + search_select + "\"")
				subprocess.call("mpc searchplay filename \"" + search_select + "\"", shell=True)
			else:
				print("mpc search filename \"" + search_select + "\" |mpc add")
				print("mpc searchplay filename \"" + search_select + "\"")
				subprocess.call("mpc search filename \"" + search_select + "\" |mpc add", shell=True)
				subprocess.call("mpc searchplay filename \"" + search_select + "\"", shell=True)
			search_clean()
			search_output_rect = None
			search_output_open = False
			refresh_menu_screen()
	else:
		#ABORT
		if 246 <= click_pos[0] <= 346 and 280 <= click_pos[1] <= 310:
			print("ABORT")
			search_output_rect = None
			search_output_open = False
			refresh_menu_screen()
	

#define function that checks for mouse location
def on_click():
	global keyboard_open
	global search_output_open
	
	if search_output_open:
		search_button()
		return search_output_open
	
	if keyboard_open:
		#print("test")
		keyboard_button()
	else:
		# volume down was pressed
		if 10 <= click_pos[0] <= 103 and 4 <= click_pos[1] <= 60:
			print "You pressed volume down"
			button(6)
		# button 7 was pressed
		if 104 <= click_pos[0] <= 194 and 4 <= click_pos[1] <=60:
			print "You pressed volume up"
			button(7)
		# button 8 was pressed
		if 195 <= click_pos[0] <= 283 and 4 <= click_pos[1] <=60:
			print "You pressed Radio"
			button(8)
		# mp3 was pressed
		if 284 <= click_pos[0] <= 373 and 4 <= click_pos[1] <=60:
			print "You pressed  mp3"
			button(3)
		# exit has been pressed
		if 392 < click_pos[0] < 460 and 4 < click_pos[1] < 60:
			print "You pressed exit" 
			button(0)		
		# previous  was pressed
		if 7 <= click_pos[0] <= 103 and 260 <= click_pos[1] <=315:
			print "You pressed  previous"
			button(4)	
		# play was pressed
		if 104 <= click_pos[0] <= 193 and 260 <= click_pos[1] <=315:
			print "You pressed  play"
			button(1)
		# next  was pressed
		if 194 <= click_pos[0] <= 283 and 260 <= click_pos[1] <=315:
			print "You pressed button next"
			button(5)
		# button 9 was pressed
		if 284 <= click_pos[0] <= 372 and 260 <= click_pos[1] <=315:
			print "You pressed Shuffle"
			button(9)
		# folder  was pressed
		if 374 <= click_pos[0] <= 458 and 260 <= click_pos[1] <315:
			print "You pressed folder button"
			#button(2)
			keyboard()


#define action on pressing buttons
def button(number):
	global album_img
	global play
	global x
	global CurrPlaylist
	print "You pressed button ",number
	if number == 0:    #time to  exit
		screen.fill(black)
		font=pygame.font.Font(None,30)
		subprocess.call("mpc stop", shell=True)
        	label=font.render("RaspiPlayer Rocks!!", 1, (white))
        	screen.blit(label,(40,150))
		pygame.display.flip()
		###time.sleep(2)
		sys.exit()

	if number == 1: # play / stop	
		if play == True:
			subprocess.call("mpc stop ", shell=True)
		else:
			subprocess.call("mpc play ", shell=True)
		play = (1,0)[play]
		#album_img = ("/tmp/kunst.png") #don't ues this.. make the event handling without any KUNST... very slow!
		refresh_menu_screen()

	if number == 2: # One playlist for each subdirectory in USB drive.
		try:
                    subprocess.call("mpc clear ", shell=True)
	 	    CurrPlaylist = PlayList[x]
		    CurrPlaylist = CurrPlaylist[:-4]
		    CurrPlaylist = CurrPlaylist[:11]
		except IndexError: # end of playlists.
		    x = 0
                    CurrPlaylist = PlayList[x]
                    CurrPlaylist = CurrPlaylist[:-4]
                    CurrPlaylist = CurrPlaylist[:11]
		print (CurrPlaylist)
	        subprocess.call("mpc load " + str(CurrPlaylist), shell = True)
		subprocess.call("mpc add " + str(CurrPlaylist), shell = True)
        	x = x + 1
		mp3 = True
		play = False
		refresh_menu_screen()

	if number == 8:  # radio
		subprocess.call("mpc clear ", shell=True)
		subprocess.call("mpc load Radio ", shell=True)
		global mp3
		mp3 = False
		CurrPlaylist = "Radio"
		refresh_menu_screen() 

	if number == 4:
		subprocess.call("mpc prev ", shell=True)
		refresh_menu_screen()

	if number == 5:
		subprocess.call("mpc next ", shell=True)
		refresh_menu_screen()

	if number == 6:
		subprocess.call("mpc volume -5 ", shell=True)
		refresh_menu_screen()

	if number == 7:
		subprocess.call("mpc volume +5 ", shell=True)
		refresh_menu_screen()

	if number == 9:
                subprocess.call("mpc random ", shell=True)
		global shuffle
		shuffle = (1,0)[shuffle]
		refresh_menu_screen()

        if number == 3: # Single playlist for all files in usb
                subprocess.call("mpc clear ", shell=True)
		subprocess.call("mpc add /", shell=True) 
		mp3 = True
		CurrPlaylist = "USB"
                refresh_menu_screen()

def connected():
    """Detect an internet connection."""
    global connection
    connection = None
    try:
        socket.create_connection(("1.1.1.1", 53)) # check every 180 seconds
      #  r.raise_for_status()
        print("Internet connection detected.")
#	return True
        connection = True
    except OSError:
        print("Internet connection not detected.")
        connection = False
    finally:
        return connection

def keyboard():
	global keyboard_open
	global searchstring
	searchstring = ""
	keyboard_open = True
	skin_kb = pygame.image.load("Tastatur_de.png")
	screen.blit(skin_kb,(0,0))
	pygame.display.flip()

def refresh_menu_screen():
	global connection
	global connect_img
	global CurrPlaylist
	global keyboard_open
	
	if keyboard_open :
		return keyboard_open
	
	if search_output_open :
		return search_output_open
	
	current_time = datetime.datetime.now().strftime('%H:%M')
	time_font=pygame.font.Font(None,70)
	time_label = time_font.render(current_time, 1, (white))

	connect_font=pygame.font.Font(None, 32)
	connect_label = connect_font.render(". .", 1, (white))
	font=pygame.font.Font(None,32)
	station_font=pygame.font.Font(None,28)
	skin1=pygame.image.load("backgnd.png")
	skin2=pygame.image.load("buttons.png")
	indicator_on=font.render("[        ]", 1, (green))
	indicator_off=font.render("", 1, (white))
	label2=font.render("RaspiPlayer", 1, (silver))

	screen.blit(skin1,(0,0))
	screen.blit(skin2,(0,0))
	screen.blit(label2,(190, 62))
	pygame.draw.rect(screen, gray, (336, 95, 130, 49),0)
	pygame.draw.rect(screen, gray, (52, 183, 407, 75),0)
	#screen.blit(time_label,(336, 90)) # position not nice :)
	screen.blit(time_label,(338, 94))
	conn_image=pygame.image.load("internet.png")
	if connection==True:
		screen.blit(conn_image,(418, 62))
	else:
		screen.blit(connect_label,(418, 62))

	try:
		album_art=pygame.image.load(album_img) # album art
		album_art=pygame.transform.scale(album_art, (155, 117))
		screen.blit(album_art,(17,60))
	except pygame.error:
		time.sleep(1)

	##### display the station name and split it into 2 parts : 
	lines = subprocess.check_output("mpc current", shell=True).split("-")
	if len(lines)==1:
		line1 = lines[0]
		line1 = line1[:-1]
		line2 = " No additional info: "
	else:
		line1 = lines[0]
		line2 = lines[1]

	line1 = line1[:38]
	line2 = line2[1:38]
	line2 = line2[:-1]
	#trap no station data
	if line1 =="":
		line2 = "Press PLAY"
		Playlist_name = (CurrPlaylist)
#		connection = False
	else:
		Playlist_name = (CurrPlaylist)
#		connection = True

	station_name=station_font.render(line1, 1, (white))
	additional_data=station_font.render(line2, 1, (white))
	station_label=font.render(Playlist_name, 1, (cyan))
	screen.blit(station_label,(190,117)) #playing
	screen.blit(station_name,(66,231))
	screen.blit(additional_data,(66,195))

	 ##### display remaining time  : 
        RemTime = subprocess.check_output("mpc -f %time%", shell=True).split("\n")
        if len(RemTime)==1:
                Ln1 = RemTime[0]
                Ln1 = Ln1[:-1]
                Ln2 = "> "
        else:
                Ln1 = RemTime[0]
                Ln2 = RemTime[1]

        Ln2 = Ln2[:-5]
        rem_time=station_font.render(Ln2, 1, (cyan))
        screen.blit(rem_time,(190,153))

	# add volume number
	volume = subprocess.check_output("mpc volume", shell=True )
	volume = volume[8:] # remove unwanted characters.
	volume = volume[:-1]
	volume_tag=font.render(volume, 1, (white))
	screen.blit(volume_tag,(190,90))
	# shuffle the list
	if shuffle == 1:
		screen.blit(indicator_on,(300, 273))

	else:
        	screen.blit(indicator_off,(373, 273))
	# light-up source button
	if mp3 == True:
		screen.blit(indicator_on,(298, 16))
		screen.blit(indicator_off,(209, 16))
	else:
		screen.blit(indicator_off,(298, 16))
		screen.blit(indicator_on,(209,16))
#	time.sleep(.3)
	pygame.display.flip()

def main():
    global click_pos
    timer = pygame.time.get_ticks()
    while 1:
        seconds=(pygame.time.get_ticks() - timer)/1000
        if seconds > 180: # check every 3 min 
	    timer = pygame.time.get_ticks()
            connected() # check for internet connection

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                print "screen pressed" #for debugging purposes
                print click_pos #for checking coordinates
                on_click()

            #Press ESC key on the computer to end while in VNC

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # ESC key will kill it
                    if play == True:
                        subprocess.call("mpc stop ", shell=True)
                    sys.exit()
					
        clock.tick(15) #refresh screen 15fps
        if seconds > 3:	
            refresh_menu_screen()

connected()
refresh_menu_screen() 
main() # Main loop


