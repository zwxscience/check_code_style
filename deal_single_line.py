import re

from log import Log
import const


class DealSingle(object):
    def __init__(self):
        self.log = Log()
        pass

    def check_all(self,filename, line_no, line):
        self.check_max_line_length(filename, line_no, line)
        self.check_2blank_operator(filename, line_no, line)
        self.check_before_blank(filename, line_no, line)
        self.check_after_blank(filename, line_no, line)

    def check_max_line_length(self,filename, line_no, line):
        if len(line) > const.max_line_length:
            self.log.error("file %s,line %d,line length %d exceed max length."%
                           (filename, line_no, len(line)))

    # before blank ~a ( ((
    def check_before_blank(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '(')
        eqs_format1 = [' (', ')(']
        eqs_format2 = ['((']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx - 1:eqIdx + 1]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2):
                if eqstr in eqs_format2  and line[eqIdx - 2:eqIdx - 1] != ' ' :
                    self.log.error("file %s,line %d,col %d operator %s missed blank." %
                                   (filename, line_no, eqIdx + 1, eqstr))
            else:
                #
                # if not (len(re.findall(r"[a-zA-Z\"]", line[eqIdx + 1:eqIdx + 2])) > 0):
                self.log.error("file %s,line %d,len %d col %s operator %s missed blank." %
                               (filename, line_no, len(line), str(eqIdx + 1), line[eqIdx:eqIdx + 1]))

    # after blank  ,
    def check_after_blank(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, ',')
        eqs_format1 = [', ']
        eqs_format2 = []
        for eqIdx in eq_ids:
            eqstr = line[eqIdx:eqIdx + 2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2):
                if eqstr in eqs_format2:
                    self.log.error("file %s,line %d,col %d operator %s missed blank." %
                                   (filename, line_no, eqIdx + 1, eqstr))
            else:
                # line end
                if not (line[-1] == ','):
                    self.log.error("file %s,line %d,len %d col %s operator %s missed blank." %
                               (filename, line_no, len(line), str(eqIdx + 1), line[eqIdx:eqIdx + 1]))

        # 2 charater >= <=  ==  != || && += -= *= /= &= ~=
        # 1 charater + - * / % | ? = > < &
    def check_2blank_operator(self, filename, line_no, line):
        self.check_eq(filename, line_no, line)
        self.check_plus(filename, line_no, line)
        self.check_minus(filename, line_no, line)
        self.check_muliti(filename, line_no, line)
        self.check_dev(filename, line_no, line)
        self.check_perc(filename, line_no, line)
        self.check_question(filename, line_no, line)
        self.check_greater(filename, line_no, line)
        self.check_less(filename, line_no, line)
        self.check_and(filename, line_no, line)

    def str_all_index(self, str_, a):
        '''
        Parameters
        ----------
        str_ : string.
        a : str_中的子串

        Returns
        -------
        index_list : list

        首先输入变量2个，输出list，然后中间构造每次find的起始位置start,start每次都在找到的索引+1，后面还得有终止循环的条件

        '''
        index_list = []
        start = 0
        while True:
            x = str_.find(a, start)
            if x > -1:
                start = x + 1
                index_list.append(x)
            else:
                break
        return index_list

    def check_eq(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '=')
        eqs_format1 = [' = ']
        eqs_format2 = [ '>= ', '<= ', '!= ', '+= ','-= ', '*= ','/= ','&= ','~= ', '|= ', '|| ', '== ']
        eqs_format3 = [' ||', ' ==']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx-1:eqIdx+2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3) :
                if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
                elif eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
            else:
                self.log.error("file %s,line %d,col %s operator = missed blank."%
                               (filename, line_no, str(eqIdx+1)))

    def check_plus(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '+')
        eqs_format1 = [' + ']
        eqs_format2 = []
        eqs_format3 = [' +=']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx-1:eqIdx+2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3) :
                if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
                if eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
            else:
                # a++
                if not (line[eqIdx-1:eqIdx] == '+' or line[eqIdx+1:eqIdx+2] == '+'):
                    self.log.error("file %s,line %d,col %s operator %s missed blank."%
                                    (filename, line_no, str(eqIdx+1), line[eqIdx:eqIdx+1]))

    # the variable with - will error identify
    def check_minus(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '-')
        eqs_format1 = [' - ']
        eqs_format2 = ['']
        eqs_format3 = [' -=']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx-1:eqIdx+2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3) :
                if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
                if eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
            else:
                # a-- b->flag
                if not (line[eqIdx-1:eqIdx] == '-' or line[eqIdx+1:eqIdx+2] == '-' or line[eqIdx+1:eqIdx+2] == '>'):
                    self.log.error("file %s,line %d,col %s operator %s missed blank or a variable."%
                                    (filename, line_no, str(eqIdx+1), line[eqIdx:eqIdx+1]))

    def check_muliti(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '*')
        eqs_format1 = [' * ']
        eqs_format2 = ['']
        eqs_format3 = [' *=']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx-1:eqIdx+2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3) :
                if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
                if eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
            else:
                # not /*  \*/ or pointer **a or last
                if not (line[eqIdx-1:eqIdx] == '/' or line[eqIdx+1:eqIdx+2] == '/' or line[eqIdx+1:eqIdx+2] == ' ' or
                        len(re.findall(r"[a-zA-Z>*),]", line[eqIdx+1:eqIdx+2])) > 0 or line[-1] == '*'):
                    self.log.error("file %s,line %d,len %d col %s operator %s missed blank."%
                                    (filename, line_no, len(line), str(eqIdx+1), line[eqIdx:eqIdx+1]))

    def check_dev(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '/')
        eqs_format1 = [' / ']
        eqs_format2 = ['// ']
        eqs_format3 = [' /=', ' //']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx-1:eqIdx+2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3):
                if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank." %
                                   (filename, line_no, eqIdx + 1, eqstr))
                if eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
            else:
                # /* */ some this/that maybe error show
                if not (line[eqIdx-1:eqIdx] == '*' or line[eqIdx+1:eqIdx+2] == '*' or line[eqIdx+1:eqIdx+2] == ' '):
                    self.log.error("file %s,line %d,len %d col %s operator %s missed blank."%
                                    (filename, line_no, len(line), str(eqIdx+1), line[eqIdx:eqIdx+1]))

    def check_perc(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '%')
        eqs_format1 = [' % ']
        eqs_format2 = ['%% ']
        eqs_format3 = [' %=', '%% ']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx-1:eqIdx+2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3) :
                if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
                if eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
            else:
                # %d,%e
                if not (len(re.findall(r"[a-zA-Z\"]", line[eqIdx + 1:eqIdx + 2])) > 0):
                    self.log.error("file %s,line %d,len %d col %s operator %s missed blank."%
                                    (filename, line_no, len(line), str(eqIdx+1), line[eqIdx:eqIdx+1]))

    def check_or(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '|')
        eqs_format1 = [' | ']
        eqs_format2 = ['|| ']
        eqs_format3 = [' |=', '|| ']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx-1:eqIdx+2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3) :
                if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
                if eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
            else:
                #
                # if not (len(re.findall(r"[a-zA-Z\"]", line[eqIdx + 1:eqIdx + 2])) > 0):
                self.log.error("file %s,line %d,len %d col %s operator %s missed blank."%
                                    (filename, line_no, len(line), str(eqIdx+1), line[eqIdx:eqIdx+1]))

    def check_question(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '?')
        eqs_format1 = [' ? ']
        eqs_format2 = []
        eqs_format3 = []
        for eqIdx in eq_ids:
            eqstr = line[eqIdx-1:eqIdx+2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3) :
                pass
                # if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                #     self.log.error("file %s,line %d,col %d operator %s missed blank."%
                #                    (filename, line_no, eqIdx+1, eqstr))
                # if eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                #     self.log.error("file %s,line %d,col %d operator %s missed blank."%
                #                    (filename, line_no, eqIdx+1, eqstr))
            else:
                #
                # if not (len(re.findall(r"[a-zA-Z\"]", line[eqIdx + 1:eqIdx + 2])) > 0):
                self.log.error("file %s,line %d,len %d col %s operator %s missed blank."%
                                    (filename, line_no, len(line), str(eqIdx+1), line[eqIdx:eqIdx+1]))

    def check_greater(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '>')
        eqs_format1 = [' > ']
        eqs_format2 = ['>> ', '->']
        eqs_format3 = [' >>', ' >=']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx-1:eqIdx+2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3) :
                if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
                if eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank."%
                                   (filename, line_no, eqIdx+1, eqstr))
            else:
                # -> <int> cout<<
                if not (line[eqIdx - 1:eqIdx] == '-' or line[eqIdx - 1:eqIdx] == '>' or
                        len(re.findall(r"[a-zA-Z\*>]", line[eqIdx - 1:eqIdx])) > 0):
                    self.log.error("file %s,line %d,len %d col %s operator %s missed blank."%
                                    (filename, line_no, len(line), str(eqIdx+1), line[eqIdx:eqIdx+1]))

    def check_less(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '<')
        eqs_format1 = [' < ']
        eqs_format2 = ['<< ']
        eqs_format3 = [' <<', ' <=']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx - 1:eqIdx + 2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3):
                if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank." %
                                   (filename, line_no, eqIdx + 1, eqstr))
                if eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank." %
                                   (filename, line_no, eqIdx + 1, eqstr))
            else:
                # <int>
                if not (len(re.findall(r"[a-zA-Z<]", line[eqIdx + 1:eqIdx + 2])) > 0 or
                        line[eqIdx - 1:eqIdx] == '<'):
                    self.log.error("file %s,line %d,len %d col %s operator %s missed blank." %
                               (filename, line_no, len(line), str(eqIdx + 1), line[eqIdx:eqIdx + 1]))

    def check_and(self, filename, line_no, line):
        eq_ids = self.str_all_index(line, '&')
        eqs_format1 = [' & ']
        eqs_format2 = ['&& ']
        eqs_format3 = [' &&']
        for eqIdx in eq_ids:
            eqstr = line[eqIdx - 1:eqIdx + 2]
            if (eqstr in eqs_format1) or (eqstr in eqs_format2) or (eqstr in eqs_format3):
                if eqstr in eqs_format2 and line[eqIdx - 2:eqIdx - 1] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank." %
                                   (filename, line_no, eqIdx + 1, eqstr))
                if eqstr in eqs_format3 and line[eqIdx + 2:eqIdx + 3] != ' ':
                    self.log.error("file %s,line %d,col %d operator %s missed blank." %
                                   (filename, line_no, eqIdx + 1, eqstr))
            else:
                # &a,
                if not (len(re.findall(r"[a-zA-Z<]", line[eqIdx + 1:eqIdx + 2])) > 0 ):
                    self.log.error("file %s,line %d,len %d col %s operator %s missed blank." %
                               (filename, line_no, len(line), str(eqIdx + 1), line[eqIdx:eqIdx + 1]))