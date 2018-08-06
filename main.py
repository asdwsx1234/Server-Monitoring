#coding=gbk
from tkinter import Frame,Label,StringVar,Button,ttk
import tkinter.messagebox as messagebox
from serverParse import parse
from tcping import ping
import time, threading
import winsound

class SpyThread:
    def __init__(self,dic):
        self._running = True
        self.choosed = dic

    def stop(self):
        self._running = False

    def setChoosed(self,dic):
        self.choosed = dic
        
    def run(self):
        print('thread %s is running...' % threading.current_thread().name)
        while self._running:
            #if ping(self.choosed["ip"],int(self.choosed["port"])) == 1:
            if ping('192.168.8.111',9999) == 1:
                continue
            else:
                winsound.Beep(600,1000)
                messagebox.showinfo('Message', '开服了！冲冲冲！')
                self._running = False
        print('thread %s ended.' % threading.current_thread().name)
        

class Application(Frame):
    st = SpyThread({})
    serverlist = parse()
    fulist = []
    qu = []
    fu = []
    choosed = {}
    tip = "作者：慕卿渊@暗香掠影"
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        Label(self,text="区").grid(row=1)#靠右
        Label(self,text="服").grid(row=2)#第二行，靠左
        self.initQuList()
        self.alertButton = Button(self, text='开始监控', command=self.beginSpy)
        self.alertButton.grid(row=1, column=2)
        self.alertButton1 = Button(self, text='终止', command=self.stopSpy)
        self.alertButton1.grid(row=2, column=2)
        self.alertButton1.configure(state='disable')
        self.frmLT = Frame(width=300, height=100)
        self.frmLT.grid(row=3,padx=80,pady=20)
        self.createText(self.tip)

    def createText(self,text):
        self.label = ttk.Label(self.frmLT,text=self.tip)
        self.label.pack()


    def initQuList(self):
        self.qu=list(self.serverlist.keys())
        comvalue=StringVar()
        self.comboxlist = ttk.Combobox(self, width=12, textvariable=comvalue, state='readonly')
        self.comboxlist["values"]=self.qu
        self.comboxlist.current(0)  #选择第一个
        self.comboxlist.bind("<<ComboboxSelected>>",self.getFuList)
        self.comboxlist.grid(row=1, column=1,padx=10,pady=20)
        comvalue1=StringVar()
        self.comboxlist1 = ttk.Combobox(self, width=12, textvariable=comvalue1, state='readonly')
        self.comboxlist1.grid(row=2, column=1)
        
    def getFuList(self, arg):
        self.fulist=self.serverlist[self.comboxlist.get()]
        arr = []
        for item in self.fulist:
            arr.append(item["name"])
        self.fu = arr
        self.comboxlist1["values"]=self.fu
        self.comboxlist1.current(0)
        self.choosed = self.fulist[0]
        self.comboxlist1.bind("<<ComboboxSelected>>",self.chooseFu)
        
    def chooseFu(self, arg):
        for item in self.fulist:
            if item["name"] == self.comboxlist1.get():
                self.choosed = item
    
    def beginSpy(self):
        if not 'name' in self.choosed:
            messagebox.showinfo('Message', '请先选择服务器')
            return
        if hasattr(self,'t'):
            print(self.t)
        self.t=threading.Thread(target=self.st.run, name='SpyThread-%s'% self.choosed["name"])
        self.st.__init__(self.choosed)
        self.t.start()
        self.alertButton.configure(state='disable')
        self.alertButton1.configure(state='active')
        messagebox.showinfo('Message', '正在监控-%s'% self.choosed["name"])

    def stopSpy(self):
        if self.t.isAlive():
            self.st.stop()
            messagebox.showinfo('Message', '停止监控.')
            self.alertButton.configure(state='active')
            self.alertButton1.configure(state='disable')
        else:
            self.alertButton.configure(state='active')
            self.alertButton1.configure(state='disable')

app = Application()
app.master.title('剑网三开服监控')
app.master.resizable(False, False)
app.mainloop()

#http://jx3gc.autoupdate.kingsoft.com/jx3hd/zhcn_hd/serverlist/serverlist.ini
