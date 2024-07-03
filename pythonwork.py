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
                self.notes = json.load(f)
        except FileNotFoundError:
            self.notes = []

    def list_notes(self):
        for note in self.notes:
            print(f"ID: {note['id']}\nTitle: {note['title']}\nBody: {note['body']}\nCreated at: {note['created_at']}\nUpdated at: {note['updated_at']}\n---")

    def update(self, note_id, title, body):
        for note in self.notes:
            if note['id'] == note_id:
                note['title'] = title
                note['body'] = body
                note['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_notes()
                return
        print("Note not found.")

    def delete(self, note_id):
        for note in self.notes:
            if note['id'] == note_id:
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
        app.list_notes()
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
