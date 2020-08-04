#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re

from ply import lex
from wcwidth import wcswidth

KEYWORD_regex_string = r'(t|ti|ts|s|tsc|desc|tscd|eti|cti|ab|eab|cab|cl|ecl|d|eds|ap|fap|addr|aee|caee|in|ag|at|n|dn|an|pr|dd|ddy|ddm|ad|ady|adm|pctDate|ipc|ipc-section|ipc-class|ipc-subclass|ipc-group|ipc-subgroup|ipc-main|ipcm-section|ipcm-class|ipcm-subclass|ipcm-group|ipcm-subgroup|uspc|uspcc|fi|ft|loc|cpc|ls|currentStatus|type|cc|acc|kc|lang|apt|ap-zip|country|province|city|aeet|caeet|agc|legalTag|legalEvent|maintainYears|citedCount|citingCount|level|judgment\.date|judgment\.title|judgment\.caseId|judgment\.court|judgment\.province|judgment\.city|judgment\.accuser|judgment\.defendant)(?=\s*:)'
regex = re.compile(KEYWORD_regex_string, flags = re.IGNORECASE)
reserved = {
            'and' : 'AND'
           ,'or'  : 'OR'
           ,'not' : 'NOT'
           ,'to'  : 'TO'
        }

# List of token names.   This is always required
tokens = (
            'KEYWORD'
           ,'EQUAL'
           ,'VALUE'
           ,'CONNECT'
           ,'LPARENTHESIS'
           ,'RPARENTHESIS'
           ,'LBRACKET'
           ,'RBRACKET'
) + tuple(reserved.values())

# Regular expression rules for simple tokens
t_EQUAL        = r':'
#  t_CONNECT      = r'\(\s*[1-9]?[wWnN]\s*\)'
t_LPARENTHESIS = r'\('
t_RPARENTHESIS = r'\)'
t_LBRACKET     = r'\['
t_RBRACKET     = r'\]'

def t_KEYWORD(t):
    r'(t|ti|ts|s|tsc|desc|tscd|eti|cti|ab|eab|cab|cl|ecl|d|eds|ap|fap|addr|aee|caee|in|ag|at|n|dn|an|pr|dd|ddy|ddm|ad|ady|adm|pctDate|ipc|ipc-section|ipc-class|ipc-subclass|ipc-group|ipc-subgroup|ipc-main|ipcm-section|ipcm-class|ipcm-subclass|ipcm-group|ipcm-subgroup|uspc|uspcc|fi|ft|loc|cpc|ls|currentStatus|type|cc|acc|kc|lang|apt|ap-zip|country|province|city|aeet|caeet|agc|legalTag|legalEvent|maintainYears|citedCount|citingCount|level|judgment\.date|judgment\.title|judgment\.caseId|judgment\.court|judgment\.province|judgment\.city|judgment\.accuser|judgment\.defendant)(?=\s*:)'
    t.type = 'KEYWORD'
    t.value = t.value.lower()
    return t

# A regular expression rule with some action code
def t_VALUE(t):
    # r'(?P<quote>")?[^\(\)\[\]\s=]+(?(quote)")'
    r'"[^"]+"|[^\s\(\)\[\]]+'
    t.type = reserved.get(t.value.lower(), 'VALUE')
    t.value = re.sub(' +', ' ', t.value) #将多个连续的空格替换为单个空格
    t.value = re.sub('(?<=")[\s\n\t ]+|[\s\n\t]+(?=")', '', t.value) #将紧靠双引号内侧的空格删除
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def scFormatter(string):
    string = regex.sub(lambda i: i.group().lower(), string)
    # Build the lexer
    lexer = lex.lex()

    if string.strip() == '':
        return
    # Give the lexer some input
    lexer.input(f'{string}')

    # Tokenize
    result = []
    newline = ''
    step  = ' ' * 8
    align = ' ' * 4
    indent = ''

    for tok in lexer:
        if not tok: break      # No more input
        # print(tok.type, tok.value, tok.lexpos, sep = '\t'*2)

        if tok.type in ("LPARENTHESIS", "LBRACKET"):
######测试代码{
#如果一行代码以(or|and|not) (结尾且不仅仅只包括or|and|not，那么就在or|and|not前换行
            match = re.match('^(?P<head>.*?)\s+(?P<tail>(?:or|and|not))\s*$', newline)
            if match:
                if match.group('head'):
                    result.append(match.group('head'))
                    newline = indent[:-4] + match.group('tail').ljust(4, ' ')
                    # if match.group('tail') == 'or':
                        #or 在行首，额外增加一个空格，以使其能够与and对齐
                        # newline += ' '
                    # result.append(newline)
######测试代码}
            elif newline.endswith(' : '):
                pass
            #  elif re.search(t_CONNECT + '\s*$', newline):
                #  pass
            elif newline.strip() != '':
                newline = newline.rstrip()

            newline += tok.value
            result.append(newline)
            indent += step
            newline = indent

        elif tok.type in ("RPARENTHESIS", "RBRACKET"):
            indent = indent[:-8]

            if 0 < len(newline.strip()) < 40 and result[-1].endswith('('):
                newline = result.pop().rstrip() + newline.strip()
            else:
                result.append(newline.rstrip())
                newline = ''
                newline += indent

            newline += tok.value
            result.append(newline)
            newline = indent

        # elif tok.type == "LBRACKET":
            # newline += tok.value + ''
        # elif tok.type == "RBRACKET":
            # newline = newline.rstrip() + tok.value
            # result.append(newline)
            # newline += indent

        elif tok.type == "KEYWORD":
            match = re.match('(?P<head>\S+?)\s+(?P<tail>or|and|not)\s*$', newline)
            if match:
                # if match.group('head'):
                result.append(match.group('head'))
                newline = indent[:-4] + match.group('tail').ljust(4, ' ')

            newline += tok.value + ' '

        elif tok.type == "EQUAL":
            newline += tok.value + ' '
        elif tok.type == "VALUE":
            if newline.strip() == '' and result[-1].endswith(')'):
                #主要用来处理公司名称中出现的括号
                #当公司名称中有括号时，不要换行
                newline = result.pop()
            newline += tok.value + ' '

        elif tok.type == "CONNECT":
            tok.value = re.sub('\(\s*([1-9]?)\s*([wn])\s*\)', '(\g<1>\g<2>)', tok.value.lower())
            if newline.strip() == '' and result[-1].endswith(')'):
                if result[-1].strip() != ')':
                    #连字符紧跟在右括号后边时，不换行
                    newline = result.pop() + ' '
                    newline += tok.value + ' '
                else:
                    result.append(newline.rstrip())
                    newline = indent
                    newline = newline[:-4]
                    newline += tok.value.ljust(4, ' ')
            else:
                newline += tok.value + ' '
        elif tok.type == "TO":
            newline += tok.value.lower() + ' '
        elif tok.type == "AND":
            if newline.strip() == '':
                if len(newline) < 8:
                    return scFormatter(f'({string})')
                newline = newline[:-4]
            newline += tok.value.lower() + ' '
        elif tok.type == "OR":
            if wcswidth(newline) > 100:
                result.append(newline.rstrip())
                newline = '' + indent

            if newline.strip() == '':
                if len(newline) < 8:
                    return scFormatter(f'({string})')
                newline = newline[:-4]
                newline += tok.value.lower() + '  '
            else:
                newline += tok.value.lower() + ' '
        elif tok.type == "NOT":
            if newline.strip() == '':
                if len(newline) < 8:
                    return scFormatter(f'({string})')
                newline = newline[:-4]
            newline += tok.value.lower() + ' '
    else:
        if newline.strip():
            result.append(newline.rstrip())
        while indent:
            indent = indent[:-8]
            result.append(indent + ')')

        for i in range(1, len(result) - 1):
            if result[i] == '':
                continue
            else:
                l = i - 1
                while(l and result[l] == ''):
                    l -= 1
                n = i + 1
            # if result[l].endswith('(') and len(result[i].strip()) < 50 and result[n].strip() == ')':
                # result[l] += result[i].strip() + result[n].strip()
                # result[i] = ''
                # result[n] = ''
            # elif result[i].lstrip().startswith('(w)') or result[i].lstrip().startswith('(n)'):
                # result[l] += ' ' + result[i].strip()
                # result[i] = ''
        else:
            result = '\n'.join(filter(None, result))

        result = re.sub('\([\n\s]*\)', '', result)#删除空括号对（自动补全括号时，有可能会产生空括号对。
        result = re.sub('^\s*(and|or|not)*\s*$', '', result, flags = re.M)#删除只有and or not的行以及空行。
        result = re.sub(r'[A-Z]([A-Za-z-]*?[A-Za-z])?(?=\s*=\s*)', lambda matched : matched.group(0).lower(), result)
        result = re.sub(r'(?P<quote>")?(?P<ipc>\b(?P<section>[A-H])(?(section)(?P<class>\d{2})?)(?(class)(?P<subclass>[A-Z])?)(?(subclass)(?P<group>\d{1,})?)(?(group)(?:/(?P<subgroup>\d{1,}))?)\b)(?(quote)")',
                        lambda matched : matched.group('ipc').upper(), result, flags = re.IGNORECASE)
        #将所有ipc分类号转为大写
        #  result = re.sub(r'\b(?P<country>am|ap|ar|at|au|ba|be|bg|br|by|ca|ch|cl|cn|co|cr|cs|cu|cy|cz|dd|de|dk|do|dz|ea|ec|ee|eg|ep|es|fi|fr|gb|gc|ge|gr|gt|hk|hn|hr|hu|id|ie|il|in|is|it|jo|jp|ke|kr|kz|lt|lu|lv|ma|mc|md|me|mn|mo|mt|mw|mx|my|ni|nl|no|nz|oa|pa|pe|ph|pl|pt|ro|rs|ru|se|sg|si|sk|sm|su|sv|th|tj|tr|tt|tw|ua|us|uy|uz|vn|wo|yu|za|zm|zw|py|bo|ve|eu|sa|kg|tn|ae|bh|bn|lb)\b(?!\s*=)', lambda matched : matched.group('country').upper(), result, flags = re.IGNORECASE)
        #  将所有国别代码转为大写
        result = re.sub('(\n\))+\n*$', '\n)\n', result)
        result = re.sub('\[[\n\s]*(?P<start>\d{1,4}-?\d{1,2}-?\d{1,2})\s+to\s+(?P<end>\d{1,4}-?\d{1,2}-?\d{1,2})[\n\s]*\]', '[\g<start> to \g<end>]', result) #避免方括号内的日期占用三行空间
        return result.strip()


if __name__ == "__main__":
    import sys
    data = "".join(sys.stdin.readlines()) #接受管道输入的其它参数
    print(scFormatter(data))
