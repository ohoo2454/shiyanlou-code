class UniqueChars(object):

    def has_unique_chars(self, string):
        if string == None:
            return False
        return len(set(string)) == len(string)
        