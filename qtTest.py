import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import tempMatch
import correlation
screenSize = [ ]
class correlator(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Correlator')
        self.setFixedSize(425,150)
        layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        label.setText("STATSCAN COMPUTER ASSISTED MATCHING PROGRAM")
        label.setFont(QFont("Arial",11))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        hbox1 =  QtWidgets.QHBoxLayout()
        self.exactWord = QtWidgets.QPushButton('Main Menu')
        self.exactWord.clicked.connect(lambda: self.toMain())
        hbox1.addWidget(self.exactWord)
        self.codesearch = QtWidgets.QPushButton('Code Search')
        self.codesearch.clicked.connect(lambda: self.toCodeSearch())
        hbox1.addWidget(self.codesearch)
        self.stringparser = QtWidgets.QPushButton('Exact Code')
        self.stringparser.clicked.connect(lambda: self.toExactWord())
        hbox1.addWidget(self.stringparser)
        self.correlator = QtWidgets.QPushButton('String Parser')
        self.correlator.clicked.connect(lambda: self.toStringParser())
        hbox1.addWidget(self.correlator)
        vbox.addLayout(hbox1)
        label2 = QtWidgets.QLabel(self)
        label2.setText("What code would you like to correlate?")
        vbox.addWidget(label2)
        toCorrelateTextbox = QtWidgets.QLineEdit(self)
        toCorrelateTextbox.resize(280,40)
        toCorrelateTextbox.textChanged.connect(lambda: self.enableSubmit(toCorrelateTextbox))
        vbox.addWidget(toCorrelateTextbox)
        self.submit = QtWidgets.QPushButton('Submit')
        self.submit.setDisabled(True)
        self.submit.clicked.connect(lambda: self.toResult(toCorrelateTextbox.text()))
        vbox.addWidget(self.submit)
        self.setLayout(vbox)

    def enableSubmit(self,label3):
        if (len(label3.text())>0):
            self.submit.setDisabled(False)

    def toMain(self):
        self.w = MainMenu()
        self.w.show()
        self.hide()
    
    def toStringParser(self):
        self.w = stringParser()
        self.w.show()
        self.hide()

    def toCodeSearch(self):
        self.w = codeSearch()
        self.w.show()
        self.hide()

    def toExactWord(self):
        self.w = exactWord()
        self.w.show()
        self.hide()

    def toResult(self, toCorrelate):
        dataSet = correlation.performCorrelation(toCorrelate)
        self.w = correlatorResult(dataSet,toCorrelate)
        self.w.show()
        self.hide()

class correlatorResult(QtWidgets.QWidget):
    def __init__(self,tableData,searched):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Correlator Result')
        
        layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        label.setText("STATSCAN COMPUTER ASSISTED MATCHING PROGRAM")
        label.setFont(QFont("Arial",11))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        hbox1 =  QtWidgets.QHBoxLayout()
        self.exactWord = QtWidgets.QPushButton('Main Menu')
        self.exactWord.clicked.connect(lambda: self.toMain())
        hbox1.addWidget(self.exactWord)
        self.codesearch = QtWidgets.QPushButton('Code Search')
        self.codesearch.clicked.connect(lambda: self.toCodeSearch())
        hbox1.addWidget(self.codesearch)
        self.stringparser = QtWidgets.QPushButton('Exact Code')
        self.stringparser.clicked.connect(lambda: self.toExactWord())
        hbox1.addWidget(self.stringparser)
        self.correlator = QtWidgets.QPushButton('String Parser')
        self.correlator.clicked.connect(lambda: self.toStringParser())
        hbox1.addWidget(self.correlator)
        vbox.addLayout(hbox1)
        label2 = QtWidgets.QLabel(self)
        label2.setText("Code Correlated: " + str(searched))
        label2.setFont(QFont("Arial",11))
        vbox.addWidget(label2) 
        resultTable = QtWidgets.QTableWidget()
        columns = list(tableData)
        resultTable.setRowCount(len(tableData))
        resultTable.setColumnCount(len(columns))
        for j in range(0,len(tableData)):
            count = 0
            for i in columns:
                item = QtWidgets.QTableWidgetItem(str(tableData[i].tolist()[j]))
                resultTable.setItem(j,count,item)
                count += 1
        resultTable.resizeColumnsToContents()
        resultTable.setWordWrap(True)
        resultTable.setHorizontalHeaderLabels(["Code","Class Title", "Class Definition"])
        resultTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        resultTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setFixedHeight(screenSize[1]-50)
        self.setFixedWidth(screenSize[0])
        vbox.addWidget(resultTable) 
        self.setLayout(vbox)

    def toMain(self):
        self.w = MainMenu()
        self.w.show()
        self.hide()
    
    def toStringParser(self):
        self.w = stringParser()
        self.w.show()
        self.hide()

    def toCodeSearch(self):
        self.w = codeSearch()
        self.w.show()
        self.hide()

    def toCorrelate(self):
        self.w = correlator()
        self.w.show()
        self.hide()

class exactWord(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Exact Word Search')
        self.setFixedSize(425,400)
        layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        label.setText("STATSCAN COMPUTER ASSISTED MATCHING PROGRAM")
        label.setFont(QFont("Arial",11))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        hbox1 =  QtWidgets.QHBoxLayout()
        self.exactWord = QtWidgets.QPushButton('Main Menu')
        self.exactWord.clicked.connect(lambda: self.toMain())
        hbox1.addWidget(self.exactWord)
        self.codesearch = QtWidgets.QPushButton('Code Search')
        self.codesearch.clicked.connect(lambda: self.toCodeSearch())
        hbox1.addWidget(self.codesearch)
        self.stringparser = QtWidgets.QPushButton('String Parser')
        self.stringparser.clicked.connect(lambda: self.toStringParser())
        hbox1.addWidget(self.stringparser)
        self.correlator = QtWidgets.QPushButton('Correlator')
        self.correlator.clicked.connect(lambda: self.toCorrelate())
        hbox1.addWidget(self.correlator)
        vbox.addLayout(hbox1)
        label2 = QtWidgets.QLabel(self)
        label2.setText("Which dataset would you like to search in?")
        vbox.addWidget(label2)
        bg1 = QtWidgets.QButtonGroup(self)
        rb1 = QtWidgets.QRadioButton("BLS", self)
        rb2 = QtWidgets.QRadioButton("NAPCS", self)
        hbox2 =  QtWidgets.QHBoxLayout()
        hbox2.addWidget(rb1)
        hbox2.addWidget(rb2)
        vbox.addLayout(hbox2)
        label3 = QtWidgets.QLabel(self)
        label3.setText("What exact word would you like to search for?")
        vbox.addWidget(label3)
        exactWordTextbox = QtWidgets.QLineEdit(self)
        exactWordTextbox.resize(280,40)
        exactWordTextbox.textChanged.connect(lambda: self.enableSubmit(exactWordTextbox, rb1.isChecked(), rb2.isChecked()))
        rb1.clicked.connect(lambda: self.enableSubmit(exactWordTextbox, rb1.isChecked(), rb2.isChecked()))
        rb2.clicked.connect(lambda: self.enableSubmit(exactWordTextbox, rb1.isChecked(), rb2.isChecked()))
        vbox.addWidget(exactWordTextbox)
        label4 = QtWidgets.QLabel(self)
        label4.setText("Optional Filtering for NAPCS only:")
        vbox.addWidget(label4)
        label5 = QtWidgets.QLabel(self)
        label5.setText("What length code would you like to look for? (Optional)")
        vbox.addWidget(label5)
        lengthCodeTextbox = QtWidgets.QLineEdit(self)
        lengthCodeTextbox.resize(280,40)
        vbox.addWidget(lengthCodeTextbox)
        label6 = QtWidgets.QLabel(self)
        label6.setText("What code first digit would you like to look for? (Optional)")
        vbox.addWidget(label6)
        firstDigitTextbox = QtWidgets.QLineEdit(self)
        firstDigitTextbox.resize(280,40)
        vbox.addWidget(firstDigitTextbox)
        self.submit = QtWidgets.QPushButton('Submit')
        self.submit.setDisabled(True)
        self.submit.clicked.connect(lambda: self.toResult(rb1, exactWordTextbox.text(),lengthCodeTextbox.text(),firstDigitTextbox.text()))
        vbox.addWidget(self.submit)
        self.setLayout(vbox)

    def enableSubmit(self,label3,isBLS,isNAPCS):
        if (len(label3.text())>0) and (isBLS == True or isNAPCS == True):
            self.submit.setDisabled(False)

    def toMain(self):
        self.w = MainMenu()
        self.w.show()
        self.hide()
    
    def toStringParser(self):
        self.w = stringParser()
        self.w.show()
        self.hide()

    def toCodeSearch(self):
        self.w = codeSearch()
        self.w.show()
        self.hide()

    def toCorrelate(self):
        self.w = correlator()
        self.w.show()
        self.hide()

    def toResult(self,isBLF, exactWordText,lenCode, firstDigit):
        if isBLF.isChecked() == True:
            dataSet = tempMatch.exactSearch("BLS",exactWordText,lenCode,firstDigit)
        else:
            dataSet = tempMatch.exactSearch("NAPCS",exactWordText,lenCode,firstDigit)
        self.w = exactWordResult(dataSet,exactWordText)
        self.w.show()
        self.hide()

class exactWordResult(QtWidgets.QWidget):
    def __init__(self,tableData,exactWord):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Exact Word Result')

        layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        label.setText("StatsCan Computer Assisted Matching Program ")
        label.setFont(QFont("Arial",11))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        hbox1 =  QtWidgets.QHBoxLayout()
        self.exactWord = QtWidgets.QPushButton('Main Menu')
        self.exactWord.clicked.connect(lambda: self.toMain())
        hbox1.addWidget(self.exactWord)
        self.codesearch = QtWidgets.QPushButton('Code Search')
        self.codesearch.clicked.connect(lambda: self.toCodeSearch())
        hbox1.addWidget(self.codesearch)
        self.stringparser = QtWidgets.QPushButton('String Parser')
        self.stringparser.clicked.connect(lambda: self.toStringParser())
        hbox1.addWidget(self.stringparser)
        self.correlator = QtWidgets.QPushButton('Correlator')
        self.correlator.clicked.connect(lambda: self.toCorrelate())
        hbox1.addWidget(self.correlator)
        vbox.addLayout(hbox1)
        label2 = QtWidgets.QLabel(self)
        label2.setText("Exact Word Searched: " + str(exactWord))
        label2.setFont(QFont("Arial",11))
        vbox.addWidget(label2)
        resultTable = QtWidgets.QTableWidget()
        columns = list(tableData)
        resultTable.setRowCount(len(tableData))
        resultTable.setColumnCount(len(columns))
        for j in range(0,len(tableData)):
            count = 0
            for i in columns:
                item = QtWidgets.QTableWidgetItem(str(tableData[i].tolist()[j]))
                resultTable.setItem(j,count,item)
                count += 1
        resultTable.resizeColumnsToContents()
        resultTable.setWordWrap(True)
        resultTable.setHorizontalHeaderLabels(["Code","Class Title", "Class Definition"])
        resultTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        resultTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setFixedHeight(screenSize[1]-50)
        self.setFixedWidth(screenSize[0])
        vbox.addWidget(resultTable) 
        self.setLayout(vbox)

    def toMain(self):
        self.w = MainMenu()
        self.w.show()
        self.hide()
    
    def toStringParser(self):
        self.w = stringParser()
        self.w.show()
        self.hide()

    def toCodeSearch(self):
        self.w = codeSearch()
        self.w.show()
        self.hide()

    def toCorrelate(self):
        self.w = correlator()
        self.w.show()
        self.hide()

#__________________________CODE SEARCH________________________
class codeSearch(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Code Search')
        self.setFixedSize(425,275)
        layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        label.setText("STATSCAN COMPUTER ASSISTED MATCHING PROGRAM")
        label.setFont(QFont("Arial",11))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        hbox1 =  QtWidgets.QHBoxLayout()
        self.exactWord = QtWidgets.QPushButton('Main Menu')
        self.exactWord.clicked.connect(lambda: self.toMain())
        hbox1.addWidget(self.exactWord)
        
        self.codesearch = QtWidgets.QPushButton('Exact Word')
        self.codesearch.clicked.connect(lambda: self.toExactWord())
        hbox1.addWidget(self.codesearch)

        self.stringparser = QtWidgets.QPushButton('String Parser')
        self.stringparser.clicked.connect(lambda: self.toStringParser())
        hbox1.addWidget(self.stringparser)
        self.correlator = QtWidgets.QPushButton('Correlator')
        self.correlator.clicked.connect(lambda: self.toCorrelate())
        hbox1.addWidget(self.correlator)

        vbox.addLayout(hbox1)
        label2 = QtWidgets.QLabel(self)
        label2.setText("Which dataset would you like to search in?")
        vbox.addWidget(label2)
        bg1 = QtWidgets.QButtonGroup(self)
        rb1 = QtWidgets.QRadioButton("BLS", self)
        rb2 = QtWidgets.QRadioButton("NAPCS", self)
        
        hbox2 =  QtWidgets.QHBoxLayout()
        hbox2.addWidget(rb1)
        hbox2.addWidget(rb2)
        vbox.addLayout(hbox2)
        label3 = QtWidgets.QLabel(self)
        label3.setText("What code would you like to compare?")
        vbox.addWidget(label3)
        codeTextbox = QtWidgets.QLineEdit(self)
        codeTextbox.resize(280,40)
        vbox.addWidget(codeTextbox)
        label4 = QtWidgets.QLabel(self)
        label4.setText("How many of the nearest matches would you like to see?")
        vbox.addWidget(label4)
        matchesTextbox = QtWidgets.QLineEdit(self)
        matchesTextbox.resize(280,40)
        
        codeTextbox.textChanged.connect(lambda: self.enableSubmit(codeTextbox, matchesTextbox, rb1.isChecked(), rb2.isChecked()))
        matchesTextbox.textChanged.connect(lambda: self.enableSubmit(codeTextbox,matchesTextbox, rb1.isChecked(), rb2.isChecked()))
        rb1.clicked.connect(lambda: self.enableSubmit(codeTextbox,matchesTextbox, rb1.isChecked(), rb2.isChecked()))
        rb2.clicked.connect(lambda: self.enableSubmit(codeTextbox,matchesTextbox, rb1.isChecked(), rb2.isChecked()))
        
        vbox.addWidget(matchesTextbox)
        
        self.submit = QtWidgets.QPushButton('Submit')
        self.submit.setDisabled(True)
        self.submit.clicked.connect(lambda: self.toResult(rb1, codeTextbox.text(),matchesTextbox.text()))
        vbox.addWidget(self.submit)
        self.setLayout(vbox)

    def enableSubmit(self,code,matches,isBLS,isNAPCS):
        if (len(code.text())>0) and (len(matches.text())>0) and (isBLS == True or isNAPCS == True):
            self.submit.setDisabled(False)

    def toMain(self):
        self.w = MainMenu()
        self.w.show()
        self.hide()
    
    def toStringParser(self):
        self.w = stringParser()
        self.w.show()
        self.hide()

    def toExactWord(self):
        self.w = exactWord()
        self.w.show()
        self.hide()

    def toCorrelate(self):
        self.w = correlator()
        self.w.show()
        self.hide()

    def toResult(self,isBLF, codeBeingSearched,numberMatches):
        if isBLF.isChecked() == True:
            dataSet = tempMatch.main("BLS",codeBeingSearched,numberMatches)
        else:
            dataSet = tempMatch.main("NAPCS",codeBeingSearched,numberMatches)
        self.w = codeSearchResult(dataSet, codeBeingSearched)
        self.w.show()
        self.hide()


class codeSearchResult(QtWidgets.QWidget):
    def __init__(self,tableData,searchedCode):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Code Search Result')
        
        layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        label.setText("StatsCan Computer Assisted Matching Program ")
        label.setFont(QFont("Arial",11))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        hbox1 =  QtWidgets.QHBoxLayout()
        self.exactWord = QtWidgets.QPushButton('Main Menu')
        self.exactWord.clicked.connect(lambda: self.toMain())
        hbox1.addWidget(self.exactWord)
        self.codesearch = QtWidgets.QPushButton('Exact Word')
        self.codesearch.clicked.connect(lambda: self.toExactWord())
        hbox1.addWidget(self.codesearch)
        self.stringparser = QtWidgets.QPushButton('String Parser')
        self.stringparser.clicked.connect(lambda: self.toStringParser())
        hbox1.addWidget(self.stringparser)
        self.correlator = QtWidgets.QPushButton('Correlator')
        self.correlator.clicked.connect(lambda: self.toCorrelate())
        hbox1.addWidget(self.correlator)
        vbox.addLayout(hbox1)
        label2 = QtWidgets.QLabel(self)
        label2.setText("Code Searched: " + str(searchedCode))
        label2.setFont(QFont("Arial",11))
        vbox.addWidget(label2)
        resultTable = QtWidgets.QTableWidget()
        columns = list(tableData)
        resultTable.setRowCount(len(tableData))
        resultTable.setColumnCount(len(columns))
        for j in range(0,len(tableData)):
            count = 0
            for i in columns:
                item = QtWidgets.QTableWidgetItem(str(tableData[i].tolist()[j]))
                resultTable.setItem(j,count,item)
                count += 1
        resultTable.resizeColumnsToContents()
        resultTable.setWordWrap(True)
        resultTable.setHorizontalHeaderLabels(["Code","Class Title", "Class Definition"])
        resultTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        resultTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setFixedHeight(screenSize[1]-50)
        self.setFixedWidth(screenSize[0])
        vbox.addWidget(resultTable) 
        self.setLayout(vbox)

    def toMain(self):
        self.w = MainMenu()
        self.w.show()
        self.hide()
    
    def toStringParser(self):
        self.w = stringParser()
        self.w.show()
        self.hide()

    def toExactWord(self):
        self.w = exactWord()
        self.w.show()
        self.hide()

    def toCorrelate(self):
        self.w = correlator()
        self.w.show()
        self.hide()

class stringParser(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('String Parser')
        self.setFixedSize(425,400)
        layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        label.setText("STATSCAN COMPUTER ASSISTED MATCHING PROGRAM")
        label.setFont(QFont("Arial",11))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        hbox1 =  QtWidgets.QHBoxLayout()
        self.exactWord = QtWidgets.QPushButton('Main Menu')
        self.exactWord.clicked.connect(lambda: self.toMain())
        hbox1.addWidget(self.exactWord)
        self.codesearch = QtWidgets.QPushButton('Exact Word')
        self.codesearch.clicked.connect(lambda: self.toExactWord())
        hbox1.addWidget(self.codesearch)
        self.stringparser = QtWidgets.QPushButton('Code Search')
        self.stringparser.clicked.connect(lambda: self.toCodeSearch())
        hbox1.addWidget(self.stringparser)
        self.correlator = QtWidgets.QPushButton('Correlator')
        self.correlator.clicked.connect(lambda: self.toCorrelate())
        hbox1.addWidget(self.correlator)
        vbox.addLayout(hbox1)
        label2 = QtWidgets.QLabel(self)
        label2.setText("Which dataset would you like to search in?")
        vbox.addWidget(label2)
        bg1 = QtWidgets.QButtonGroup(self)
        rb1 = QtWidgets.QRadioButton("BLS", self)
        rb2 = QtWidgets.QRadioButton("NAPCS", self)
        hbox2 =  QtWidgets.QHBoxLayout()
        hbox2.addWidget(rb1)
        hbox2.addWidget(rb2)
        vbox.addLayout(hbox2)
        label3 = QtWidgets.QLabel(self)
        label3.setText("What string would you like to parse?")
        vbox.addWidget(label3)
        exactWordTextbox = QtWidgets.QLineEdit(self)
        exactWordTextbox.resize(280,40)
        exactWordTextbox.textChanged.connect(lambda: self.enableSubmit(exactWordTextbox, rb1.isChecked(), rb2.isChecked()))
        rb1.clicked.connect(lambda: self.enableSubmit(exactWordTextbox, rb1.isChecked(), rb2.isChecked()))
        rb2.clicked.connect(lambda: self.enableSubmit(exactWordTextbox, rb1.isChecked(), rb2.isChecked()))
        vbox.addWidget(exactWordTextbox)
        label4 = QtWidgets.QLabel(self)
        label4.setText("Optional Filtering for NAPCS only:")
        vbox.addWidget(label4)
        label5 = QtWidgets.QLabel(self)
        label5.setText("What length code would you like to look for? (Optional)")
        vbox.addWidget(label5)
        lengthCodeTextbox = QtWidgets.QLineEdit(self)
        lengthCodeTextbox.resize(280,40)
        vbox.addWidget(lengthCodeTextbox)
        label6 = QtWidgets.QLabel(self)
        label6.setText("What code first digit would you like to look for? (Optional)")
        vbox.addWidget(label6)
        firstDigitTextbox = QtWidgets.QLineEdit(self)
        firstDigitTextbox.resize(280,40)
        vbox.addWidget(firstDigitTextbox)
        self.submit = QtWidgets.QPushButton('Submit')
        self.submit.setDisabled(True)
        self.submit.clicked.connect(lambda: self.toResult(rb1, exactWordTextbox.text(),lengthCodeTextbox.text(),firstDigitTextbox.text()))
        vbox.addWidget(self.submit)
        self.setLayout(vbox)

    def enableSubmit(self,label3,isBLS,isNAPCS):
        if (len(label3.text())>0) and (isBLS == True or isNAPCS == True):
            self.submit.setDisabled(False)

    def toMain(self):
        self.w = MainMenu()
        self.w.show()
        self.hide()
    
    def toCodeSearch(self):
        self.w = codeSearch()
        self.w.show()
        self.hide()

    def toExactWord(self):
        self.w = exactWord()
        self.w.show()
        self.hide()

    def toCorrelate(self):
        self.w = correlator()
        self.w.show()
        self.hide()

    def toResult(self,isBLF, entry,lencode,firstdig):
        if isBLF.isChecked() == True:
            dataSet = tempMatch.parseResult("BLS",entry,lencode,firstdig)
        else:
            dataSet = tempMatch.parseResult("NAPCS",entry,lencode,firstdig)
        self.w = stringParserResult(dataSet,entry)
        self.w.show()
        self.hide()
    
class stringParserResult(QtWidgets.QWidget):
    def __init__(self,tableData,entry):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('String Parser Result')
        
        layout = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel(self)
        label.setText("StatsCan Computer Assisted Matching Program ")
        label.setFont(QFont("Arial",11))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        hbox1 =  QtWidgets.QHBoxLayout()
        self.exactWord = QtWidgets.QPushButton('Main Menu')
        self.exactWord.clicked.connect(lambda: self.toMain())
        hbox1.addWidget(self.exactWord)
        self.codesearch = QtWidgets.QPushButton('Exact Word')
        self.codesearch.clicked.connect(lambda: self.toExactWord())
        hbox1.addWidget(self.codesearch)
        self.stringparser = QtWidgets.QPushButton('Code Search')
        self.stringparser.clicked.connect(lambda: self.toCodeSearch())
        hbox1.addWidget(self.stringparser)
  
        self.correlator = QtWidgets.QPushButton('Correlator')
        self.correlator.clicked.connect(lambda: self.toCorrelate())
        hbox1.addWidget(self.correlator)
        vbox.addLayout(hbox1)
        label2 = QtWidgets.QLabel(self)
        label2.setText("String Parsed: " + str(entry))
        label2.setFont(QFont("Arial",11))
        vbox.addWidget(label2)
        resultTable = QtWidgets.QTableWidget()
        columns = list(tableData)
        resultTable.setRowCount(len(tableData))
        resultTable.setColumnCount(len(columns))
        for j in range(0,len(tableData)):
            count = 0
            for i in columns:
                item = QtWidgets.QTableWidgetItem(str(tableData[i].tolist()[j]))
                resultTable.setItem(j,count,item)
                count += 1
        resultTable.resizeColumnsToContents()
        resultTable.setWordWrap(True)
        resultTable.setHorizontalHeaderLabels(["Code","Class Title", "Class Definition"])
        resultTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        resultTable.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.setFixedHeight(screenSize[1]-50)
        self.setFixedWidth(screenSize[0])
        vbox.addWidget(resultTable) 
        self.setLayout(vbox)

    def toMain(self):
        self.w = MainMenu()
        self.w.show()
        self.hide()
    
    def toStringParser(self):
        self.w = stringParser()
        self.w.show()
        self.hide()

    def toExactWord(self):
        self.w = exactWord()
        self.w.show()
        self.hide()

    def toCorrelate(self):
        self.w = correlator()
        self.w.show()
        self.hide()

class MainMenu(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('S.C.A.M.P Main Menu')
        self.setFixedSize(425,75)
        label = QtWidgets.QLabel(self)
        label.setText("STATSCAN COMPUTER ASSISTED MATCHING PROGRAM")
        label.setFont(QFont("Arial",11))
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        hbox1 =  QtWidgets.QHBoxLayout()
        self.exactWord = QtWidgets.QPushButton('Exact Word')
        self.exactWord.clicked.connect(lambda: self.toExactWord())
        hbox1.addWidget(self.exactWord)

        self.codesearch = QtWidgets.QPushButton('Code Search')
        self.codesearch.clicked.connect(lambda: self.toCodeSearch())
        hbox1.addWidget(self.codesearch)

        self.stringparser = QtWidgets.QPushButton('String Parser')
        self.stringparser.clicked.connect(lambda: self.toStringParser())
        hbox1.addWidget(self.stringparser)

        self.correlator = QtWidgets.QPushButton('Correlator')
        self.correlator.clicked.connect(lambda: self.toCorrelate())
        hbox1.addWidget(self.correlator)
        vbox.addLayout(hbox1)

        self.setLayout(vbox)

    def toStringParser(self):
        self.w = stringParser()
        self.w.show()
        self.hide()
    
    def toCodeSearch(self):
        self.w = codeSearch()
        self.w.show()
        self.hide()

    def toExactWord(self):
        self.w = exactWord()
        self.w.show()
        self.hide()
    
    def toCorrelate(self):
        self.w = correlator()
        self.w.show()
        self.hide()


class Controller:

    def __init__(self):
        pass

    def show_main_menu(self):
        self.main_menu = MainMenu()
        self.main_menu.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    screenSize.append(screen.size().width())
    screenSize.append(screen.size().height())
    controller = Controller()
    controller.show_main_menu()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()