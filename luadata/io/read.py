import codecs


class StreamData:
    def __init__(self, data, p):
        self.data = data
        self.p = p

    @staticmethod
    def valid(ch):
        return ch != '\r' and ch != '\n' and ch != '\t' and ch != ' '

    @staticmethod
    def format_marks(string):
        if string[0] == '\"' and string[-1] == '\"':
            return string[1:-1]
        elif string[0] == '\'' and string[-1] == '\'':
            return string[1:-1]
        return string

    @staticmethod
    def format_key(key):
        if key[0] == '[':
            key = key[1:-1]
            if key[0] == '\"' or key[0] == '\'':
                return StreamData.format_marks(key)
            elif key.isdigit():
                return int(key)
        return key

    @staticmethod
    def format_value(val):
        if isinstance(val, str) and val.isdigit():
            return int(val)
        return val

    def read_char(self):
        return self.data[self.p]

    def read_next(self):
        self.p += 1
        return self.read_char()

    def read_trim(self):
        ch = self.read_char()
        while not StreamData.valid(ch):
            ch = self.read_next()

    def read_chars(self):
        buffer = ""
        self.read_trim()
        ch = self.read_char()
        while StreamData.valid(ch) and ch != '{' and ch != '}' and ch != '=' and ch != ',':
            buffer += ch
            ch = self.read_next()
        self.read_trim()
        return buffer

    def read_brackets(self):
        buffer = ""
        self.read_trim()
        ch = self.read_next()
        while ch != ']':
            buffer += ch
            ch = self.read_next()
        self.p += 1
        self.read_trim()
        return buffer

    def read_string(self):
        buffer = ""
        self.read_trim()
        left_ch = self.read_char()
        ch = self.read_next()
        while ch != left_ch:
            buffer += ch
            ch = self.read_next()
        self.p += 1
        self.read_trim()
        return buffer

    def read_table(self):
        index = 0
        table = {}
        lists = []

        ch = self.read_next()
        while ch != '}':
            item = self.read_item()
            self.read_trim()
            ch = self.read_char()
            if ch == "=":
                self.p += 1
                table[StreamData.format_key(item)] = self.read_item()
            else:
                index += 1
                table[index] = item

            self.read_trim()
            ch = self.read_char()

            if ch == ',':
                self.p += 1
                self.read_trim()
                ch = self.read_char()

        self.p += 1

        for i in range(1, len(table) + 1):
            if i in table:
                lists.append(table[i])

        if len(lists) == len(table):
            return lists
        return table

    def read_pairs(self):
        key = self.read_item()
        self.read_trim()
        ch = self.read_char()
        if ch == "=":
            self.p += 1
            return StreamData.format_value(key), self.read_item()
        return key

    def read_item(self):
        self.read_trim()
        ch = self.read_char()
        if ch == '{':
            return self.read_table()
        elif ch == '\"' or ch == '\'':
            return self.read_string()

        item = self.read_chars()
        if item.isdigit():
            return int(item)
        elif item == "true":
            return True
        elif item == 'false':
            return False
        else:
            return item


def unserialize_buffer(src_data):
    return StreamData("{%s}" % src_data, 0).read_item()


def unserialize(path, encoding='utf-8'):
    fl = codecs.open(path, 'r', encoding)
    src_data = fl.read()
    data = unserialize_buffer(src_data)
    fl.close()
    return data
