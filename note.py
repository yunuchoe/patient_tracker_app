import datetime

class Note:
    def __init__(self, code: int, text: str, timestamp=datetime.datetime.now()):
        self.code = code
        self.text = text
        self.timestamp = timestamp

    def __eq__(self, other):
        return self.text == other.text and self.code == other.code

    def __str__(self):
        return "Code: %d, Text: %s" % (self.code, self.text)

    def __repr__(self):
        return "Note(%r, %r)" % (self.code, self.text)
