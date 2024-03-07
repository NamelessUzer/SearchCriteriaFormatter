#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import webbrowser
from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from tkinter.ttk import *

from ply import lex
from incoPatSearchCriteriaFormatter import scFormatter

url = "http://www.incopat.com/advancedSearch/init"

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('专利检索式格式化工具——By 老林<Kun.Lin#qq.com>')
        self.master.geometry('1200x650+80+60')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.top.columnconfigure(0, weight = 1)
        self.top.columnconfigure(1, weight = 1)
        self.top.columnconfigure(2, weight = 1)
        self.top.columnconfigure(3, weight = 1)
        self.top.columnconfigure(4, weight = 1)
        self.top.rowconfigure(1, weight = 1)

        self.style.configure('TCommand1.TButton', font=('微软雅黑',12))
        self.checkpatbutton = Button(self.top, text='格式化剪贴板中的检索式', command=self.formatStringinClipboard, style='TCommand1.TButton')
        self.checkpatbutton.grid(row = 0, column = 0, sticky = W+E)

        self.exportbutton = Button(self.top, text = '复制检索式到剪贴板', command = self.exportResult, style = 'TCommand1.TButton')
        self.exportbutton.grid(row = 0, column = 1, sticky = W+E)

        self.exportbutton = Button(self.top, text = '复制检索式到剪贴板（单行式）', command = self.exportResult_oneline, style = 'TCommand1.TButton')
        self.exportbutton.grid(row = 0, column = 2, sticky = W+E)

        self.exportbutton = Button(self.top, text = '复制检索要素到剪贴板', command = self.exportElement, style = 'TCommand1.TButton')
        self.exportbutton.grid(row = 0, column = 3, sticky = W+E)

        self.exportbutton = Button(self.top, text = '打开 incoPat', command = self.openBrowser, style = 'TCommand1.TButton')
        self.exportbutton.grid(row = 0, column = 4, sticky = W+E)

        self.Text1Font = Font(font=('Courier New', 10))
        self.textarea = ScrolledText(self.top, font=self.Text1Font)
        self.textarea.grid(row = 1, column = 0, columnspan = 5, sticky = N+E+W+S)


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def formatStringinClipboard(self, event = None):
        try:
            string = self.textarea.clipboard_get().strip()
            if string == '':
                raise
        except:
            print("未在剪贴板中发现文本内容!")
        self.exportbutton = Button(self.top, text = '打开 incoPat', command = self.openBrowser, style = 'TCommand1.TButton')
        self.exportbutton.grid(row = 0, column = 2, sticky = W+E)

        self.Text1Font = Font(font=('Courier New', 10))
        self.textarea = ScrolledText(self.top, font=self.Text1Font)
        self.textarea.grid(row = 1, column = 0, columnspan = 3, sticky = N+E+W+S)


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def formatStringinClipboard(self, event = None):
        try:
            string = self.textarea.clipboard_get().strip()
            if string == '':
                raise
            string = re.sub(r'[\s\n]+', ' ', string)
            string = scFormatter(string)
        except IndexError as e:
            #  print("剪贴板中的检索式不正确")
            #  print(e)
            raise
        except:
            print("未在剪贴板中发现文本内容!")
        else:
            self.textarea.delete('1.0', END)
            self.textarea.insert(END, string)

    def exportResult(self, event = None):
        text = self.textarea.get('1.0', END)
        if text:
            self.textarea.clipboard_clear()
            self.textarea.clipboard_append(text)
        return text or ''

    def exportResult_oneline(self, event = None):
        text = self.textarea.get('1.0', END)
        if text:
            text = re.sub(r'[\s\n]+', ' ', text)
            text = re.sub(r'(?<=[(\[])[\s\n\t ]+|[\s\n\t]+(?=[)\]])', '', text)
            text = re.sub(r' *(\(\d?[wWnN]\)) *', r' \g<1> ', text)
            self.textarea.clipboard_clear()
            self.textarea.clipboard_append(text)
        return text or ''

    def getElement(self, string):
        # Build the lexer
        lexer = lex.lex()

        if string.strip() == '':
            return
        # Give the lexer some input
        lexer.input(f'{string}')

        result = []
        # result = list(tok.value for tok in filter(lambda tok: tok.type == 'VALUE', lexer))

        for tok in lexer:
            if not tok: break
            if tok.type == "VALUE" and tok.value not in result:
                result.append(tok.value)
        else:
            return ' '.join(result)


    def exportElement(self, event = None):
        text = self.textarea.get('1.0', END)
        if text:
            self.textarea.clipboard_clear()
            text = self.getElement(text)
            self.textarea.clipboard_append(text)
        return text or ''

    def openBrowser(self, event = None):
        webbrowser.open(url)


if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
    try: top.destroy()
    except: pass
