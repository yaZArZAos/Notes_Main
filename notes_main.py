from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit, QListWidget, QHBoxLayout, QLineEdit, QInputDialog
import json

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
main_win.resize(900, 600)

def show_note():
    key = list1.selectedItems()[0].text()
    note.setText(notes[key]['текст'])
    list2.clear()
    list2.addItems(notes[key]['теги'])

def add_note():
    notes_name, result = QInputDialog.getText(
        main_win, 'Добавление заметки', 'Название:'
    ) 
    if result:
        notes[notes_name] = {
            'текст': '',
            'теги': []        
        }
        list1.addItem(notes_name)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def delete_note():
    if list1.selectedItems():
        key = list1.selectedItems()[0].text()
        del notes[key]
        list1.clear()
        list1.addItems(notes)
        note.clear()
        list2.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def save_note():
    if list1.selectedItems():
        key = list1.selectedItems()[0].text()
        notes[key]['текст'] = note.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def add_tag():
    if list1.selectedItems():
        key = list1.selectedItems()[0].text()
        tag = line1.text()
        if tag != '' and not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list2.addItem(tag)
            line1.clear()
            with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def delete_tag():
    if list2.selectedItems():
        key = list1.selectedItems()[0].text()
        tag = list2.selectedItems()[0].text()
        notes[key ]['теги'].remove(tag)
        list2.clear()
        list2.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys = True, ensure_ascii = False)

def search_tag():
    tag = line1.text()
    if tag and btn6.text() == 'Искать заметки по тегу':
        notes_filtered = dict()
        for key in notes:
            if tag in notes[key]['теги']:
                notes_filtered[key] = notes[key]
        btn6.setText('Сбросить поиск')
        list1.clear()
        list2.clear()
        note.clear()
        list1.addItems(notes_filtered)
    else:
        line1.clear()
        btn6.setText('Искать заметки по тегу')
        list1.clear()
        list1.addItems(notes)


#inscriptiouns
inscr1 = QLabel('Список заметок')
inscr2 = QLabel('Список тегов')

#btns
btn1 = QPushButton('Создать заметку')
btn2 = QPushButton('Удалить заметку')
btn3 = QPushButton('Сохранить заметку')
btn4 = QPushButton('Добавить к заметке')
btn5 = QPushButton('Открепить от заметки')
btn6 = QPushButton('Искать заметки по тегу')

#note
note = QTextEdit()

#lists
list1 = QListWidget()
list2 = QListWidget()

#edit line
line1 = QLineEdit()
line1.setPlaceholderText('Введите тег')

#lines
HL1 = QHBoxLayout()
HL2 = QHBoxLayout()
HL3 = QHBoxLayout()
VL1 = QVBoxLayout()
VL2 = QVBoxLayout()

HL1.addLayout(VL1)
HL1.addLayout(VL2)

VL1.addWidget(note)
VL2.addWidget(inscr1)
VL2.addWidget(list1)
HL2.addWidget(btn1)
HL2.addWidget(btn2)
VL2.addLayout(HL2)
VL2.addWidget(btn3)
VL2.addWidget(inscr2)
VL2.addWidget(list2)
VL2.addWidget(line1)
HL3.addWidget(btn4)
HL3.addWidget(btn5)
VL2.addLayout(HL3)
VL2.addWidget(btn6)
VL2.addWidget(inscr2)
 
with open('notes_data.json', 'r') as file:
    notes = json.load(file)

list1.addItems(notes)
list1.itemClicked.connect(show_note)
btn1.clicked.connect(add_note)
btn2.clicked.connect(delete_note)
btn3.clicked.connect(save_note)
btn4.clicked.connect(add_tag)
btn5.clicked.connect(delete_tag)
btn6.clicked.connect(search_tag)
main_win.setLayout(HL1)
main_win.show()
app.exec_()