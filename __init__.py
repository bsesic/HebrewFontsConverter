# -*- coding: utf-8 -*-

#Script to convert Text in BwHebb Fonts to normal unicode Hebrew.
#copyright 2013 Benjamin Schnabel Benjamin-777@gmx.de www.benjaminschnabel.de
#Benjamin-777@gmx.de

import os
import sys
import string
import codecs

#Load file
def LoadFile() :
    fread = input('Enter input file:')
    print('Select options:')
    print('[1] Bwhebb -> Hebrew')
    print('[2] Hebrew -> Bwhebb')
    print('[3] Bwgrk -> Greek')
    print('[4] Greek -> Bwgrk')
    selection = input()
    return (fread, selection)

#read line
def ReadLine(fread, selection) :
    if selection == '1':
        charfile = 'hebrew.txt'
        converter = 1
        lang = 1
    elif selection == '2':
        charfile = 'hebrew.txt'
        converter = 2
        lang = 1
    elif selection == '3':
        charfile = 'greek.txt'
        converter = 1
        lang = 2
    elif selection == '4':
        charfile = 'greek.txt'
        converter = 2
        lang = 2
    else:
        print('wrong selection, exiting...')
        sys.exit()
    
    bwhebb = []
    hebrew = []
    result = ''
    indicator = False
    vowels = ''
    
    try: 
        c = open(charfile, 'r', encoding='utf-8')
    except (OSError, IOError):
        print('Character file not found, exiting...')
        sys.exit()
    
    #load characters and vowels in string    
    for character in c:
        character.encode(encoding='utf-8', errors='replace')
        character = character.strip()
        split = character.split(' ')
        if indicator == True:
            vowels += character[0]
        if 'vowels:' in character:
            indicator = True
        elif converter == 1:
            bwhebb.append(split[0])
            hebrew.append(split[-1])
        elif converter == 2:
            bwhebb.append(split[-1])
            hebrew.append(split[0])
    c.close()
    
    try:
        f = open(fread, 'r', encoding='utf-8')
    except (OSError, IOError):
        print('Input file not found, exiting...')
        sys.exit()
    for content in f:
        content = content.replace(' / ', '*')
        content = content.replace('* ','*')
        content = content[:-1]
        #replace vowels
        content = ReplaceVowels(content, vowels)
        #change RTL before replacing characters
        if lang == 1:
            content = ChangeRTL(content)
        #change characters one by one
        for i in range(len(bwhebb)):
            content = content.replace(bwhebb[i], hebrew[i])
        content = content.replace('*', '/')
        result += content + '\n'
    f.close()
    if lang == 1:
        result = result +  u'\u200f'
    return result

def ReplaceVowels (content, vowels):
#change the place of the vowels with the consonant before it (RTL)
    content = ' ' + content + ' '
    for i in range(len(content)):
        for j in range(len(vowels)):
            if vowels[j] == content[i]:
                replace = list(content)
                replace[i] = content[i-1]
                replace[i-1] = content[i]
                content = ''.join(replace)
    content = content.strip()
    return content

#change RTL
def ChangeRTL(content) :
    result = ''
    for i in range(len(content)-1, -1, -1):
        result += content[i]
    return result

#write file
def  WriteFile(content) :
    content.encode(encoding='utf-8', errors='replace')
    filename = input('Enter output file:')
    fwrite = open(filename,'w', encoding='utf-8')
    fwrite.writelines(content)
    fwrite.close()

fread = None
result = None    
fread, selection = LoadFile()
result = ReadLine(fread, selection)
WriteFile(result)