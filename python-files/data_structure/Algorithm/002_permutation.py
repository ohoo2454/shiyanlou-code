class Permutations(object):

    def is_permutation(self, str1, str2):
        if str1 == None or str2 == None:
            return False
        return sorted(str1) == sorted(str2)
        