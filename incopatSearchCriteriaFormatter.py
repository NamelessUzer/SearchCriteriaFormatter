#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re

from ply import lex

KEYWORD_regex_string = r'(ab|ab-otlang|ab-ts|abo|ad|adm|ady|aee|aeenor|agc|all|an|ann|aor|ap|ap-add|ap-country|ap-or|ap-ot|ap-otadd|ap-pc|ap-province|ap-ts|ap-type|apnor|assign-city|assign-country|assign-date|assign-flag|assign-party|assign-state|assign-text|assignee-add|assignee-cadd|assignyear|at|at-add|at-city|at-country|at-state|auth|bclas1|bclas2|bclas3|cf|cfn|city|claim|claim-en|claim-or|claim-ts|class|cn-dc|county|cp-dc|cpc|cpc-class|cpc-group|cpc-section|cpc-subclass|cpc-subgroup|ct|ct-ad|ct-ap|ct-auth|ct-code|ct-no|ct-pd|ct-times|ctfw|ctfw-ad|ctfw-ap|ctfw-auth|ctfw-no|ctfw-pd|ctfw-times|ctnp|ctyear|customs-flag|des|des-or|doc-dc|ecd|ecla|ecla-class|ecla-group|ecla-section|ecla-subclass|ecla-subgroup|ex|ex-time|expiry-date|fa-country|fam-dc|fc-dc|fct|fct-ap|fct-times|fctfw|fctfw-ap|fctfw-times|fi|filing-lang|ft|full|grant-date|ian|if|ifn|in|in-add|in-ap|in-city|in-country|in-state|ipc|ipc-class|ipc-group|ipc-main|ipc-section|ipc-subclass|ipc-subgroup|ipcm-class|ipcm-group|ipcmaintt|ipcm-section|ipcm-subclass|ipn|lawtxt|lee|lee-current|lg|lgc|lgd|lge|lgf|lgi-case|lgi-court|lgi-date|lgi-defendant|lgi-firm|lgi-flag|lgi-judge|lgi-no|lgi-party|lgi-plantiff|lgi-region|lgi-text|lgi-ti|lgi-type|lgiyear|licence-flag|license-cs|license-date|license-no|license-sd|license-stage|license-td|license-type|licenseyear|loc|lor|mf|mfn|no-claim|number|page|patent-life|patentee|patenteenor|pc-cn|pd|pdm|pdy|pee|pee-current|pfex-time|phc|pledge-cd|pledge-date|pledge-no|pledge-rd|pledge-stage|pledge-term|pledge-type|pledgeyear|plege-flag|pn|pnc|pnk|pnn|por|pr|pr-au|pr-date|prd|prn|pryear|pt|pu-date|re-ap|ree-flag|ref-dc|reward-level|reward-name|reward-session|ri-ae|ri-ap|ri-basis|ri-date|ri-inernal|ri-leader|ri-me|ri-num|ri-point|ri-text|ri-type|riyear|status|status-lite|std-company|std-etsi|std-flag|std-num|subex-date|ti|ti-otlang|ti-ts|tiab|tiabc|tio|uc|uc-main|vlstar|who|ap|ap-or|ap-ot|ap-ts|apnor|aee|aor|assign-party|aeenor|ap-otadd|in|lor|lee|lgi-party|at|agc|re-ap|in-ap|ri-me|ri-ae|ri-leader|por|pee|ex|ap-type|who|patentee|patenteenor|aptt|ap-ortt|ap-ottt|ap-tstt|apnortt|aeett|aortt|assign-partytt|aeenortt|ap-otaddtt|intt|lortt|leett|lgi-partytt|attt|agctt|re-aptt|in-aptt|ri-mett|ri-aett|ri-leadertt|portt|peett|extt|ap-typett|whott|patenteett|patenteenortt)(?=\s*=)'
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
t_EQUAL        = r'='
t_CONNECT      = r'\(\s*[1-9]?[wWnN]\s*\)'
t_LPARENTHESIS = r'\('
t_RPARENTHESIS = r'\)'
t_LBRACKET     = r'\['
t_RBRACKET     = r'\]'

def t_KEYWORD(t):
    r'(ab|ab-otlang|ab-ts|abo|ad|adm|ady|aee|aeenor|agc|all|an|ann|aor|ap|ap-add|ap-country|ap-or|ap-ot|ap-otadd|ap-pc|ap-province|ap-ts|ap-type|apnor|assign-city|assign-country|assign-date|assign-flag|assign-party|assign-state|assign-text|assignee-add|assignee-cadd|assignyear|at|at-add|at-city|at-country|at-state|auth|bclas1|bclas2|bclas3|cf|cfn|city|claim|claim-en|claim-or|claim-ts|class|cn-dc|county|cp-dc|cpc|cpc-class|cpc-group|cpc-section|cpc-subclass|cpc-subgroup|ct|ct-ad|ct-ap|ct-auth|ct-code|ct-no|ct-pd|ct-times|ctfw|ctfw-ad|ctfw-ap|ctfw-auth|ctfw-no|ctfw-pd|ctfw-times|ctnp|ctyear|customs-flag|des|des-or|doc-dc|ecd|ecla|ecla-class|ecla-group|ecla-section|ecla-subclass|ecla-subgroup|ex|ex-time|expiry-date|fa-country|fam-dc|fc-dc|fct|fct-ap|fct-times|fctfw|fctfw-ap|fctfw-times|fi|filing-lang|ft|full|grant-date|ian|if|ifn|in|in-add|in-ap|in-city|in-country|in-state|ipc|ipc-class|ipc-group|ipc-main|ipc-section|ipc-subclass|ipc-subgroup|ipcm-class|ipcm-group|ipcmaintt|ipcm-section|ipcm-subclass|ipn|lawtxt|lee|lee-current|lg|lgc|lgd|lge|lgf|lgi-case|lgi-court|lgi-date|lgi-defendant|lgi-firm|lgi-flag|lgi-judge|lgi-no|lgi-party|lgi-plantiff|lgi-region|lgi-text|lgi-ti|lgi-type|lgiyear|licence-flag|license-cs|license-date|license-no|license-sd|license-stage|license-td|license-type|licenseyear|loc|lor|mf|mfn|no-claim|number|page|patent-life|patentee|patenteenor|pc-cn|pd|pdm|pdy|pee|pee-current|pfex-time|phc|pledge-cd|pledge-date|pledge-no|pledge-rd|pledge-stage|pledge-term|pledge-type|pledgeyear|plege-flag|pn|pnc|pnk|pnn|por|pr|pr-au|pr-date|prd|prn|pryear|pt|pu-date|re-ap|ree-flag|ref-dc|reward-level|reward-name|reward-session|ri-ae|ri-ap|ri-basis|ri-date|ri-inernal|ri-leader|ri-me|ri-num|ri-point|ri-text|ri-type|riyear|status|status-lite|std-company|std-etsi|std-flag|std-num|subex-date|ti|ti-otlang|ti-ts|tiab|tiabc|tio|uc|uc-main|vlstar|who|ap|ap-or|ap-ot|ap-ts|apnor|aee|aor|assign-party|aeenor|ap-otadd|in|lor|lee|lgi-party|at|agc|re-ap|in-ap|ri-me|ri-ae|ri-leader|por|pee|ex|ap-type|who|patentee|patenteenor|aptt|ap-ortt|ap-ottt|ap-tstt|apnortt|aeett|aortt|assign-partytt|aeenortt|ap-otaddtt|intt|lortt|leett|lgi-partytt|attt|agctt|re-aptt|in-aptt|ri-mett|ri-aett|ri-leadertt|portt|peett|extt|ap-typett|whott|patenteett|patenteenortt)(?=\s*=)'
    t.type = 'KEYWORD'
    t.value = t.value.lower()
    return t

# A regular expression rule with some action code
def t_VALUE(t):
    # r'(?P<quote>")?[^\(\)\[\]\s=]+(?(quote)")'
    r'"[^="]+"|[^=\s\(\)\[\]]+'
    t.type = reserved.get(t.value.lower(), 'VALUE')
    t.value = re.sub(' +', ' ', t.value)#将多个连续的空格替换为单个空格
    t.value = re.sub('(?<=")[\s\n\t ]+|[\s\n\t]+(?=")', '', t.value)#将紧靠双引号内侧的空格删除
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
            elif newline.endswith(' = '):
                pass
            elif re.search(t_CONNECT + '\s*$', newline):
                pass
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
            if len(newline) > 100:
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
        result = re.sub(r'\b(?P<country>am|ap|ar|at|au|ba|be|bg|br|by|ca|ch|cl|cn|co|cr|cs|cu|cy|cz|dd|de|dk|do|dz|ea|ec|ee|eg|ep|es|fi|fr|gb|gc|ge|gr|gt|hk|hn|hr|hu|id|ie|il|in|is|it|jo|jp|ke|kr|kz|lt|lu|lv|ma|mc|md|me|mn|mo|mt|mw|mx|my|ni|nl|no|nz|oa|pa|pe|ph|pl|pt|ro|rs|ru|se|sg|si|sk|sm|su|sv|th|tj|tr|tt|tw|ua|us|uy|uz|vn|wo|yu|za|zm|zw|py|bo|ve|eu|sa|kg|tn|ae|bh|bn|lb)\b(?!\s*=)', lambda matched : matched.group('country').upper(), result, flags = re.IGNORECASE)
        #将所有国别代码转为大写
        result = re.sub('(\n\))+\n*$', '\n)\n', result)
        result = re.sub('\[[\n\s]*(?P<start>\d{1,8})\s*to\s*(?P<end>\d{1,8})[\n\s]*\]', '[\g<start> to \g<end>]', result)#避免方括号内的日期占用三行空间
        return result.strip()


if __name__ == "__main__":
    import sys
    data = "".join(sys.stdin.readlines()[:-1]) #接受管道输入的其它参数
    print(scFormatter(data))
