
import xml.etree.ElementTree as ET
from xml.dom import minidom

def save_xml(filename, xml_code):
    xml_string = ET.tostring(xml_code).decode()
 
    xml_prettyxml = minidom.parseString(xml_string).toprettyxml()
    with open(filename, 'a', encoding = "utf-8") as xml_file:
        xml_file.write(xml_prettyxml)


#---------Перераспределение значений в табице------------

name = input ("Введите название исходного файла (не забудьте про формат): ") # name = "questionnaire_size_frames.csv"
if name.endswith ('.csv') == True:
    new_name = "new_" + name
    name_sorted = "sorted_" + name
else:
    new_name = "new_" + name.split ('.')[0] + '.csv'
    name_sorted = "sorted_" + name.split ('.')[0] + '.csv'
xml_name = name.split ('.')[0] + '.xml'

tax_class = input ("Введите таксономический класс: ")       #tax_class = 'размер' 
meaning = input ("Введите типа значения (d, если значение исходное, и f -- если переносное) ")         #meaning = 'd'
_lang_ = input ("Введите язык (полное название на русском): ")   #_lang_ = "английский"
#field = input ("Введите семантическое поле: ")
field = '' #?

f = open (name, 'r', encoding = 'utf-8')
all_strings = f.read()
f.close()
strings = all_strings.split ("\n")

d = {}
for _lexeme_ in strings[0].split(";"):
    if len(_lexeme_) > 1:
        d[_lexeme_] = ''

del (strings[0])

f = open (new_name, 'a', encoding = 'utf-8')
#f = open ('questionnaire_size.csv', 'a', encoding = 'utf-8')
f.write ("lexeme" + "\t" + "lang" + "\t" + "mframe" + "\t" + "trans" + "\t" + "frame" + "\t" + "tax_class" + "\t" + "field" + "\t" + "meaning" + "\t" + "usage" + "\n")

i = 2
for lexeme in d:
    i += 1
    for string in strings:
        _cells_in_a_row_ = string.split(";")
        _frame_ = _cells_in_a_row_[0]
        if _cells_in_a_row_[i] == "+":
            _usage_ = "+"
        else:
            _usage_ = "-"
        _mframe_ = _cells_in_a_row_[1]
        trans = _cells_in_a_row_[2]

        f.write (lexeme + "\t" + _lang_ + "\t" + _mframe_ + "\t" + trans + "\t" + _frame_ + "\t" + tax_class + "\t" + field + "\t" + meaning + "\t" + _usage_ + "\n")
f.close()


#-------------Сортировка----------------

import pandas as pd

def main():
    df = pd.read_csv(new_name, sep='\t', index_col=False)
    #df = pd.read_csv("questionnaire_size.csv", sep='\t', index_col=False)
    df = df.sort_values(by=['field', 'frame', 'usage', 'lexeme', 'meaning'])
    df.to_csv(name_sorted, sep='\t', encoding = "utf-8")
    #df.to_csv('questionnaire_size_sorted.csv', sep='\t', encoding = "utf-8")    

if __name__ ==  '__main__':
    main()


#----------Создание XML-----------------

FRAMES = []
LEXEMES = []
MFRAMES = []

root = ET.Element ('root')
root.text = ""

field = ET.SubElement (root, 'field')
field.text = '' #string [7]

f = open (name_sorted, 'r', encoding = 'utf-8')
all_strings = f.read()
f.close()
strings = all_strings.split ("\n")
del (strings[0])
for string in strings:
    string = string.split ("\t")
    if string[5] not in FRAMES:
        LEXEMES = []
        FRAMES.append (string[5])
        meaning = ET.Element ("meaning")
        meaning.text = string [8]
        tax_class = ET.Element ("tax_class")
        tax_class.text = string [6]
        frame = ET.SubElement (field, "frame" , attrib = {"tax_class":tax_class.text, "meaning":meaning.text})
        frame.text = string [5]

    if string [1] not in LEXEMES:
        MFRAMES = []
        LEXEMES.append (string[1])
        lang = ET.Element ("lang")
        lang.text = string [2]
        lexeme = ET.SubElement (frame, 'lexeme', attrib = {"lang":lang.text})
        lexeme.text = string [1]

    if string[3] not in MFRAMES:
        MFRAMES.append (string [3])
        trans = ET.Element ("mframe_trans")
        trans.text = string [4]
        usage = ET.Element ("usage")
        usage.text = string [9]
        mframe = ET.SubElement (lexeme, "mframe", attrib = {"trans":trans.text, "usage":usage.text})
        mframe.text = string [3]


#save_xml('questionnaire_size.xml', root)
save_xml(xml_name, root)
