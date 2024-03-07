#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re

from ply import lex
from wcwidth import wcswidth

KEYWORD_regex_string = r'''(
    r|rad|rpd|
    ti|ab|tiab-dwpi|claim|ipc|loc|an|rand-DWPI|ad|pn|pd|ap|aee|ap-add|ap-country|in|in-DWPI|lor|lee|lg|ri-text|status|lgi-party|
    ti|ti-cn|ti-otlang|ti-en|ti-dwpi|ab|ab-cn|ab-otlang|ab-en|use-dwpi|adv-dwpi|novelty-dwpi|abstract-dwpi|DTD-DWPI|ACTIVITY-DWPI|MEC-DWPI|FOC-DWPI|DRAW-DWPI|tiab|tiab-dwpi|claim|first-claim|first-claim-or|indepclaims-cn|depclaims-cn|no-indepclaims|no-depclaims|first-claim-ts|len-first-claim|Claim-EN|Claim-CN|Claim-OT|no-claim|tiabc|des|des-ot|des-en|des-cn|technical-field|background-art|disclosure|mode-for-invention|use-cn|use-en|effect-s-cn|effect-ph-cn|effect-cn|effect-cn-3|effect-cn-2|effect-cn-1|effect-triz|all|full|filing-lang|prd|PRD-DWPI|page|vlstar|vlstar-1|vlstar-2|vlstar-3|reward-level|reward-name|reward-session|std-type|std-Project|std-num|std-company|std-flag|cas-no|drug-name-cn|drug-name-en|company|Brand-Name|active-ingredient|Target|indication|patent-expiration|PED-patent-expiration|
    ap|ap-group|ap-grouptt|AP-ALL|aptt|CO-DWPI|ap-or|ap-ot|ap-ts|apnor|ap-first|no-ap|aee|aeett|aor|assign-party|aeenor|AOR-TYPE|intt|AEE-TYPE|ap-otadd|in|in-or|in-ot|in-ts|in-first|no-in|in-new-name|in-current|lor|lee|LOR-TYPE|LEE-TYPE|lgi-party|at|agc|re-ap|in-ap|ri-me|ri-ae|ri-leader|por|pee|ex|ap-type|ck-DWPI|CK-TYPE-DWPI|who|patentee|patenteett|patenteenor|ap-new-name|ap-as|ap-en|ap-reg-location|ap-company-org-type|ap-estiblish-time|ap-usc|ap-reg-number|ap-reg-status|ap-list-code|opponent|
    ipc|ipc-main|ipc-section|ipc-class|ipc-subclass|ipc-group|IPCM-Section|IPCM-Class|IPCM-Subclass|IPCM-Group|ipc-subgroup|ipc-low|ipc-high|IPCM-Low|IPCM-High|IPC-DWPI|IPC-Section-dwpi|IPC-Class-dwpi|loc|IPC-Subclass-DWPI|IPC-GROUP-dwpi|IPC-Subgroup-DWPI|IPC-f-DWPI|IPC-Section-f-dwpi|IPC-Class-f-dwpi|IPC-Subclass-f-DWPI|IPC-GROUP-f-dwpi|IPC-Subgroup-f-DWPI|DC-DWPI|DC-SECTION-DWPI|DC-CLASS-DWPI|MC-DWPI|MC-section-DWPI|MC-class-DWPI|MC-group-DWPI|MC-subgroup-DWPI|MC-subgroupd-DWPI|MC-fullmc-DWPI|MC-fullmcx-DWPI|loc-class|loc|loc-subclass|ecla|ecla-section|ecla-class|ecla-subclass|ecla-group|ecla-subgroup|uc|uc-main|cpc|cpc-section|cpc-class|cpc-subclass|cpc-group|cpc-subgroup|fi|bclass|mbclas1|mbclas2|mbclas3|mbclas4|mbclass|ft|Class|bclas1|bclas2|bclas3|bclas4|cpc-main|cpcm-section|cpcm-class|cpcm-subclass|cpcm-group|cpcm-subgroup|industry1|mindustry1|mindustry2|industry2|Industry-type|Mkclas1|Mkclas2|sc-main|sc-section|sc-class|sc-subclass|Lngclas1|Lngclas2|Lngclas3|Cpclas1|Cpclas2|Cpclas3|digclas1|digclas2|digclas3|
    ap-country|in-country|auth|pnc|ap-add|pr-au|pr-au-DWPI|ORIPRC-DWPI|ap-province|pc-cn|ap-pc|city|county|PATENTEE-ADD|PATENTEE-PROVINCE|PATENTEE-CITY|PATENTEE-COUNTY|in-add|IN-ADD-OTH|IN-OR-ADD|in-city|in-state|assign-country|assignee-add|assignee-cadd|assign-state|assign-city|AEE-PROVINCE|AEE-CITY|AEE-COUNTY|ASSIGNOR-ADD|AOR-PROVINCE|AOR-CITY|AOR-COUNTY|at-country|at-add|at-city|at-state|lgi-region|where|
    ap-country|in-country|auth|pnc|ap-add|pr-au|pr-au-DWPI|ORIPRC-DWPI|ap-province|pc-cn|ap-pc|city|county|PATENTEE-ADD|PATENTEE-PROVINCE|PATENTEE-CITY|PATENTEE-COUNTY|in-add|IN-ADD-OTH|IN-OR-ADD|in-city|in-state|assign-country|assignee-add|assignee-cadd|assign-state|assign-city|AEE-PROVINCE|AEE-CITY|AEE-COUNTY|ASSIGNOR-ADD|AOR-PROVINCE|AOR-CITY|AOR-COUNTY|at-country|at-add|at-city|at-state|lgi-region|where|
    ad|radd-DWPI|adm|ady|pd|PU-DATE|pdy|pdm|pr-date|pr-date-DWPI|pryear|ori-prdate|ct-ad|ct-pd|ctfw-ad|ctfw-pd|ctyear|subex-date|GRANT-DATE|EXDT|expiry-date|expiry-year|ecd|pledgeyear|assignyear|licenseyear|assign-date|assign-rd|ri-date|lgi-date|lgi-fd|lgi-cd|lgd|pledge-date|license-date|license-sd|license-td|pledge-cd|pledge-rd|lgiyear|lgi-fy|lgi-cy|patent-life|ex-time|pfex-time|re-date|in-date|or-date|reapp-date|inapp-date|ori-pryear|ori-pryear-DWPI|
    status|status-lite|lg|lge|lgf|lgc|ri-type|ri-text|ri-ap|inapp-date|re-decision|ri-basis|ri-point|lgi-court|lgi-judge|lgi-firm|lawyer|lgi-cause|assign-text|lgi-ti|lgi-text|lgi-type|lgi-no|lgi-procedure|lgi-plaintiff|lgi-defendant|license-type|license-stage|license-cs|lee-current|pee-current|pledge-type|pledge-stage|lawtxt|assign-flag|Assign-times|assign-no|licence-flag|Licence-times|plege-flag|pledge-times|ree-flag|lgi-flag|Lgi-times|action-types|customs-Flag|all-flag|Tovalide-date|
    ct|ctfw|ct-self|ct-oth|ctfw-self|ctfw-oth|ct-times|ctfw-times|ct-self-times|ct-oth-times|ctfw-self-times|ctfw-oth-times|fct|fctfw|ct-ap|ctfw-ap|fct-ap|fctfw-ap|ct-no|ctfw-no|ct-auth|ctfw-auth|ct-code|ct-X|fct-times|fctfw-times|ctnp|ct-source|ctfw-source
)(?=\s*=)'''

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
    r'''(
    r|rad|rpd|
    ti|ab|tiab-dwpi|claim|ipc|loc|an|rand-DWPI|ad|pn|pd|ap|aee|ap-add|ap-country|in|in-DWPI|lor|lee|lg|ri-text|status|lgi-party|
    ti|ti-cn|ti-otlang|ti-en|ti-dwpi|ab|ab-cn|ab-otlang|ab-en|use-dwpi|adv-dwpi|novelty-dwpi|abstract-dwpi|DTD-DWPI|ACTIVITY-DWPI|MEC-DWPI|FOC-DWPI|DRAW-DWPI|tiab|tiab-dwpi|claim|first-claim|first-claim-or|indepclaims-cn|depclaims-cn|no-indepclaims|no-depclaims|first-claim-ts|len-first-claim|Claim-EN|Claim-CN|Claim-OT|no-claim|tiabc|des|des-ot|des-en|des-cn|technical-field|background-art|disclosure|mode-for-invention|use-cn|use-en|effect-s-cn|effect-ph-cn|effect-cn|effect-cn-3|effect-cn-2|effect-cn-1|effect-triz|all|full|filing-lang|prd|PRD-DWPI|page|vlstar|vlstar-1|vlstar-2|vlstar-3|reward-level|reward-name|reward-session|std-type|std-Project|std-num|std-company|std-flag|cas-no|drug-name-cn|drug-name-en|company|Brand-Name|active-ingredient|Target|indication|patent-expiration|PED-patent-expiration|
    ap|ap-group|ap-grouptt|AP-ALL|aptt|CO-DWPI|ap-or|ap-ot|ap-ts|apnor|ap-first|no-ap|aee|aeett|aor|assign-party|aeenor|AOR-TYPE|intt|AEE-TYPE|ap-otadd|in|in-or|in-ot|in-ts|in-first|no-in|in-new-name|in-current|lor|lee|LOR-TYPE|LEE-TYPE|lgi-party|at|agc|re-ap|in-ap|ri-me|ri-ae|ri-leader|por|pee|ex|ap-type|ck-DWPI|CK-TYPE-DWPI|who|patentee|patenteett|patenteenor|ap-new-name|ap-as|ap-en|ap-reg-location|ap-company-org-type|ap-estiblish-time|ap-usc|ap-reg-number|ap-reg-status|ap-list-code|opponent|
    ipc|ipc-main|ipc-section|ipc-class|ipc-subclass|ipc-group|IPCM-Section|IPCM-Class|IPCM-Subclass|IPCM-Group|ipc-subgroup|ipc-low|ipc-high|IPCM-Low|IPCM-High|IPC-DWPI|IPC-Section-dwpi|IPC-Class-dwpi|loc|IPC-Subclass-DWPI|IPC-GROUP-dwpi|IPC-Subgroup-DWPI|IPC-f-DWPI|IPC-Section-f-dwpi|IPC-Class-f-dwpi|IPC-Subclass-f-DWPI|IPC-GROUP-f-dwpi|IPC-Subgroup-f-DWPI|DC-DWPI|DC-SECTION-DWPI|DC-CLASS-DWPI|MC-DWPI|MC-section-DWPI|MC-class-DWPI|MC-group-DWPI|MC-subgroup-DWPI|MC-subgroupd-DWPI|MC-fullmc-DWPI|MC-fullmcx-DWPI|loc-class|loc|loc-subclass|ecla|ecla-section|ecla-class|ecla-subclass|ecla-group|ecla-subgroup|uc|uc-main|cpc|cpc-section|cpc-class|cpc-subclass|cpc-group|cpc-subgroup|fi|bclass|mbclas1|mbclas2|mbclas3|mbclas4|mbclass|ft|Class|bclas1|bclas2|bclas3|bclas4|cpc-main|cpcm-section|cpcm-class|cpcm-subclass|cpcm-group|cpcm-subgroup|industry1|mindustry1|mindustry2|industry2|Industry-type|Mkclas1|Mkclas2|sc-main|sc-section|sc-class|sc-subclass|Lngclas1|Lngclas2|Lngclas3|Cpclas1|Cpclas2|Cpclas3|digclas1|digclas2|digclas3|
    ap-country|in-country|auth|pnc|ap-add|pr-au|pr-au-DWPI|ORIPRC-DWPI|ap-province|pc-cn|ap-pc|city|county|PATENTEE-ADD|PATENTEE-PROVINCE|PATENTEE-CITY|PATENTEE-COUNTY|in-add|IN-ADD-OTH|IN-OR-ADD|in-city|in-state|assign-country|assignee-add|assignee-cadd|assign-state|assign-city|AEE-PROVINCE|AEE-CITY|AEE-COUNTY|ASSIGNOR-ADD|AOR-PROVINCE|AOR-CITY|AOR-COUNTY|at-country|at-add|at-city|at-state|lgi-region|where|
    ap-country|in-country|auth|pnc|ap-add|pr-au|pr-au-DWPI|ORIPRC-DWPI|ap-province|pc-cn|ap-pc|city|county|PATENTEE-ADD|PATENTEE-PROVINCE|PATENTEE-CITY|PATENTEE-COUNTY|in-add|IN-ADD-OTH|IN-OR-ADD|in-city|in-state|assign-country|assignee-add|assignee-cadd|assign-state|assign-city|AEE-PROVINCE|AEE-CITY|AEE-COUNTY|ASSIGNOR-ADD|AOR-PROVINCE|AOR-CITY|AOR-COUNTY|at-country|at-add|at-city|at-state|lgi-region|where|
    ad|radd-DWPI|adm|ady|pd|PU-DATE|pdy|pdm|pr-date|pr-date-DWPI|pryear|ori-prdate|ct-ad|ct-pd|ctfw-ad|ctfw-pd|ctyear|subex-date|GRANT-DATE|EXDT|expiry-date|expiry-year|ecd|pledgeyear|assignyear|licenseyear|assign-date|assign-rd|ri-date|lgi-date|lgi-fd|lgi-cd|lgd|pledge-date|license-date|license-sd|license-td|pledge-cd|pledge-rd|lgiyear|lgi-fy|lgi-cy|patent-life|ex-time|pfex-time|re-date|in-date|or-date|reapp-date|inapp-date|ori-pryear|ori-pryear-DWPI|
    status|status-lite|lg|lge|lgf|lgc|ri-type|ri-text|ri-ap|inapp-date|re-decision|ri-basis|ri-point|lgi-court|lgi-judge|lgi-firm|lawyer|lgi-cause|assign-text|lgi-ti|lgi-text|lgi-type|lgi-no|lgi-procedure|lgi-plaintiff|lgi-defendant|license-type|license-stage|license-cs|lee-current|pee-current|pledge-type|pledge-stage|lawtxt|assign-flag|Assign-times|assign-no|licence-flag|Licence-times|plege-flag|pledge-times|ree-flag|lgi-flag|Lgi-times|action-types|customs-Flag|all-flag|Tovalide-date|
    ct|ctfw|ct-self|ct-oth|ctfw-self|ctfw-oth|ct-times|ctfw-times|ct-self-times|ct-oth-times|ctfw-self-times|ctfw-oth-times|fct|fctfw|ct-ap|ctfw-ap|fct-ap|fctfw-ap|ct-no|ctfw-no|ct-auth|ctfw-auth|ct-code|ct-X|fct-times|fctfw-times|ctnp|ct-source|ctfw-source
)(?=\s*=)'''
    t.type = 'KEYWORD'
    t.value = t.value.lower()
    return t

# A regular expression rule with some action code
def t_VALUE(t):
    # r'(?P<quote>")?[^\(\)\[\]\s=]+(?(quote)")'
    r'"[^="]+"|[^=\s\(\)\[\]]+'
    t.type = reserved.get(t.value.lower(), 'VALUE')
    t.value = re.sub(' +', ' ', t.value)#将多个连续的空格替换为单个空格
    t.value = re.sub(r'(?<=")[\s\n\t ]+|[\s\n\t]+(?=")', '', t.value)#将紧靠双引号内侧的空格删除
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
            match = re.match(r'^(?P<head>.*?)\s+(?P<tail>(?:or|and|not))\s*$', newline)
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
            elif re.search(t_CONNECT + r'\s*$', newline):
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
            match = re.match(r'(?P<head>\S+?)\s+(?P<tail>or|and|not)\s*$', newline)
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
            tok.value = re.sub(r'\(\s*([1-9]?)\s*([wn])\s*\)', r'(\g<1>\g<2>)', tok.value.lower())
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

        result = re.sub(r'\([\n\s]*\)', '', result)#删除空括号对（自动补全括号时，有可能会产生空括号对。
        result = re.sub(r'^\s*(and|or|not)*\s*$', '', result, flags = re.M)#删除只有and or not的行以及空行。
        result = re.sub(r'[A-Z]([A-Za-z-]*?[A-Za-z])?(?=\s*=\s*)', lambda matched : matched.group(0).lower(), result)
        result = re.sub(r'(?P<quote>")?(?P<ipc>\b(?P<section>[A-H])(?(section)(?P<class>\d{2})?)(?(class)(?P<subclass>[A-Z])?)(?(subclass)(?P<group>\d{1,})?)(?(group)(?:/(?P<subgroup>\d{1,}))?)\b)(?(quote)")',
                        lambda matched : matched.group('ipc').upper(), result, flags = re.IGNORECASE)
        #将所有ipc分类号转为大写
        result = re.sub(r'\b(?P<country>am|ap|ar|at|au|ba|be|bg|br|by|ca|ch|cl|cn|co|cr|cs|cu|cy|cz|dd|de|dk|do|dz|ea|ec|ee|eg|ep|es|fi|fr|gb|gc|ge|gr|gt|hk|hn|hr|hu|id|ie|il|in|is|it|jo|jp|ke|kr|kz|lt|lu|lv|ma|mc|md|me|mn|mo|mt|mw|mx|my|ni|nl|no|nz|oa|pa|pe|ph|pl|pt|ro|rs|ru|se|sg|si|sk|sm|su|sv|th|tj|tr|tt|tw|ua|us|uy|uz|vn|wo|yu|za|zm|zw|py|bo|ve|eu|sa|kg|tn|ae|bh|bn|lb)\b(?!\s*=)', lambda matched : matched.group('country').upper(), result, flags = re.IGNORECASE)
        #将所有国别代码转为大写
        result = re.sub(r'(\n\))+\n*$', '\n)\n', result)
        result = re.sub(r'\[[\n\s]*(?P<start>\d{1,8})\s*to\s*(?P<end>\d{1,8})[\n\s]*\]', r'[\g<start> to \g<end>]', result)#避免方括号内的日期占用三行空间
        return result.strip()


if __name__ == "__main__":
    import sys
    data = "".join(sys.stdin.readlines()) #接受管道输入的其它参数
    print(scFormatter(data))
