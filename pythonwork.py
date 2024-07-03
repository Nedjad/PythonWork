import json
import datetime

class Note:
    def __init__(self, title, body):
        self.id = id(self)
        self.title = title
        self.body = body
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class NoteApp:
    def __init__(self):
        self.notes = []

    def create(self, title, body):
        note = Note(title, body)
        self.notes.append(note)
        self.save_notes()

    def save_notes(self):
        with open('notes.json', 'w') as f:
            json.dump([note.to_dict() for note in self.notes], f)

    def load_notes(self):
        try:
            with open('notes.json', 'r') as f:
                notes_dicts = json.load(f)
                self.notes = [self.dict_to_note(note_dict) for note_dict in notes_dicts]
        except FileNotFoundError:
            self.notes = []

    def dict_to_note(self, note_dict):
        note = Note(note_dict['title'], note_dict['body'])
        note.id = note_dict['id']
        note.created_at = datetime.datetime.strptime(note_dict['created_at'], '%Y-%m-%d %H:%M:%S')
        note.updated_at = datetime.datetime.strptime(note_dict['updated_at'], '%Y-%m-%d %H:%M:%S')
        return note

    def list_notes(self, date_filter=None):
        for note in self.notes:
            if date_filter and note.created_at.date() != date_filter:
                continue
            print(f"ID: {note.id}\nTitle: {note.title}\nBody: {note.body}\nCreated at: {note.created_at}\nUpdated at: {note.updated_at}\n---")

    def update(self, note_id, title, body):
        for note in self.notes:
            if note.id == note_id:
                note.title = title
                note.body = body
                note.updated_at = datetime.datetime.now()
                self.save_notes()
                return
        print("Note not found.")

    def delete(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                self.notes.remove(note)
                self.save_notes()
                return
        print("Note not found.")

app = NoteApp()
app.load_notes()

while True:
    command = input("Введите команду: ")
    if command == "add":
        title = input("Введите заголовок заметки: ")
        body = input("Введите тело заметки: ")
        app.create(title, body)
        print("Заметка успешно сохранена")
    elif command == "list":
        date_filter = input("Введите дату для фильтрации (YYYY-MM-DD) или оставьте пустым для всех заметок: ")
        if date_filter:
            date_filter = datetime.datetime.strptime(date_filter, '%Y-%m-%d').date()
        else:
            date_filter = None
        app.list_notes(date_filter)
    elif command == "update":
        note_id = int(input("Введите ID заметки: "))
        title = input("Введите новый заголовок заметки: ")
        body = input("Введите новое тело заметки: ")
        app.update(note_id, title, body)
    elif command == "delete":
        note_id = int(input("Введите ID заметки: "))
        app.delete(note_id)
    elif command == "quit":
        break
    else:
        print("Неизвестная команда.")
