import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
import datetime
from collections import deque
global nonemergency
global emergency
global call
nonemergency = [] 
emergency = []
file1 = open("databaseemergency.txt","r")
read1 = file1.readline()
file1.close()
file2 = open("databasenonemergency.txt","r")
read2 = file2.readline()
file2.close()

if len(read1) == 0:
    file1 = open("databaseemergency.txt","w")
    file1.write(str(emergency)+"\n")
    file1.close()
else:
    emergency = eval(read1)
if len(read2) == 0:
    file2 = open("databasenonemergency.txt","w")
    file2.write(str(nonemergency)+"\n")
    file2.close()
else:
    nonemergency = eval(read2)
call = []


class firstpage(QDialog):
    def __init__(self):
        super(firstpage, self).__init__()   #use init of QDialog
        loadUi("firstpage.ui",self)
        self.gotoinfopage.clicked.connect(self.gogoinfo)
        self.seeque.clicked.connect(self.gogocq)
        self.searchque.clicked.connect(self.banana)
        #เปิดโปรแกรมมาเช็ค databaseemergency ก่อนส ละดึงใส่ nonemergency&emergenvcy
        global allinfo
        allinfo = emergency + nonemergency  
       
        
    #go to info page
    def gogoinfo(self):
        info = infopage()
        widget.addWidget(info)#currently firstpage is widget A and info page is widget A+1
        widget.setCurrentIndex(widget.currentIndex()+1)#go to info page by set index A+1
    def gogocq(self):
        qqq = queuepage()
        widget.addWidget(qqq)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def banana(self):
        searchq = searchpage()
        widget.addWidget(searchq)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class infopage(QDialog):
    def __init__(self):
        super(infopage, self).__init__()
        loadUi("infopage.ui",self)
        print(emergency)
        nam = ""
        descrip = ""
        prior = ""
        timae = ""
        self.confirm.clicked.connect(self.confirmna)
        self.returnbutt.clicked.connect(self.rere)
    def rere(self): #go back to first page without finishing input info
        first = firstpage()
        widget.addWidget(first)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def confirmna(self):
        currenttime = datetime.datetime.now()
        hours = currenttime.strftime('%H')
        minutes = currenttime.strftime('%M')
        global timae
        timae = hours + ":" + minutes
        global nam
        nam = self.name.text()
        global descrip
        descrip = self.description.toPlainText()
        global prior
        prior = self.priority.currentText()
        global new
        if nam == "" or descrip == "":
            print("Error")
            self.error.setText("Fill Out All Fields")
        else:
            if prior == "Emergency":            #ดู count จาก index new ใน list emergency ละก็ใช้ counte ต่อจากเลขเดิม ถ้า list ว่าง ให้  count เป็น 1  
                if len(emergency) == 0:
                    counte = 1
                else:
                    temp = emergency[(len(emergency))-1][4]
                    counte = int(temp[1:])
                    counte = counte + 1

                new = "E" + str(counte)
                data = [nam,descrip,prior, timae, new]
                emergency.append(data)
                print(emergency)
            elif prior == "Non-Emergency":      #เหมือนกัน
                if len(nonemergency) == 0:
                    countn = 1
                else:
                    print(emergency)
                    temp = nonemergency[(len(nonemergency))-1][4]
                    countn = int(temp[1:])
                    countn = countn + 1
               
                new = "N" + str(countn)
                data = [nam,descrip,prior, timae, new]
                nonemergency.append(data)

            print(emergency)
            print(nonemergency)
            qqq = afterinfo()
            widget.addWidget(qqq)
            widget.setCurrentIndex(widget.currentIndex()+1)
            #ใส่ databaseemergency หลัง insert
            file1 = open("databaseemergency.txt","w")
            file1.write(str(emergency)+"\n")
            file1.close()
            file2 = open("databasenonemergency.txt","w")
            file2.write(str(nonemergency)+"\n")
            file2.close()
        #move to next page to show queue (To be done)


class afterinfo(QDialog): #missing show queue
    def __init__(self):
        super(afterinfo,self).__init__()
        loadUi("afterinfo.ui",self)
        self.nameafter.setText(nam)
        self.descriptionafter.setText(descrip)
        self.priorityafter.setText(prior)
        self.arrivalafter.setText(timae)
        self.returnbutt.clicked.connect(self.rere)

        self.queueafter.setText(str(new))
    def rere(self):
        first = firstpage()
        widget.addWidget(first)
        widget.setCurrentIndex(widget.currentIndex()+1)

        
class queuepage(QDialog):
    def __init__(self):
        super(queuepage,self).__init__()
        loadUi("queuepage.ui",self)
        self.tableWidget.setColumnWidth(0, 340)
        self.tableWidget.setColumnWidth(1, 340)
        self.tableWidget.setColumnWidth(2, 340)
        count = 1
        table = 0
        rowcount =1
        self.removeq.clicked.connect(self.removena)
        self.returnbutt.clicked.connect(self.rere)
        if call != []:
            self.nameafter.setText(call[0])
            self.queueafter.setText(call[4])
            self.priorityafter.setText(call[2])
            self.arrivalafter.setText(call[1])
        for i in range(len(allinfo)):

            self.tableWidget.setRowCount(rowcount)
            self.tableWidget.setRowHeight(table, 25)
            self.tableWidget.setItem(table, 0, QtWidgets.QTableWidgetItem(str(allinfo[i][4])))
            self.tableWidget.setItem(table, 1, QtWidgets.QTableWidgetItem(str(allinfo[i][3])))
            self.tableWidget.setItem(table, 2, QtWidgets.QTableWidgetItem(str(allinfo[i][2])))
            table += 1
            rowcount +=1 
            count+=1

    def rere(self):
        first = firstpage()
        widget.addWidget(first)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def removena(self):
        global emergency
        global nonemergency
        global allinfo
        global call
        try:
            newasdeque = deque(emergency)
            call = newasdeque.popleft()
            emergency = list(newasdeque)
        except:
            try:
                newasdeque = deque(nonemergency)
                call = newasdeque.popleft()
                nonemergency = list(newasdeque)
            except:
                call = []
        allinfo = emergency + nonemergency
        file1 = open("databaseemergency.txt","w")
        file1.write(str(emergency)+"\n")
        file1.close()
        file2 = open("databasenonemergency.txt","w")
        file2.write(str(nonemergency)+"\n")
        file2.close()
        #แก้ databaseemergency อีกรอบ
        again = queuepage()
        widget.addWidget(again)
        widget.setCurrentIndex(widget.currentIndex()+1)
        #cแก้ databaseemergency

class searchpage(QDialog):
    def __init__(self):
        super(searchpage, self).__init__()
        loadUi("searchpage.ui",self)
        self.returnbutt.clicked.connect(self.rere)
        self.confirm.clicked.connect(self.confirming)
        self.label_4.setText("Your Queue: ")
    def rere(self):
        first = firstpage()
        widget.addWidget(first)
        widget.setCurrentIndex(widget.currentIndex()+1)
    def confirming(self):
        count = 0
        temp = self.name.text()
        searchby = self.priority.currentText()
        if len(allinfo) == 0:
            self.label_4.setText("Your Queue: Invalid")
        if searchby == "Name":
            for i in range (len(allinfo)):
                print(temp, allinfo[i][0])
                if temp == allinfo[i][0]:
                    self.label_4.setText("Your Queue: " + str(i+1))
                    count = 1
                else:
                    if count == 0:
                        self.label_4.setText("Your Queue: Invalid")
        elif searchby == "Queue Number":
            for i in range (len(allinfo)):
                print(temp, allinfo[i][4])
                if temp == allinfo[i][4]:
                    self.label_4.setText("Your Queue: " + str(i+1))
                    count = 1
                else:
                    if count == 0:
                        self.label_4.setText("Your Queue: Invalid")

app = QApplication(sys.argv)
first = firstpage()
widget = QtWidgets.QStackedWidget() 
widget.addWidget(first) #add and set up the first page
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
sys.exit(app.exec_()) #exit
