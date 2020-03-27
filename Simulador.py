import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtCore
import matplotlib.pyplot as plt
from PyQt5.QtChart import QChart, QChartView, QBarSet, QHorizontalPercentBarSeries, QBarCategoryAxis, QValueAxis
import numpy as np 
import random 
import copy
import sqlite3
from sqlite3 import Error

class Ui(QtWidgets.QMainWindow):

	# metodo constructor de la clase ventana
	def __init__(self):
		super(Ui, self).__init__()
		uic.loadUi('simulador.ui', self)
		self.setWindowTitle("Simulador")

		# para cargar las colas desde la base de datos
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 858, 21))
		self.menubar.setObjectName("menubar")
		
		# ----------------------------------- CARGAR COLAS DE PROCESOS -----------------------------------

		self.menuFile = self.menubar.addMenu('&Colas')		

		self.actionCargarProcesos1 = QtWidgets.QAction(self)
		self.actionCargarProcesos1.setObjectName("actionCargarProcesos1")
		self.actionCargarProcesos1.setText("Cargar Cola 1")
		self.menuFile.addAction(self.actionCargarProcesos1)

		self.actionCargarProcesos2 = QtWidgets.QAction(self)
		self.actionCargarProcesos2.setObjectName("actionCargarProcesos2")
		self.actionCargarProcesos2.setText("Cargar Cola 2")
		self.menuFile.addAction(self.actionCargarProcesos2)

		self.actionCargarProcesos3 = QtWidgets.QAction(self)
		self.actionCargarProcesos3.setObjectName("actionCargarProcesos3")
		self.actionCargarProcesos3.setText("Cargar Cola 3")
		self.menuFile.addAction(self.actionCargarProcesos3)

		self.actionCargarProcesos1.triggered.connect(self.cargar_tabla_procesos1)
		self.actionCargarProcesos2.triggered.connect(self.cargar_tabla_procesos2)
		self.actionCargarProcesos3.triggered.connect(self.cargar_tabla_procesos3)

		# ----------------------------------- CARGAS DE TRABAJO -----------------------------------

		self.cargaTarabajoMenu = self.menubar.addMenu('&Carga de Trabajo')

		self.actionCargaTrabajo1 = QtWidgets.QAction(self)
		self.actionCargaTrabajo1.setObjectName("CargaTrabajo1")
		self.actionCargaTrabajo1.setText("Cargar de Trabajo 1")
		self.cargaTarabajoMenu.addAction(self.actionCargaTrabajo1)

		self.actionCargaTrabajo1.triggered.connect(self.cargaTrabajo1)

		# para el ejercicio de comprobacion:
		# Guia Administración de Memoria Contigua
		# Ejercicio 3 
		self.Ejercicio3 = QtWidgets.QAction(self)
		self.Ejercicio3.setObjectName("Ejercicio3")
		self.Ejercicio3.setText("Cargar Ejercicio 3")
		self.cargaTarabajoMenu.addAction(self.Ejercicio3)

		self.Ejercicio3.triggered.connect(self.ejercicio3)

		# ----------------------------------- PESTAÑA DE ENTRADA -----------------------------------

		# para que al abrir el programa, se muestre la pestaña de salida
		self.tabWidget.setCurrentIndex(0)

		# TAMAÑO DE MEMORIA
		self.TamMemSpinBox.setMaximum(4096) 
		self.TamMemSpinBox.setMinimum(32)		
		self.TamMemSpinBox.setValue(1024)

		# PORCION DE MEMORIA DEL SO

		self.TamSoLabel = QtWidgets.QLabel(self.EntradaIzqGroupBox)
		self.TamSoLabel.setObjectName("TamSoLabel")
		self.TamSoLabel.setGeometry(QtCore.QRect(20, 70, 241, 20))
		self.TamSoLabel.setText('% para el SO')

		self.TamSoSpinBox = QtWidgets.QSpinBox(self.EntradaIzqGroupBox)
		self.TamSoSpinBox.setMinimum(10)
		self.TamSoSpinBox.setMaximum(30)
		self.TamSoSpinBox.setObjectName("TamSoSpinBox")
		self.TamSoSpinBox.setGeometry(QtCore.QRect(139, 70, 112, 20))

		# la parte superior de la seccion "Memoria"
		self.EntradaArribaLine.setGeometry(QtCore.QRect(10, 105, 241, 20))

		# PARTICIONES FIJAS O VARIABLES
		self.VariablesRadioButton.setChecked(True)
		self.BestRadioButton.setEnabled(False) # porque por defecto esta el particionado variable
		self.PartFijaGroupBox.setVisible(False)

		self.PartLabel.setGeometry(QtCore.QRect(30, 125, 71, 16))
		self.VariablesRadioButton.setGeometry(QtCore.QRect(60, 150, 82, 17))
		self.FijasRadioButton.setGeometry(QtCore.QRect(160, 150, 51, 17))

		# PARTICIONES FIJAS
		self.AgregarPartPushButton.clicked.connect(self.agregar_particion)
		self.NroEspacioDispLabel.setText('0')

		self.TamPartSpinBox.setMaximum(99999)
		self.TamPartSpinBox.setMinimum(1)

		# para que se vea mejor
		self.ParticionesTableWidget.verticalHeader().setVisible(False)
		header = self.ParticionesTableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

		self.EliminarPartPushButton.clicked.connect(self.eliminar_particion)

		self.PartFijaGroupBox.setGeometry(QtCore.QRect(-1, 170, 281, 271))

		self.EspacioOcupProgressBar.setProperty("value", 0)

		self.EntradaAbajoLine.setGeometry(QtCore.QRect(49, 470, 241, 20))

		# METODO DE ASIGNACION
		self.FirstRadioButton.setChecked(True)
		self.QuantumLabel.setVisible(False)
		self.QuantumSpinBox.setVisible(False)
		self.QuantumSpinBox.setMinimum(1)
		self.QuantumSpinBox.setMaximum(5)
		self.QuantumSpinBox.setValue(1)

		self.MetAsigGroupBox.setGeometry(QtCore.QRect(20, 475, 240, 100))

		# ALGORITMOS DE PLANIFICACION
		self.AlgoritmoGroupBox.setGeometry(QtCore.QRect(20, 590, 240, 120))
		
		# algoritmo SJF agregado 
		self.AlgortimoComboBox.addItem("")

		self.AlgortimoComboBox.setItemText(0, "First Come First Service (FCFS)")
		self.AlgortimoComboBox.setItemText(1, "Prioridades")
		self.AlgortimoComboBox.setItemText(2, "Multilevel Queue (MLQ)")
		self.AlgortimoComboBox.setItemText(3, "Round Robin with Quantum (RRQ)")
		self.AlgortimoComboBox.setItemText(4, "Short Job First (SJF)")

		# LISTA DE PROCESOS CARGADOS
		self.ListProcCargTableWidget.setColumnCount(5)
		aux = ['Proceso','Tamaño', 'Arribo', 'Prioridad','Rafagas']
		self.ListProcCargTableWidget.setHorizontalHeaderLabels(aux)
		self.ListProcCargTableWidget.verticalHeader().setVisible(False)

		# para que se vea mejor 
		header = self.ListProcCargTableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

		self.BorrarTablaPushButton.clicked.connect(self.borrar_lista_procesos)
		self.BorrarSeleccionPushButton.clicked.connect(self.borrar_un_proceso)

		# NUEVO PROCESO
		self.NuevoProcGroupBox.setGeometry(QtCore.QRect(20, 25, 440, 340))
		self.ListaProcCargLabel.setGeometry(QtCore.QRect(30, 375, 131, 16))
		self.ListProcCargTableWidget.setGeometry(QtCore.QRect(20, 400, 440, 251))

		self.TALabel.setGeometry(QtCore.QRect(322, 30, 60, 20))
		self.TALabel.setText('Arribo')
		self.TamProcLabel.setGeometry(QtCore.QRect(160, 30, 81, 20))

		self.TamProcSpinBox.setGeometry(QtCore.QRect(229, 30, 50, 22))
		self.TASpinBox.setGeometry(QtCore.QRect(360, 30, 60, 22))

		self.ProcActualTableWidget.horizontalHeader().setVisible(False)
		self.ProcActualTableWidget.verticalHeader().setVisible(False)

		# pero solo podemos cargar 10 procesos como maximo
		self.IdProcSpinBox.setMaximum(100)
		self.IdProcSpinBox.setMinimum(1) 
		self.IdProcSpinBox.setValue(1) 

		self.TASpinBox.setMaximum(100)
		self.TASpinBox.setMinimum(0)
		self.TASpinBox.setValue(0)

		# se pone el siguiente tamaño maximo, pero de todas formas, al momento de cargar
		# se hace el control del tamaño
		self.TamProcSpinBox.setMaximum(self.TamMemSpinBox.value() * 0.9)

		self.TamProcSpinBox.setMinimum(1)
		self.TamProcSpinBox.setValue(1)

		filas = self.ProcActualTableWidget.verticalHeader()
		filas.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		filas.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

		self.AgregarProcPushButton.clicked.connect(self.agregar_proceso)
		self.AgregarPushButton.clicked.connect(self.agregar_rafaga)

		self.AgregarProcPushButton.setGeometry(QtCore.QRect(320, 295, 100, 30))
		
		self.PrioridadLabel = QtWidgets.QLabel(self.NuevoProcGroupBox)
		self.PrioridadLabel.setGeometry(QtCore.QRect(20, 250, 90, 17))
		self.PrioridadLabel.setObjectName("PrioridadLabel")
		self.PrioridadLabel.setText("Prioridad")

		self.ColaRandomButton = QtWidgets.QRadioButton(self.NuevoProcGroupBox)
		self.ColaRandomButton.setGeometry(QtCore.QRect(210, 250, 80, 17))
		self.ColaRandomButton.setObjectName("ColaRandomButton")
		self.ColaRandomButton.setText("Aleatoria")

		self.ColaElegidaButton = QtWidgets.QRadioButton(self.NuevoProcGroupBox)
		self.ColaElegidaButton.setGeometry(QtCore.QRect(100, 250, 100, 17))
		self.ColaElegidaButton.setObjectName("ColaElegidaButton")
		self.ColaElegidaButton.setText("Elegir")

		self.ColaRandomButton.setChecked(True)

		self.PrioridadComboBox = QtWidgets.QComboBox(self.NuevoProcGroupBox)
		self.PrioridadComboBox.setGeometry(QtCore.QRect(100, 280, 100, 22))
		self.PrioridadComboBox.setObjectName("PrioridadComboBox")
		self.PrioridadComboBox.addItem("")
		self.PrioridadComboBox.addItem("")
		self.PrioridadComboBox.addItem("")
		self.PrioridadComboBox.setItemText(0, "Baja")
		self.PrioridadComboBox.setItemText(1, "Media")
		self.PrioridadComboBox.setItemText(2, "Alta")

		self.PrioridadComboBox.setVisible(False)

		self.ColaRandomButton.clicked.connect(self.clickEvent)
		self.ColaElegidaButton.clicked.connect(self.clickEvent)

		self.INICIARPushButton.clicked.connect(self.planificar)

		# ----------------------------------- PESTAÑA DE SALIDA -----------------------------------

		self.DiagramaGanttPushButton.clicked.connect(self.graficar_gantt)

		self.ColaCPULabel.setText('Cola de Listos')
		self.ColaCPULabel.setGeometry(QtCore.QRect(45, 185, 70, 13))
		self.ColaSuspLabel.setText('Cola disp. Entrada')
		self.ColaSuspLabel.setGeometry(QtCore.QRect(20, 247, 111, 31))
		self.CargEnMemLabel.setText('Cola disp. Salida')
		self.CargEnMemLabel.setGeometry(QtCore.QRect(38, 315, 111, 31))

		self.enCpuLabel = QtWidgets.QLabel(self.ProcesamPorTiempoGroupBox)
		self.enCpuLabel.setObjectName("enCpu")
		self.enCpuLabel.setGeometry(QtCore.QRect(38, 384, 111, 31))
		self.enCpuLabel.setText("Proceso en CPU")

		self.idEnCpuLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
		self.idEnCpuLabel.setObjectName("idEnCpuLabel")
		self.IDsProcsVerticalLayout.addWidget(self.idEnCpuLabel)
		self.idEnCpuLabel.setText("0")

		self.PartOcupTextEdit.setReadOnly(True)
		self.HistPlanifTextEdit.setReadOnly(True)

		self.PartOcupTextEdit.setGeometry(QtCore.QRect(140, 500, 131, 81))
		self.ProcesamPorTiempoGroupBox.setGeometry(QtCore.QRect(70, 50, 291, 670))
		self.GraficarDiagMemPushButton = QtWidgets.QPushButton(self.ProcesamPorTiempoGroupBox)
		self.GraficarDiagMemPushButton.setGeometry(QtCore.QRect(147, 600, 120, 40))
		self.GraficarDiagMemPushButton.setObjectName("GraficarDiagMemPushButton")
		self.GraficarDiagMemPushButton.setText('Diagrama de Memoria')
		self.SalidaVerticalLine.setGeometry(QtCore.QRect(120, 20, 20, 625))

		self.SegundoSpinBox.setEnabled(False) 

		self.GraficarDiagMemPushButton.clicked.connect(self.mostrarMapaMemoria)

		# procesamiento por tiempo
		self.SegundoSpinBox.valueChanged.connect(self.resultadosPorTiempo)

		self.FijasRadioButton.clicked.connect(self.clickEvent)
		self.VariablesRadioButton.clicked.connect(self.clickEvent)
		self.AlgortimoComboBox.currentTextChanged.connect(self.clickEvent)

		self.HistDePlanifGroupBox.setGeometry(QtCore.QRect(430, 50, 341, 590))

		self.HistPlanifTextEdit.setGeometry(QtCore.QRect(30, 40, 281, 430))

		self.DiagramaGanttPushButton.setGeometry(QtCore.QRect(30, 495, 111, 41))
		self.GuardarColaPushButton.setGeometry(QtCore.QRect(200, 495, 111, 41))

		# antes de comenzar la ejecucion debe estar inhabilitado
		self.GuardarColaPushButton.setEnabled(False)
		self.DiagramaGanttPushButton.setEnabled(False)
		self.GraficarDiagMemPushButton.setEnabled(False)

		# seccion de seleccion de la cola 
		self.ColaSeleccionadaLabel = QtWidgets.QLabel(self.HistDePlanifGroupBox)
		self.ColaSeleccionadaLabel.setGeometry(QtCore.QRect(206, 538, 100, 20)) 
		self.ColaSeleccionadaLabel.setObjectName("ColaSeleccionadaLabel")
		self.ColaSeleccionadaLabel.setText("Guardar en cola nro")

		self.ColaSelecSpinBox = QtWidgets.QSpinBox(self.HistDePlanifGroupBox)
		self.ColaSelecSpinBox.setGeometry(QtCore.QRect(235, 560, 42, 20)) 
		self.ColaSelecSpinBox.setObjectName("ColaSelec")
		self.ColaSelecSpinBox.setMinimum(1)
		self.ColaSelecSpinBox.setMaximum(3)
		self.ColaSelecSpinBox.setValue(1)

		self.GuardarColaPushButton.clicked.connect(self.guardarColaProcesos)

		# PROMEDIOS
		self.PromediosGroupBox = QtWidgets.QGroupBox(self.SalidaTab)     
		self.PromediosGroupBox.setGeometry(QtCore.QRect(430, 654, 343, 70))
		self.PromediosGroupBox.setObjectName("PromediosGroupBox")
		self.PromediosGroupBox.setTitle("Promedios")

		self.TiempoEsperaLabel = QtWidgets.QLabel(self.PromediosGroupBox)
		self.TiempoEsperaLabel.setGeometry(QtCore.QRect(50, 15, 100, 20)) 
		self.TiempoEsperaLabel.setObjectName("TiempoEsperaLabel")
		self.TiempoEsperaLabel.setText("Tiempo de Espera: ")

		self.TiempoRetornoLabel = QtWidgets.QLabel(self.PromediosGroupBox)
		self.TiempoRetornoLabel.setGeometry(QtCore.QRect(50, 37, 100, 20)) 
		self.TiempoRetornoLabel.setObjectName("TiempoRetornoLabel")
		self.TiempoRetornoLabel.setText("Tiempo de Retorno: ")

		self.ValorEsperaLabel = QtWidgets.QLabel(self.PromediosGroupBox)
		self.ValorEsperaLabel.setGeometry(QtCore.QRect(220, 15, 100, 20)) 
		self.ValorEsperaLabel.setObjectName("ValorEsperaLabel")
		self.ValorEsperaLabel.setText("000.000")

		self.ValorRetornoLabel = QtWidgets.QLabel(self.PromediosGroupBox)
		self.ValorRetornoLabel.setGeometry(QtCore.QRect(220, 37, 100, 20))
		self.ValorRetornoLabel.setObjectName("ValorRetornoLabel")
		self.ValorRetornoLabel.setText("000.000")

	# PROCESOS DE LA CLASE VENTANA / UI

	def clickEvent(self):
		# selecciono la opcion de RRQ
		if self.AlgortimoComboBox.currentIndex() == 3:
			self.QuantumLabel.setVisible(True)
			self.QuantumSpinBox.setVisible(True)
		else:
			self.QuantumLabel.setVisible(False)
			self.QuantumSpinBox.setVisible(False)
		# selecciono la opcion de colas multinivel
		if self.AlgortimoComboBox.currentIndex() == 2:
			self.QuantumLabel.setVisible(True)
			self.QuantumSpinBox.setVisible(True)
		# seleccion parciones fijas
		if self.FijasRadioButton.isChecked():
			self.PartFijaGroupBox.setVisible(True)
			# para este particionado, solamente se tienen diponibles FF Y BF, no WF
			self.WorstRadioButton.setEnabled(False)
			self.BestRadioButton.setEnabled(True)
		else:
			self.PartFijaGroupBox.setVisible(False)
			# para este particionado, solamente se tienen disponibles FF Y WF, no BF
			self.WorstRadioButton.setEnabled(True)
			self.BestRadioButton.setEnabled(False)

		# prioridad / cola de los procesos 
		if self.ColaElegidaButton.isChecked():
			self.PrioridadComboBox.setVisible(True)
			self.ColaRandomButton.setChecked(False)
		else:
			self.PrioridadComboBox.setVisible(False)


	def cargar_tabla_procesos1(self):
		self.cargar_cola(1)
	def cargar_tabla_procesos2(self):
		self.cargar_cola(2)
	def cargar_tabla_procesos3(self):
		self.cargar_cola(3)

	# ------------------------------------- METODOS PARA LA BASE DE DATOS -------------------------------------

	def	cargar_cola(self, cola):
		# conexion a la base de datos
		if self.ListProcCargTableWidget.rowCount() == 0:
			con = sqlite3.connect('simulador_db.db')

			# si no existe la tabla, la crea
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE if not exists procesos(id_conjunto integer , idp integer, tamaño integer, arribo integer, prioridad text, rafagas text, PRIMARY KEY(id_conjunto, idp))")
			con.commit()

			cursorObj.execute('SELECT * FROM procesos')
			if len(cursorObj.fetchall()) == 0:
				# la primera que vez que se ejecuta el simulador en una pc, si se quieren cargar colas, se generar 3 aleatorias
				# a partir de aqui se pueden usar las mismas, o guardar otras 

				# CARGAR TABLA
				# ciclo que controla las colas
				for j in range(1,4):
					# la lista nuevos_procesos es la que vamos a usar para insertar varios procesos juntos
					# a la base de datos
					# lo hacemos de esta manera porque usando una lista, se hace solo un INSERT, lo cual es mas simple
					nuevos_procesos = []
					# ciclo que controla los procesos
					for i in range(1,6):
						tam = random.randint(1,30)
						arribo = random.randint(0,11)
						p = ['A', 'M', 'B']
						prioridad = random.choice(p)
						rafagas = 'CPU: ' + str(random.randint(1,10)) + ';'

						if i % 2 == 0:
							rafagas = rafagas + ' S: ' + str(random.randint(1,10)) + ';'
						else:
							rafagas = rafagas + ' E: ' + str(random.randint(1,10)) + ';'

						rafagas = rafagas + ' CPU: ' + str(random.randint(1,10)) + ';'

						# primer campo es el id_conjunto
						reg = (j, i, tam, arribo, prioridad, rafagas)
						nuevos_procesos.append(reg)

					con = sqlite3.connect('simulador_db.db')
					cursorObj = con.cursor()
					cursorObj.executemany("INSERT INTO procesos VALUES(?, ?, ?, ?, ?, ?)", nuevos_procesos)
					con.commit()

			# consulta
			cursorObj = con.cursor()
			if cola == 1:
				cursorObj.execute('SELECT * FROM procesos WHERE id_conjunto = 1')
			if cola == 2:
				cursorObj.execute('SELECT * FROM procesos WHERE id_conjunto = 2')
			if cola == 3:
				cursorObj.execute('SELECT * FROM procesos WHERE id_conjunto = 3')

			rows = cursorObj.fetchall()
			for row in rows:
				fila = str(row)
				fila = fila.replace('(', '')
				fila = fila.replace(')', '')
				fila = fila.replace("'", '')

				fila = fila.split(',')

				self.ListProcCargTableWidget.setRowCount(self.ListProcCargTableWidget.rowCount()+1)

				proc=QtWidgets.QTableWidgetItem(str(fila[1]))
				proc.setTextAlignment(Qt.AlignCenter) 
				tam=QtWidgets.QTableWidgetItem(str(fila[2]))
				tam.setTextAlignment(Qt.AlignCenter)
				ta=QtWidgets.QTableWidgetItem(str(fila[3]))
				ta.setTextAlignment(Qt.AlignCenter)
				pri=QtWidgets.QTableWidgetItem(str(fila[4]))
				pri.setTextAlignment(Qt.AlignCenter)

				raf=QtWidgets.QTableWidgetItem(fila[5]+'')

				self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1,0,proc)
				self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1,1,tam)
				self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1,2,ta)
				self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1,3,pri)
				self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1,4,raf)

			self.IdProcSpinBox.setValue(self.ListProcCargTableWidget.rowCount()+1)

	def guardarColaProcesos(self):

		nf = self.ListProcCargTableWidget.rowCount()
		nuevos_procesos = []
		
		for i in range(nf):

			con = sqlite3.connect('simulador_db.db')
			cursorObj = con.cursor()
			proc = list()

			id_conj = int(self.ColaSelecSpinBox.value())
			idp = int(self.ListProcCargTableWidget.item(i,0).text())
			tam  = int(self.ListProcCargTableWidget.item(i,1).text())
			ta = int(self.ListProcCargTableWidget.item(i,2).text())
			pri = str(self.ListProcCargTableWidget.item(i,3).text())
			rafs = str(self.ListProcCargTableWidget.item(i,4).text())

			proc = (id_conj, idp, tam, ta, pri, rafs)
			nuevos_procesos.append(proc)

		if id_conj == 1:
			cursorObj.execute('DELETE FROM procesos WHERE id_conjunto = 1')
		if id_conj == 2:
			cursorObj.execute('DELETE FROM procesos WHERE id_conjunto = 2')
		if id_conj == 3:
			cursorObj.execute('DELETE FROM procesos WHERE id_conjunto = 3')

		cursorObj.executemany("INSERT INTO procesos VALUES(?, ?, ?, ?, ?, ?)", nuevos_procesos)
		con.commit()

	# ----------------------------------- PROCESOS DE CARGA DE TRABAJO -----------------------------------

	def cargaTrabajo1(self):

		if self.ParticionesTableWidget.rowCount() == 0: # para no cargar varias veces
			self.FijasRadioButton.setChecked(True)
			self.clickEvent()

			self.ParticionesTableWidget.setRowCount(self.ParticionesTableWidget.rowCount()+1)
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,0,QTableWidgetItem(str(1)))
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,1,QTableWidgetItem(str(400)))
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,1).setTextAlignment(Qt.AlignCenter)

			self.ParticionesTableWidget.setRowCount(self.ParticionesTableWidget.rowCount()+1)
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,0,QTableWidgetItem(str(2)))
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,1,QTableWidgetItem(str(200)))
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,1).setTextAlignment(Qt.AlignCenter)

			self.ParticionesTableWidget.setRowCount(self.ParticionesTableWidget.rowCount()+1)
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,0,QTableWidgetItem(str(3)))
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,1,QTableWidgetItem(str(200)))
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,1).setTextAlignment(Qt.AlignCenter)

			self.ParticionesTableWidget.setRowCount(self.ParticionesTableWidget.rowCount()+1)
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,0,QTableWidgetItem(str(4)))
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,1,QTableWidgetItem(str(122)))
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,1).setTextAlignment(Qt.AlignCenter)

			self.EspacioOcupProgressBar.setProperty("value",100)

			# metodo de asignacion 
			self.BestRadioButton.setChecked(True)

			# algoritmo 
			self.AlgortimoComboBox.setCurrentIndex(3) 
			self.QuantumSpinBox.setValue(5)

	# Ejercicio de verificacion
	def ejercicio3(self):
		if self.ListProcCargTableWidget.rowCount() == 0:
			self.FijasRadioButton.setChecked(True)
			self.clickEvent()
			self.TamMemSpinBox.setValue(137)
			self.TamSoSpinBox.setValue(23)

			# PARTICIONES
			self.ParticionesTableWidget.setRowCount(self.ParticionesTableWidget.rowCount()+1)
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,0,QTableWidgetItem(str(1)))
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,1,QTableWidgetItem(str(10)))
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,1).setTextAlignment(Qt.AlignCenter)

			self.ParticionesTableWidget.setRowCount(self.ParticionesTableWidget.rowCount()+1)
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,0,QTableWidgetItem(str(2)))
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,1,QTableWidgetItem(str(25)))
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,1).setTextAlignment(Qt.AlignCenter)

			self.ParticionesTableWidget.setRowCount(self.ParticionesTableWidget.rowCount()+1)
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,0,QTableWidgetItem(str(3)))
			self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,1,QTableWidgetItem(str(70)))
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
			self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,1).setTextAlignment(Qt.AlignCenter)

			self.EspacioOcupProgressBar.setProperty("value",100)

			# metodo de asignacion 
			self.BestRadioButton.setChecked(True)

			# algoritmo 
			self.AlgortimoComboBox.setCurrentIndex(3) 
			self.QuantumSpinBox.setValue(5)

			# PROCESOS
			# proceso 1
			id_proc = QTableWidgetItem('1')
			id_proc.setTextAlignment(Qt.AlignCenter)
			arribo = QTableWidgetItem('0')
			arribo.setTextAlignment(Qt.AlignCenter)
			tam = QTableWidgetItem('20')
			tam.setTextAlignment(Qt.AlignCenter)
			prioridad_item = QTableWidgetItem('M')
			prioridad_item.setTextAlignment(Qt.AlignCenter)
			raf_item = QTableWidgetItem('CPU: 5;')
			self.ListProcCargTableWidget.setRowCount(self.ListProcCargTableWidget.rowCount()+1)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 0, id_proc)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 1, tam)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 2, arribo)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 3, prioridad_item)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 4, raf_item)

			# proceso 2
			id_proc = QTableWidgetItem('2')
			id_proc.setTextAlignment(Qt.AlignCenter)
			arribo = QTableWidgetItem('0')
			arribo.setTextAlignment(Qt.AlignCenter)
			tam = QTableWidgetItem('5')
			tam.setTextAlignment(Qt.AlignCenter)
			prioridad_item = QTableWidgetItem('M')
			prioridad_item.setTextAlignment(Qt.AlignCenter)
			raf_item = QTableWidgetItem('CPU: 4;')
			self.ListProcCargTableWidget.setRowCount(self.ListProcCargTableWidget.rowCount()+1)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 0, id_proc)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 1, tam)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 2, arribo)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 3, prioridad_item)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 4, raf_item)

			# proceso 3
			id_proc = QTableWidgetItem('3')
			id_proc.setTextAlignment(Qt.AlignCenter)
			arribo = QTableWidgetItem('0')
			arribo.setTextAlignment(Qt.AlignCenter)
			tam = QTableWidgetItem('14')
			tam.setTextAlignment(Qt.AlignCenter)
			prioridad_item = QTableWidgetItem('M')
			prioridad_item.setTextAlignment(Qt.AlignCenter)
			raf_item = QTableWidgetItem('CPU: 10;')
			self.ListProcCargTableWidget.setRowCount(self.ListProcCargTableWidget.rowCount()+1)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 0, id_proc)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 1, tam)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 2, arribo)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 3, prioridad_item)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 4, raf_item)

			# proceso 4
			id_proc = QTableWidgetItem('4')
			id_proc.setTextAlignment(Qt.AlignCenter)
			arribo = QTableWidgetItem('0')
			arribo.setTextAlignment(Qt.AlignCenter)
			tam = QTableWidgetItem('25')
			tam.setTextAlignment(Qt.AlignCenter)
			prioridad_item = QTableWidgetItem('M')
			prioridad_item.setTextAlignment(Qt.AlignCenter)
			raf_item = QTableWidgetItem('CPU: 3;')
			self.ListProcCargTableWidget.setRowCount(self.ListProcCargTableWidget.rowCount()+1)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 0, id_proc)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 1, tam)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 2, arribo)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 3, prioridad_item)
			self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 4, raf_item)


	# ----------------------------------- DEMAS PROCESOS DE CLASE VENTANA -----------------------------------

	# Borrar Tabla
	def borrar_lista_procesos(self):
		i=0
		while self.ListProcCargTableWidget.rowCount()>0:
			self.ListProcCargTableWidget.removeRow(i)
		# para que sea mas comodo
		self.IdProcSpinBox.setValue(self.ListProcCargTableWidget.rowCount()+1)

		# si borramos todos los procesos, podemos editar algunas configuraciones
		if self.ListProcCargTableWidget.rowCount() == 0:
			self.EntradaIzqGroupBox.setEnabled(True)

	# Borrar Seleccion
	def borrar_un_proceso(self):
		borrar = []
		nf = self.ListProcCargTableWidget.rowCount()
		for i in range(nf):
			if self.ListProcCargTableWidget.item(i,0).isSelected():
				borrar.append(i)
		for i in borrar:
			self.ListProcCargTableWidget.removeRow(i)
		# actualiza el valor del id a 1, solo aporta mas comodidad
		if self.ListProcCargTableWidget.rowCount() == 0:
			self.IdProcSpinBox.setValue(1)
		else:
			self.actualizar_procesos()

		# si borramos todos los procesos, podemos editar algunas configuraciones
		# cuyas modificaciones estaban deshabilitadas
		if self.ListProcCargTableWidget.rowCount() == 0:
			self.EntradaIzqGroupBox.setEnabled(True)

	# actualiza los id's
	def actualizar_procesos(self):
		nf = int(self.ListProcCargTableWidget.rowCount())
		for i in range(nf):
			self.ListProcCargTableWidget.item(i,0).setText(str(i+1))

	def agregar_particion(self):
		mem_dip = self.TamMemSpinBox.value() - int(self.TamMemSpinBox.value() * self.TamSoSpinBox.value()/100)

		if self.ParticionesTableWidget.rowCount() == 0:
			# control de que la unica particion que voy a cargar no supere el tam de la memoria diponible 
			if self.TamPartSpinBox.value() <= mem_dip:
				# Nueva particion
				self.ParticionesTableWidget.setRowCount(self.ParticionesTableWidget.rowCount()+1)
				self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,0,QTableWidgetItem(str(self.ParticionesTableWidget.rowCount()+1)))
				tam_part = self.TamPartSpinBox.value()
				self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,1,QTableWidgetItem(str(tam_part)))
				self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
				self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,1).setTextAlignment(Qt.AlignCenter)
				self.TamPartSpinBox.setStyleSheet("background-color: rgb(255,255,255);")#blanco

				# actualizo etiqueta de espacio disponible
				self.NroEspacioDispLabel.setText(str(mem_dip - tam_part))

				ocupado = tam_part + int(self.TamSoSpinBox.value() * self.TamMemSpinBox.value() / 100)
				self.EspacioOcupProgressBar.setProperty("value", ocupado * 100 / self.TamMemSpinBox.value() )

				self.TamMemSpinBox.setReadOnly(True)
				self.TamSoSpinBox.setReadOnly(True)

			else:
				# tam particion supera al tam de la memoria 
				self.TamPartSpinBox.setStyleSheet("background-color: rgb(255,0,0);")
		else:
			ocup = 0 
			for i in range(self.ParticionesTableWidget.rowCount()):
				ocup = ocup + int(self.ParticionesTableWidget.item(i,1).text())

			if  self.TamPartSpinBox.value() <= (mem_dip - ocup):
				# Nueva particion
				self.ParticionesTableWidget.setRowCount(self.ParticionesTableWidget.rowCount()+1)
				self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,0,QTableWidgetItem(str(self.ParticionesTableWidget.rowCount()+1)))
				tam_part = self.TamPartSpinBox.value()
				self.ParticionesTableWidget.setItem(self.ParticionesTableWidget.rowCount()-1,1,QTableWidgetItem(str(tam_part)))
				self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
				self.ParticionesTableWidget.item(self.ParticionesTableWidget.rowCount()-1,1).setTextAlignment(Qt.AlignCenter)
				self.TamPartSpinBox.setStyleSheet("background-color: rgb(255,255,255);")#blanco

				# actualizo etiqueta de espacio disponible
				self.NroEspacioDispLabel.setText(str(mem_dip - ocup - tam_part))

				ocupado = ocup + tam_part + int(self.TamSoSpinBox.value() * self.TamMemSpinBox.value() / 100)
				self.EspacioOcupProgressBar.setProperty("value", ocupado * 100 / self.TamMemSpinBox.value() )

				self.TamMemSpinBox.setReadOnly(True)
				self.TamSoSpinBox.setReadOnly(True)

			else:
				self.TamPartSpinBox.setStyleSheet("background-color: rgb(255,0,0);")#rojo

		for i in range(self.ParticionesTableWidget.rowCount()):
				self.ParticionesTableWidget.item(i,0).setText(str(i+1))

	def eliminar_particion(self):
		borrar = []
		nf = self.ParticionesTableWidget.rowCount()
		for i in range(nf):
			if self.ParticionesTableWidget.item(i,0).isSelected() or self.ParticionesTableWidget.item(i,1).isSelected():
				borrar.append(i)
		for i in borrar:
			self.ParticionesTableWidget.removeRow(i)

		self.actualizar_particion()

		# si se eliminan todas las particiones recien se puede cambiar el tamaño de la memoria, pero solo con las flechas del spinbox
		if self.ParticionesTableWidget.rowCount() == 0:
			self.TamMemSpinBox.setReadOnly(False)
			self.TamSoSpinBox.setReadOnly(False)

	def actualizar_particion(self):
		# espacio ocupado
		ocupado = 0 
		for i in range(self.ParticionesTableWidget.rowCount()):
			self.ParticionesTableWidget.item(i,0).setText(str(i+1))
			if self.ParticionesTableWidget.item(i,1).text() != '':
				# ocupado en particiones
				ocupado = ocupado + int(self.ParticionesTableWidget.item(i,1).text())

		mem_dip = self.TamMemSpinBox.value() - int(self.TamSoSpinBox.value() * self.TamMemSpinBox.value() / 100)
		self.NroEspacioDispLabel.setText(str(mem_dip - ocupado))

		ocupado = ocupado + int(self.TamSoSpinBox.value() * self.TamMemSpinBox.value() / 100)
		self.EspacioOcupProgressBar.setProperty("value", ocupado * 100 / self.TamMemSpinBox.value())

	def agregar_rafaga(self):
		if self.ProcActualTableWidget.columnCount() < 5:
			# control por si no selecciona ninguna
			if self.EntradaRadioButton.isChecked() or self.SalidaRadioButton.isChecked():
				# agrega columna
				self.ProcActualTableWidget.setColumnCount(self.ProcActualTableWidget.columnCount()+1)
				# pregunta por entrada o salida 
				if (self.EntradaRadioButton.isChecked()):
					self.ProcActualTableWidget.setItem(0, self.ProcActualTableWidget.columnCount()-1, QTableWidgetItem('E'))
				if (self.SalidaRadioButton.isChecked()):
					self.ProcActualTableWidget.setItem(0, self.ProcActualTableWidget.columnCount()-1, QTableWidgetItem('S'))
				
				# pone 0 al valor de tiempo
				self.ProcActualTableWidget.setItem(1, self.ProcActualTableWidget.columnCount()-1, QTableWidgetItem('0'))
				
				# alinea el contenido
				self.ProcActualTableWidget.item(0,self.ProcActualTableWidget.columnCount()-1).setTextAlignment(Qt.AlignCenter)
				self.ProcActualTableWidget.item(1,self.ProcActualTableWidget.columnCount()-1).setTextAlignment(Qt.AlignCenter)
				
				# agrega si o si otra rafaga de CPU, tiempo 0, alinea 
				self.ProcActualTableWidget.setColumnCount(self.ProcActualTableWidget.columnCount()+1)
				self.ProcActualTableWidget.setItem(0, self.ProcActualTableWidget.columnCount()-1, QTableWidgetItem('CPU'))
				self.ProcActualTableWidget.setItem(1, self.ProcActualTableWidget.columnCount()-1, QTableWidgetItem('0'))
				self.ProcActualTableWidget.item(0,self.ProcActualTableWidget.columnCount()-1).setTextAlignment(Qt.AlignCenter)
				self.ProcActualTableWidget.item(1,self.ProcActualTableWidget.columnCount()-1).setTextAlignment(Qt.AlignCenter)
		else:
			self.ProcActualTableWidget.item(0,0).setBackground(QColor("#FF0000"))

	def agregar_proceso(self):
		if self.ListProcCargTableWidget.rowCount() < 10:
			if (self.verificar_rafagas()):
				# crear items
				id_proc = QTableWidgetItem(str(self.IdProcSpinBox.value()))
				id_proc.setTextAlignment(Qt.AlignCenter)

				# control id de procesos, para que no haya repetidos 
				idp = str(self.IdProcSpinBox.value())

				existe = False

				for i in range(self.ListProcCargTableWidget.rowCount()):

					aux = self.ListProcCargTableWidget.item(i,0).text()
					if ' ' in aux:
						aux = aux.replace(' ', '')

					if aux == idp:
						existe = True
						self.IdProcSpinBox.setStyleSheet("background-color: rgb(255,0,0);") # rojo

				arribo = QTableWidgetItem(str(self.TASpinBox.value()))
				arribo.setTextAlignment(Qt.AlignCenter)

				# control de tamaño de proceso
				tam = self.TamProcSpinBox.value()

				# si se tiene particiones fijas
				if self.FijasRadioButton.isChecked():
					f = self.ParticionesTableWidget.rowCount()
					part_tam_max = 0
					# buscamos el tamaño maximo
					for i in range(f):
						if part_tam_max < int(self.ParticionesTableWidget.item(i,1).text()):
							part_tam_max = int(self.ParticionesTableWidget.item(i,1).text())
					if part_tam_max >= tam:
						tam = QTableWidgetItem(str(self.TamProcSpinBox.value()))
						tam.setTextAlignment(Qt.AlignCenter)
						entra = True
					else:
						entra = False
						self.TamProcSpinBox.setStyleSheet("background-color: rgb(255,0,0);") # rojo
				
				# si se tiene particiones variables
				else:
					# vemos si entra en la memoria disponible
					mem_disp = self.TamMemSpinBox.value() - int((self.TamMemSpinBox.value()) * (self.TamSoSpinBox.value())/100)
					if mem_disp >= tam:
						entra = True
						tam = QTableWidgetItem(str(self.TamProcSpinBox.value()))
						tam.setTextAlignment(Qt.AlignCenter)
					else:
						entra = False
						self.TamProcSpinBox.setStyleSheet("background-color: rgb(255,0,0);") # rojo

				# control de prioridad
				if self.ColaRandomButton.isChecked():
					arreglo_prior = ['B', 'M', 'A']
					prioridad = arreglo_prior[random.randint(0,2)]
				else:
					if self.PrioridadComboBox.currentIndex() == 0:
						prioridad = 'B'
					if self.PrioridadComboBox.currentIndex() == 1:
						prioridad = 'M'
					if self.PrioridadComboBox.currentIndex() == 2:
						prioridad = 'A'
				prioridad_item = QTableWidgetItem(prioridad)
				prioridad_item.setTextAlignment(Qt.AlignCenter)
				rafaga = ''
				nc = self.ProcActualTableWidget.columnCount()
				for i in range(nc):
					rafaga = rafaga + self.ProcActualTableWidget.item(0,i).text() + ': ' + self.ProcActualTableWidget.item(1,i).text() + '; '
				raf_item = QTableWidgetItem(rafaga)

				if entra and not existe:
					self.ListProcCargTableWidget.setRowCount(self.ListProcCargTableWidget.rowCount()+1)
					self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 0, id_proc)
					self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 1, tam)
					self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 2, arribo)
					self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 3, prioridad_item)
					self.ListProcCargTableWidget.setItem(self.ListProcCargTableWidget.rowCount()-1, 4, raf_item)
					
					# para mas comidad, pone el supuesto siguiente id a cargar 
					self.IdProcSpinBox.setValue(self.ListProcCargTableWidget.rowCount()+1)
					self.TamProcSpinBox.setValue(1)
					self.TASpinBox.setValue(0)

					# siempre dejamos una columna para la cpu
					i = 1  
					while (self.ProcActualTableWidget.columnCount()) > 1:
						self.ProcActualTableWidget.removeColumn(i)
					self.ProcActualTableWidget.item(1,0).setText('0')

					# al igual que con las particiones y la memoria 
					# una vez que carguemos un proceso, no se podran volver a modificar algunas configuraciones
					self.EntradaIzqGroupBox.setEnabled(False)
					self.TamProcSpinBox.setStyleSheet("background-color: rgb(255,255,255);")
					self.IdProcSpinBox.setStyleSheet("background-color: rgb(255,255,255);")
					self.ProcActualTableWidget.item(0,0).setBackground(QColor("#FFFFFF"))
		else: 
			self.ProcActualTableWidget.item(0,0).setBackground(QColor("#FF0000"))

	def verificar_rafagas(self):
		# ProcActualTableWidget es donde se cargan las rafagas 
		nc = self.ProcActualTableWidget.columnCount()
		for i in range(nc):
			if (self.ProcActualTableWidget.item(1,i) == None or int(self.ProcActualTableWidget.item(1,i).text()) == 0 or int(self.ProcActualTableWidget.item(1,i).text()) > 30):
				self.ProcActualTableWidget.item(1,i).setBackground(QColor("#FF0000"))
				return False
		self.limpiar_tabla_ragafas()
		return True

	# por si previamente cargaste mal, entonces no te aparece en rojo
	def limpiar_tabla_ragafas(self):
		nc = self.ProcActualTableWidget.columnCount()
		for i in range(nc):
			self.ProcActualTableWidget.item(1,i).setBackground(QColor("#FFFFFF")) # blanco

	# control de la tabla de particiones
	def control_particiones(self):
		if self.FijasRadioButton.isChecked():
			if self.ParticionesTableWidget.rowCount() > 0:
				return True
			else:
				return False 
		else:
			# particiones variables
			return True

	# control de la tabla de procesos
	def control_procesos(self):
		# if self.ProcActualTableWidget.rowCount() > 0:
		if self.ListProcCargTableWidget.rowCount() > 0:
			return True
		else:
			return False

	# dicho metodo lleva a cabo la planificacion
	# metodo planficar de la clase ventana (o Ui)
	def planificar(self):

		# este metodo lo que hace es "preparar" todos los parametros necesarios para 
		# instanciar una clase planificador y llevar a cabo dicha planificacion.

		if self.control_particiones() and self.control_procesos():

			# para evitar errores
			self.INICIARPushButton.setEnabled(False)

			# ahora si las podemos utilizar, porque vamos a tener los datos dichas opciones necesitan
			self.GuardarColaPushButton.setEnabled(True)
			self.DiagramaGanttPushButton.setEnabled(True)
			self.GraficarDiagMemPushButton.setEnabled(True)

			if self.AlgortimoComboBox.currentIndex() == 0:
				alg = 'fcfs'
			if self.AlgortimoComboBox.currentIndex() == 1:
				alg = 'pri'
			if self.AlgortimoComboBox.currentIndex() == 2:
				alg = 'mlq'
				q = self.QuantumSpinBox.value()
			if self.AlgortimoComboBox.currentIndex() == 3:
				alg = 'rrq'
				q = self.QuantumSpinBox.value()
			if self.AlgortimoComboBox.currentIndex() == 4:
				alg = 'sjf'

			# tupla de los procesos con todos su datos
			nuevo_proceso = list()
			for i in range(self.ListProcCargTableWidget.rowCount()):
				p = int(self.ListProcCargTableWidget.item(i,0).text())
				tam = int(self.ListProcCargTableWidget.item(i,1).text())
				a = int(self.ListProcCargTableWidget.item(i,2).text())
				pri = self.ListProcCargTableWidget.item(i,3).text()
				raf = self.ListProcCargTableWidget.item(i,4).text()
				
				if ' ' in pri:
					pri = pri.replace(' ', '')

				# se agrega a la lista una nueva instancia de proceso
				nuevo_proceso.append(proceso(p, tam, a, pri, raf))

			# metodo de asignacion
			if self.FirstRadioButton.isChecked():
				metodo_asignacion = 'FF'
			elif self.BestRadioButton.isChecked():
				metodo_asignacion = 'BF'
			else:
				metodo_asignacion = 'WF'

			# debemos instanciar el tipo de memoria seleccionada
			# particionado de la memoria
			if self.FijasRadioButton.isChecked():

				tm = (self.TamMemSpinBox.value()) - int((self.TamMemSpinBox.value() * (self.TamSoSpinBox.value())/100))

				# instanciamos una memoria fija
				memoria = memoria_fija(tm, metodo_asignacion)

				# hacemos la lista de particiones
				for j in range(self.ParticionesTableWidget.rowCount()):
					id_part = int(self.ParticionesTableWidget.item(j,0).text())
					tam_part = int(self.ParticionesTableWidget.item(j,1).text())

					# instanciamos una particion
					memoria.particiones.append(particion(id_part, tam_part))

			else:
				tm = (self.TamMemSpinBox.value()) - int((self.TamMemSpinBox.value() * (self.TamSoSpinBox.value())/100))
				
				# instanciamos una memoria variable
				memoria = memoria_variable(tm, metodo_asignacion)

			self.historial_particiones = list()

			# ya esta todo listo para llevar acabo la planificacion
			plan = planificador(alg, nuevo_proceso, memoria, self.QuantumSpinBox.value())

			resultado = plan.planificar() # metodo planificar de la clase planificador

			self.imprimir_resultado(resultado[0])
			plan.promediar_tiempos()
			self.imprimir_promedios(plan.retardo_prom, plan.espera_prom)

			self.datos = plan.datos_proceso
			self.SegundoSpinBox.setEnabled(True)

			self.SegundoSpinBox.setMaximum(len(self.datos)-1)

			self.resultadosPorTiempo()
			self.gantt=resultado[1]

			self.historial_particiones = resultado[2]

	def imprimir_resultado(self, texto):
		self.HistPlanifTextEdit.setText(texto)

	def imprimir_promedios(self, retorno, espera):
		self.ValorRetornoLabel.setText(str(retorno))
		self.ValorEsperaLabel.setText(str(espera))

	def graficar_gantt(self):
		self.gantt.show()

	def resultadosPorTiempo(self):

		cola_cpu=str(self.datos[self.SegundoSpinBox.value()][0]).replace('[','').replace(']','')
		self.label_21.setText(cola_cpu)

		cola_entrada = str(self.datos[self.SegundoSpinBox.value()][1]).replace('[','').replace(']','')
		self.label_26.setText(cola_entrada)

		cola_salida=str(self.datos[self.SegundoSpinBox.value()][2]).replace('[','').replace(']','')
		self.label_27.setText(cola_salida)

		enCpu = str(self.datos[self.SegundoSpinBox.value()][4]).replace('[','').replace(']','')
		self.idEnCpuLabel.setText(enCpu)

		particiones = ''

		historial = self.historial_particiones

		for i in historial:
			# pregutamos por igual tiempo, y que tenga un proceso
			if i[0] == self.SegundoSpinBox.value() and i[2] != 0:
				particiones = particiones + 'Part: ' + str(i[1]) + ' con Proc: ' + str(i[2]) + '\n'

		self.PartOcupTextEdit.setText(particiones)
		self.PartOcupTextEdit.setStyleSheet('text-align: center')

	def mostrarMapaMemoria(self):
		tiempo = self.SegundoSpinBox.value()

		historial = self.historial_particiones
		# 0 = tiempo, 1 = particion, 2 = proceso, 3 = tam particion

		espacioSo = int( (self.TamMemSpinBox.value()) * ( (self.TamSoSpinBox.value()) / 100 ))

		colores = ("red", "orange", "yellow", "green", "lightblue", "blue", "purple")
		ix_color = 0

		plt.rcdefaults()
		fig, ax = plt.subplots()

		# 1er par: posicion en y
		# 2do par: tamaño en x 
		# 3er par: tamaño en y
		# 4to par: desde donde empieza en x 
		
		# Sistema operativo
		ax.barh(1, espacioSo, 1, 0, color = "black")
		plt.plot(0,0,color = "black",label="Particion SO")		

		# Demas particiones
		desde = espacioSo 
		for i in historial:

			if i[0] == tiempo:

				if ix_color == len(colores):
					ix_color = 0

				# si no hay proceso, muestra en gris
				if i[2] == 0:
					ax.barh(1, i[3] , 1, desde, color = "gray")
					#plt.plot(0,0,color = "gray" ,label= 'Particion ' + str(i[1]) + ' sin proceso asignado')
					plt.plot(0,0,color = "gray" ,label= 'Particion ' + str(i[1]) + ' (' + str(i[3]) + ' Kb)' + ' sin proceso asignado')
					desde = desde + i[3]
					ix_color = ix_color + 1 

				else:
					ax.barh(1, i[3] , 1, desde, color = colores[ix_color])
					#plt.plot(0,0,color = colores[ix_color] ,label= 'Particion ' + str(i[1]) + ' con Proceso ' + str(i[2]) )
					plt.plot(0,0,color = colores[ix_color] ,label= 'Particion ' + str(i[1]) + ' (' + str(i[3]) + ' Kb)' + ' con Proceso ' + str(i[2]) )
					desde = desde + i[3]
					ix_color = ix_color + 1 				

		ax.set_xlabel('Tamaño de la Memoria')

		ax.set_title('Diagrama de Memoria en el tiempo: '+ str(tiempo) + 'sg')

		plt.legend()
		plt.show()

# ---------------------------------------------------- PLANIFICADOR ----------------------------------------------------

# recibe todos los parametros del metodo planificar de la clase ventana
# y luego ejecuta su propio metodo planificar

class planificador:
	def __init__(self, alg, proc, mem, q):
		self.algoritmo = alg
		self.proceso = proc # lista de procesos con sus caracteristicas
		self.memoria = mem # objeto memoria, con aloritmo de asignacion como atributo
		self.quantum = q

		self.cola = list() # general

		self.quantum = ''
		if self.algoritmo == 'rrq' or self.algoritmo == 'mlq':
			self.quantum = q

		self.cpu = list() # proceso que se esta ejecutando actualmente

		self.ent = list()
		self.sal = list()
		self.cola_bloq_e = list()
		self.cola_bloq_s = list() 
		self.cola_listos = list()

		self.datos_proceso = list()
		self.retardo_prom = 0
		self.espera_prom = 0

		self.hist_part = list()

	def ordenar_procesos(self):
		# ordena los procesos de la cola general por tiempo de arribo
		procesos_ordenados = list()
		# "proceso" es una lista de objetos proceso (con sus caracteristicas)
		while (len(self.proceso) > 0):
			tmin = self.proceso[0].arribo
			p = self.proceso[0]

			for proc in self.proceso:
				if (proc.arribo < tmin):
					# busco el menor tiempo existente
					tmin = proc.arribo
					p = proc
			# agregamos el proceso restante con el menor tiempo a la nueva lista ordenada
			procesos_ordenados.append(p)
			# sacamos dicho proceso de la lista desordenada
			self.proceso.remove(p)
		# reemplazamos la lista desordenada por la ordenada
		self.proceso = procesos_ordenados 

	# metodo planificar de la clase planificador (distinto al que existe en la clase ventana)
	def planificar(self):

		plt.title('Diagrama de Gantt',size=15)
		plt.xlabel('Tiempo',size=10)
		plt.ylabel('Procesos',size=10)

		plt.plot([0,0],[0,0], marker="^", ls="dashed", color="lime", mec="black", ms=10, alpha=1.0 ,label="Arribo del proceso")
		plt.plot([0,0],[0,0], marker="v", ls="dashed", color="red", mec="black", ms=10, alpha=1.0 ,label="Fin del proceso")
		plt.plot([0,0],[0,0], marker="^", ls="dashed", color="white",ms=10,alpha=1.0)
		plt.plot([0,0],[0,0], marker="v", ls="dashed", color="white",ms=10,alpha=1.0)
		plt.plot([0,0],[0,0], ls="solid", color="blue", mec="black", ms=10, alpha=1.0 ,lw = 4,label="En CPU")
		plt.plot([0,0],[0,0], ls="solid", color="orangered", mec="black", ms=10, alpha=1.0 ,lw = 4,label="Entrada")
		plt.plot([0,0],[0,0], ls="solid", color="darkgreen", mec="black", ms=10, alpha=1.0 ,lw = 4,label="Salida")
		plt.plot([0,0],[0,0], ls="dashed", color="gray", mec="black", ms=10, alpha=1.0 ,lw = 1,label="En cola de Listos")

		if self.algoritmo == 'fcfs' or self.algoritmo == 'rrq':
			self.ordenar_procesos()

		t = 0 
		salida = False
		resultado = ''

		if (self.algoritmo == 'rrq') or (self.algoritmo == 'mlq'):
			quantum = int(self.quantum)
		else:
			quantum = -1 # no lo vamos a ocupar

		# historial de particiones = [tiempo, particion, proceso]

		while len(self.proceso) > 0 or not salida:

			resultado = resultado + 'Tiempo: ' + str(t) + '\n'
			self.agregarCola(t)
			self.agregarHistorialParticiones(t)

			aux_listos = ''
			for k in range( len(self.cola_listos)):
				aux_listos = aux_listos + str(self.cola_listos[k][0]) + ', '

			resultado = resultado + '->Cola de Listos: ' + aux_listos + '\n'

			if ( len(self.cpu) == 0 or quantum == 0 ):

				if quantum == 0:
					quantum = self.quantum
					# resultado=resultado+'#Q!'+'\n'
					if (len(self.cpu) != 0):
						self.guardar_pcb()

				if len(self.cola_listos) > 0:

					# Ordenamiento de la cola de listos para Prioridades o Colas multinivel
					if self.algoritmo == 'pri' or self.algoritmo == 'mlq':
						# ordenamos los procesos por prioridad, para ello cambiamos las letras a numeros
						cl_ordenada = list()
						for i in self.cola_listos:
							if i[2] == 2:
								x = 2
							if i[2] == 1:
								x = 1
							if i[2] == 0:
								x = 0
							if i[2] == 'B':
								x = 2
							if i[2] == 'M':
								x = 1
							if i[2] == 'A':
								x = 0
							cl_ordenada.append([i[0],i[1], x])

						# deoendiendo la cola, ordena con distintos criterios
						if self.cola_listos[0][2]==0: 
							cl_ordenada.sort(key = lambda cl_ordenada: (cl_ordenada[2]))
						elif self.cola_listos[0][2]==1:
							cl_ordenada.sort(key = lambda cl_ordenada: (cl_ordenada[2], cl_ordenada[1]))
						else: 
							cl_ordenada.sort(key = lambda cl_ordenada: (cl_ordenada[2], cl_ordenada[0]))
						
						self.cola_listos = cl_ordenada

						p = self.cola_listos[0]
						# self.cpu = [p[0],p[1],p[2]]
						self.cpu = [p[0],p[1]]

					# Ordenamiento de la cola de listos para Short Job First
					elif self.algoritmo == 'sjf':

						# ordenamos los procesos por tiempo de uso
						cl_ordenada = list()
						cl_ordenada = self.cola_listos
						
						# ordenamos primero por tiempo de uso y luego por tiempo de arribo
						cl_ordenada.sort(key = lambda cl_ordenada: (cl_ordenada[2], cl_ordenada[1]))
						
						self.cola_listos = cl_ordenada
						
						p = self.cola_listos[0]
						# self.cpu = [p[0],p[1],p[2]]
						self.cpu = [p[0],p[1]]

					# Para FCFS o Round-Robin, el ordenamiento ya se hizo
					else:
						p = self.cola_listos[0]
						self.cpu = [p[0],p[1]]


			# ------------------------------------- COLAS MULTINIVEL------------------------------------- 

			if self.algoritmo == 'mlq' and ((len(self.cola_listos)>0)):

				#------------------------------ COLA DE PRIORIDAD ALTA: RRQ -------------------------------------------------

				if (len(self.cola_listos) > 0) and ((self.cola_listos[0][2]) == 0):

					aux_bloq_e = ''
					for k in range( len(self.cola_bloq_e)):
						aux_bloq_e = aux_bloq_e + str(self.cola_bloq_e[k][0]) + ', '

					resultado = resultado + '->Cola bloq x Ent: ' + aux_bloq_e + '\n'
					if len(self.ent) == 0:
						if len(self.cola_bloq_e) > 0:
							self.elegir_proc_cb('e')

					aux_bloq_s = ''
					for k in range( len(self.cola_bloq_s)):
						aux_bloq_s = aux_bloq_s + str(self.cola_bloq_s[k][0]) + ', '				

					resultado = resultado + '->Cola bloq x Sal: ' + aux_bloq_s + '\n'
					if len(self.sal) == 0:
						if len(self.cola_bloq_s) > 0:
							self.elegir_proc_cb('s')

					self.guardar_datos()

					resultado = resultado + 'CPU: ' + str(self.cpu) + '\n'

					if len(self.cpu) > 0:
						plt.plot([t, t+1], [self.cpu[0], self.cpu[0]], ls="solid", color="blue", mec="black", ms=10, alpha=1.0 ,lw = 4)
						quantum = quantum - 1
						self.cpu[1] = (self.cpu[1]) - 1 # descuenta el tiempo que le falta para terminar de ejecutarse 

						if self.cpu[1] < 1:
							quantum = self.quantum
							self.fin_rafaga(self.cpu,'cpu', t)
							self.terminar_proceso(t+1)
							self.cpu.clear()
								
					resultado = resultado + 'Entrada: ' + str(self.ent) + '\n'
					if len(self.ent) > 0:
						plt.plot([t, t+1], [self.ent[0], self.ent[0]], color = 'chocolate', lw = 4)
						self.ent[1] = (self.ent[1]) - 1
						if self.ent[1] < 1:
							self.fin_rafaga(self.ent, 'e', t)
							self.ent.clear()

					resultado = resultado + 'Salida: ' + str(self.sal) + '\n'
					if len(self.sal) > 0:
						plt.plot([t, t+1], [self.sal[0], self.sal[0]], color = 'forestgreen', lw = 4)
						self.sal[1] = (self.sal[1]) - 1
						if self.sal[1] < 1:
							self.fin_rafaga(self.sal, 's', t)
							self.sal.clear()

				#------------------------------ COLA DE PRIORIDAD MEDIA: SJF -------------------------------------------------

				elif (len(self.cola_listos) > 0) and self.cola_listos[0][2] == 1:

					aux_bloq_e = ''
					for k in range( len(self.cola_bloq_e)):
						aux_bloq_e = aux_bloq_e + str(self.cola_bloq_e[k][0]) + ', '

					resultado = resultado + '->Cola bloq x Ent: ' + aux_bloq_e + '\n'
					if len(self.ent) == 0:
						if len(self.cola_bloq_e) > 0:
							self.elegir_proc_cb('e')

					aux_bloq_s = ''
					for k in range( len(self.cola_bloq_s)):
						aux_bloq_s = aux_bloq_s + str(self.cola_bloq_s[k][0]) + ', '				

					resultado = resultado + '->Cola bloq x Sal: ' + aux_bloq_s + '\n'
					if len(self.sal) == 0:
						if len(self.cola_bloq_s) > 0:
							self.elegir_proc_cb('s')

					self.guardar_datos()

					resultado = resultado + 'CPU: ' + str(self.cpu) + '\n'

					if len(self.cpu) > 0:
						plt.plot([t, t+1], [self.cpu[0], self.cpu[0]], ls="solid", color="blue", mec="black", ms=10, alpha=1.0 ,lw = 4)
						
						if self.algoritmo == 'rrq':
							quantum = quantum - 1
						self.cpu[1] = (self.cpu[1]) - 1 # descuenta el tiempo que le falta para terminar de ejecutarse 
		
						if self.cpu[1] < 1:
							# aqui no se necesita resetear el q 
							self.fin_rafaga(self.cpu,'cpu', t)
							self.terminar_proceso(t+1)
							self.cpu.clear()
									
					resultado = resultado + 'Entrada: ' + str(self.ent) + '\n'
					if len(self.ent) > 0:
						plt.plot([t, t+1], [self.ent[0], self.ent[0]], color = 'chocolate', lw = 4)
						self.ent[1] = (self.ent[1]) - 1
						if self.ent[1] < 1:
							self.fin_rafaga(self.ent, 'e', t)
							self.ent.clear()

					resultado = resultado + 'Salida: ' + str(self.sal) + '\n'
					if len(self.sal) > 0:
						plt.plot([t, t+1], [self.sal[0], self.sal[0]], color = 'forestgreen', lw = 4)
						self.sal[1] = (self.sal[1]) - 1
						if self.sal[1] < 1:
							self.fin_rafaga(self.sal, 's', t)
							self.sal.clear()

				#------------------------------ COLA DE PRIORIDAD BAJA: FCFS -------------------------------------------------

				elif (len(self.cola_listos) > 0) and (self.cola_listos[0][2] == 2):

					aux_bloq_e = ''
					for k in range( len(self.cola_bloq_e)):
						aux_bloq_e = aux_bloq_e + str(self.cola_bloq_e[k][0]) + ', '

					resultado = resultado + '->Cola bloq x Ent: ' + aux_bloq_e + '\n'
					if len(self.ent) == 0:
						if len(self.cola_bloq_e) > 0:
							self.elegir_proc_cb('e')

					aux_bloq_s = ''
					for k in range( len(self.cola_bloq_s)):
						aux_bloq_s = aux_bloq_s + str(self.cola_bloq_s[k][0]) + ', '				

					resultado = resultado + '->Cola bloq x Sal: ' + aux_bloq_s + '\n'
					if len(self.sal) == 0:
						if len(self.cola_bloq_s) > 0:
							self.elegir_proc_cb('s')

					self.guardar_datos()

					resultado = resultado + 'CPU: ' + str(self.cpu) + '\n'

					if len(self.cpu) > 0:
						plt.plot([t, t+1], [self.cpu[0], self.cpu[0]], ls="solid", color="blue", mec="black", ms=10, alpha=1.0 ,lw = 4)
						self.cpu[1] = (self.cpu[1]) - 1 # descuenta 
					
						if self.cpu[1] < 1:
							#quantum = self.quantum
							self.fin_rafaga(self.cpu,'cpu', t)
							self.terminar_proceso(t+1)
							self.cpu.clear()
								
					resultado = resultado + 'Entrada: ' + str(self.ent) + '\n'
					if len(self.ent) > 0:
						plt.plot([t, t+1], [self.ent[0], self.ent[0]], color = 'chocolate', lw = 4)
						self.ent[1] = (self.ent[1]) - 1
						if self.ent[1] < 1:
							self.fin_rafaga(self.ent, 'e', t)
							self.ent.clear()

					resultado = resultado + 'Salida: ' + str(self.sal) + '\n'
					if len(self.sal) > 0:
						plt.plot([t, t+1], [self.sal[0], self.sal[0]], color = 'forestgreen', lw = 4)
						self.sal[1] = (self.sal[1]) - 1
						if self.sal[1] < 1:
							self.fin_rafaga(self.sal, 's', t)
							self.sal.clear()
			
			# ------------------------------------- OTRO ALGORTMO DISTINTO DE COLAS MULTINIVEL -------------------------------------

			else:

				# agregamos al historial la cola de bloqueados por entrada
				aux_bloq_e = ''
				for k in range( len(self.cola_bloq_e)):
					aux_bloq_e = aux_bloq_e + str(self.cola_bloq_e[k][0]) + ', '

				resultado = resultado + '->Cola bloq x Ent: ' + aux_bloq_e + '\n'

				if len(self.ent) == 0:
					if len(self.cola_bloq_e) > 0:
						self.elegir_proc_cb('e')

				# agregamos al historial la cola de bloqueados por salida
				aux_bloq_s = ''
				for k in range( len(self.cola_bloq_s)):
					aux_bloq_s = aux_bloq_s + str(self.cola_bloq_s[k][0]) + ', '				
				
				resultado = resultado + '->Cola bloq x Sal: ' + aux_bloq_s + '\n'

				if len(self.sal) == 0:
					if len(self.cola_bloq_s) > 0:
						self.elegir_proc_cb('s')

				self.guardar_datos()

				resultado = resultado + 'CPU: ' + str(self.cpu) + '\n'

				if len(self.cpu) > 0:
					plt.plot([t, t+1], [self.cpu[0], self.cpu[0]], ls="solid", color="blue", mec="black", ms=10, alpha=1.0 ,lw = 4)
					
					if self.algoritmo == 'rrq':
						quantum = quantum - 1
					self.cpu[1] = (self.cpu[1]) - 1 # descuenta el tiempo que le falta para terminar de ejecutarse 
			
					if self.cpu[1] < 1:
						quantum = self.quantum 
						self.fin_rafaga(self.cpu,'cpu', t)
						self.terminar_proceso(t+1)
						self.cpu.clear()
								
				resultado = resultado + 'Entrada: ' + str(self.ent) + '\n'

				if len(self.ent) > 0:
					plt.plot([t, t+1], [self.ent[0], self.ent[0]], color = 'chocolate', lw = 4)
					self.ent[1] = (self.ent[1]) - 1
					if self.ent[1] < 1:
						self.fin_rafaga(self.ent, 'e', t)
						self.ent.clear()

				resultado = resultado + 'Salida: ' + str(self.sal) + '\n'
				if len(self.sal) > 0:
					plt.plot([t, t+1], [self.sal[0], self.sal[0]], color = 'forestgreen', lw = 4)
					self.sal[1] = (self.sal[1]) - 1
					if self.sal[1] < 1:
						self.fin_rafaga(self.sal, 's', t)
						self.sal.clear()

			salida = True
			for i in self.cola:
				if i.t_fin == 0:
					salida = False
					break

			resultado = resultado + '_______________________' + '\n'

			if len(self.cola_listos) > 0:
				for j in range(len(self.cola_listos)):
					plt.plot([t, t+1], [self.cola_listos[j][0], self.cola_listos[j][0]], ls="dashed", color = 'gray', lw = 2, alpha = 0.75)

			if len(self.cola_bloq_e) > 0:
				for j in range(len(self.cola_bloq_e)):
					plt.plot([t, t+1], [self.cola_bloq_e[j][0], self.cola_bloq_e[j][0]], ":", color="chocolate", lw=2, alpha=0.75)

			if len(self.cola_bloq_s)>0:
				for j in range(len(self.cola_bloq_s)):
					plt.plot([t, t+1], [self.cola_bloq_s[j][0], self.cola_bloq_s[j][0]], ":", color="forestgreen", lw=2, alpha=0.75)

			t = t + 1

		resultado=resultado+'Tiempo: '+str(t)+'\n'+'->Cola listos: '+str(self.cola_listos)+'\n'+'CPU: '+str(self.cpu)+'\n'+'->Cola bloq p/E:'+str(self.cola_bloq_e)+'\n'+'Entrada: '+str(self.ent)+'\n'+'->Cola bloq p/S:'+str(self.cola_bloq_s)+'\n'+'Salida: '+str(self.sal)+'\n'
		resultado=resultado+'___________________________'+'\n'
		self.guardar_datos()
		plt.legend()
			
		return[resultado, plt, self.hist_part]

	# DEMAS PROCESOS DE PLANIFICADOR

	def agregarHistorialParticiones(self, tiempo):

		# Particiones fijas
		if self.memoria.tipo == 'f':
			for i in self.memoria.particiones:
				aux = list()
				aux.append(tiempo)
				aux.append(i.id_part)
				aux.append(i.proceso)
				aux.append(i.tamaño)
				self.hist_part.append(aux)

		# Particiones variables
		else:
			id_aux = 1
			for i in self.memoria.particiones:
				aux = list()
				aux.append(tiempo)
				aux.append(id_aux)
				aux.append(i.proceso)
				aux.append(i.tamaño_particion)
				id_aux = id_aux + 1
				self.hist_part.append(aux)

	def agregarCola(self, t_actual):
		# borrar tiene los procesos que ya estan en una cola, por lo cual hay 
		# que sacarlos de la cola general (cola)
		borrar = list()
		for i in range(len(self.proceso)):
			# si el arribo es menor a t_actual y hay espacio en la memoria, lo agrega a la cola de listos
			# en el caso de que el TA sea menor es porque no pudo asignar anteriormente
			if (self.proceso[i].arribo <= t_actual):
				if (self.memoria.asignarMemoria(self.proceso[i].id, self.proceso[i].tamaño)):
					# print('proceso ', self.proceso[i].id,' asigando a cola de listos')
					nuevo = self.proceso[i]
					self.cola.append(nuevo)
					# arribo del proceso
					plt.plot([t_actual, t_actual],[0, self.proceso[i].id], "^-.", color = "lime", mec = "black", ms = 8, alpha = 1) 
					borrar.append(self.proceso[i])

		# Si el proceso esta en memoria, no hay que tenerlo en la la lista de procesos
		# por eso lo borramos
		for i in borrar:
			if (i in self.proceso):
				self.proceso.remove(i)

		# agregar a las colas particulares 
		for p in self.cola:
			if p.t_fin==0:
				#busca la siguiente rafaga a ejecutar
				while p.rafagas[p.ejecucion].tiempo==0:
					p.ejecucion=p.ejecucion+1	

				# para cola de listos 							
				if (p.rafagas[p.ejecucion].recurso) == 'cpu':	
					existe = False # en la cola de listos
					for j in self.cola_listos:
						if (j[0] == p.id):
							existe = True # el proceso esta en la cola de listos 
							break
					if not existe:
						if self.algoritmo == 'pri' or self.algoritmo == 'mlq':
							self.cola_listos.append([p.id, p.rafagas[p.ejecucion].tiempo, p.prioridad])
						elif self.algoritmo == 'sjf':
							self.cola_listos.append([p.id, p.rafagas[p.ejecucion].tiempo, p.t_uso])
						else:
							self.cola_listos.append([p.id, p.rafagas[p.ejecucion].tiempo])

				# para cola de bloqueados por entrada
				if (p.rafagas[p.ejecucion].recurso) == 'e':
					existe = False 
					for j in self.cola_bloq_e:
						if (j[0] == p.id):
							existe = True # el proceso esta en la cola de listos 
							break
					if not existe:
						self.cola_bloq_e.append([p.id, p.rafagas[p.ejecucion].tiempo])

				# para cola de bloqueados por salidas
				if (p.rafagas[p.ejecucion].recurso) == 's':
					existe = False 
					for j in self.cola_bloq_s:
						if (j[0] == p.id):
							existe = True # el proceso esta en la cola de listos 
							break
					if not existe:
						self.cola_bloq_s.append([p.id, p.rafagas[p.ejecucion].tiempo])

	def guardar_pcb(self):
		pr_en_cpu = self.cpu
		i = 0 
		while pr_en_cpu[0] != self.cola_listos[i][0]:
			i += 1
		del self.cola_listos[i]
		self.cola_listos.append(pr_en_cpu)


	def elegir_proc_cb(self, tipo):
		if tipo == 'e':
			nuevop = self.cola_bloq_e[0]
			self.ent = [nuevop[0], nuevop[1]]
		else:
			nuevop = self.cola_bloq_s[0]
			self.sal = [nuevop[0], nuevop[1]]

	def guardar_datos(self):
		colaCpu = list()
		for i in self.cola_listos:
			colaCpu.append(i[0])

		colaEnt = list()
		for i in self.cola_bloq_e:
			colaEnt.append(i[0])

		colaSal = list()
		for i in self.cola_bloq_s:
			colaSal.append(i[0])

		memoria = list()
		for i in self.memoria.particiones:
			memoria.append(copy.copy(i))

		enCpu = list()
		c = 0 # para mostrar solo el proceso, no el tiempo remanente
		for i in self.cpu:
			if c == 0:
				enCpu.append(copy.copy(i))
				c = c + 1

		self.datos_proceso.append([colaCpu, colaEnt, colaSal, memoria, enCpu])

	# cuando un proceso termina de usar un recurso, hay que sacarlo de la cola de ese recurso
	def fin_rafaga(self, recurso, tipo, t):
		p = 0 
		while (p < len(self.cola) and self.cola[p].id != recurso[0]):
			p = p + 1
		if self.cola[p].id == recurso[0]:
			self.cola[p].ejecucion = self.cola[p].ejecucion + 1

		# se borra el proceso de la cola del recurso que estaba utilizando
		if tipo == 'cpu':
			del self.cola_listos[0]
		elif tipo == 'e':
			del self.cola_bloq_e[0]
		elif tipo == 's':
			del self.cola_bloq_s[0]

	def terminar_proceso(self, t):
		# se saca de la cola general y de la memoria a un proceso que termino todas sus rafagas
		# buscamos el que se estaba ejecutando en la cola general
		x = 0 
		idp = self.cpu[0]
		while (x < len(self.cola)) and (idp != self.cola[x].id):
			x = x + 1
		if idp == self.cola[x].id:
			if self.cola[x].ejecucion == len(self.cola[x].rafagas):
				self.memoria.desasignarMemoria(self.cpu[0])
				plt.plot([t, t], [0, self.cpu[0]], "v-",ls="dashed", color = 'red', mec = 'firebrick', ms = 8, alpha = 0.75)
				self.cola[x].finalizar(t)

	def promediar_tiempos(self):
		n = len(self.cola)
		for p in self.cola:
			self.retardo_prom = self.retardo_prom + p.retorno
			self.espera_prom = self.espera_prom + p.espera

		self.retardo_prom = round(self.retardo_prom/n, 2)
		self.espera_prom = round(self.espera_prom/n, 2)

# ---------------------------------------------------- PROCESO Y RAFAGA ----------------------------------------------------

class proceso:
	def __init__(self, idp, tam, ta, prior, raf):
		self.id = idp
		self.arribo = ta
		self.tamaño = tam
		self.prioridad = prior

		self.t_fin = 0
		self.retorno = 0 
		self.t_uso = 0 

		rafagas = raf.split("; ")
		if '' in rafagas:
			rafagas.remove('')

		self.rafagas = list()
		for r in rafagas:
			r = r.split(': ')

			# lo siguiente surgio debido a problemas en el pasaje de datos de la base de datos
			if ' ' in r[0]:
				r[0] = r[0].replace(' ', '')

			if ";" in r[1]:
				r[1] = r[1].rstrip(';')

			# se crean varios objetos rafagas
			# se pasa como parametro el recurso y el tiempo que necesita para ejecutarse
			self.rafagas.append(rafaga(r[0].lower(), int(r[1])))

		for i in self.rafagas:
			self.t_uso = self.t_uso + i.tiempo

		self.espera = 0
		self.ejecucion = 0 

	def finalizar(self, t):
		self.t_fin = t
		self.retorno = self.t_fin - self.arribo
		self.espera = self.retorno - self.t_uso

class rafaga:
	def __init__(self, rec, t):
		self.recurso = rec
		self.tiempo = t

# ---------------------------------------------------- MEMORIA FIJA ----------------------------------------------------
# particion fija 
class particion:
	def __init__(self, idPart, tam):
		# tenemos id_part gracias a la tabla, esto no sucede en las particiones variable
		self.id_part = idPart
		self.tamaño = tam 
		self.tamañoProceso = 0 
		self.proceso = 0

class memoria_fija:
	def __init__(self, tam, algAsig):
		self.tamaño = tam
		self.particiones = []
		#Será el tipo de asignacion de memoria: "BF" o "FF" en el caso de MEMORIA FIJA 
		# y "WF" o "FF" en el caso de MEMORIA VARIABLE
		self.algoritmoAsig = algAsig 
		self.tipo = 'f'
 
	def asignarMemoria(self, idp, tamp):
		# First Fit
		if self.algoritmoAsig == 'FF':
			asignado = False
			for k in range(0, len(self.particiones)):
				if self.particiones[k].proceso == 0: # particion libre
					if int(self.particiones[k].tamaño) >= tamp : # el proceso entra 
						self.particiones[k].proceso = idp
						self.particiones[k].tamañoProceso = tamp
						return True 
						break
			if not asignado:
				# como hacemos el control del tam del proceso al momento de la carga, el unico problema que 
				# tendria un proceso para ser asigando es que haya o no otro proceso en la particion 

				# el proceso no pudo ser asignado
				return False
		# Best Fit
		else:
			# opcion con el metodo de ordenar particones 
			self.ordenarParticionesBF()
			for k in range(0, len(self.particiones)):
				if self.particiones[k].proceso == 0:
					if int(self.particiones[k].tamaño) >= tamp:
						self.particiones[k].proceso = idp
						self.particiones[k].tamañoProceso = tamp
						return True
						break
			return False

	def ordenarParticionesBF(self):
		(self.particiones).sort(key = lambda particion: int(particion.tamaño))

	# quitar proceso de la particion
	def desasignarMemoria(self, idp):
		for i in range(0, len(self.particiones)):
			if self.particiones[i].proceso == idp:
				self.particiones[i].proceso = 0
				self.particiones[i].tamañoProceso = 0
				break

# ---------------------------------------------------- MEMORIA VARIABLE ----------------------------------------------------

class particion_variable:
	def __init__(self, tamProc):
		self.tamaño_particion  = tamProc
		self.inicio = 0
		self.fin = self.inicio + self.tamaño_particion
		self.proceso = 0 # si es 0, no hay proceso

class memoria_variable:
	def __init__(self, tamMem, algAsig):
		self.tamaño_memoria = tamMem
		self.algoritmoAsig = algAsig # Solo FF y WF, NO BF
		self.particiones = []
		self.tipo = 'v'

	def asignarMemoria(self, idp, tamProc):
		if len(self.particiones) == 0:
			x = particion_variable(tamProc)
			x.proceso = idp
			x.fin = tamProc

			self.particiones.append(x)

			y = particion_variable(self.tamaño_memoria - tamProc)
			y.proceso = 0
			y.inicio = x.fin
			y.fin = self.tamaño_memoria

			self.particiones.append(y)

			return True
		else:
			# FF
			if self.algoritmoAsig != 'WF': 
				flag = False
				for i in range(0 , len(self.particiones)):

					if self.particiones[i].proceso == 0:

						if self.particiones[i].tamaño_particion == tamProc:
							self.particiones[i].proceso = idp
							return True
							break

						elif self.particiones[i].tamaño_particion > tamProc :
							tamañoNuevo = self.particiones[i].tamaño_particion - tamProc
							z = particion_variable(tamañoNuevo)

							self.particiones[i].tamaño_particion = tamProc
							self.particiones[i].proceso = idp
							self.particiones[i].fin = self.particiones[i].inicio + tamProc

							z.proceso = 0 
							z.inicio = self.particiones[i].fin
							z.fin = z.inicio + z.tamaño_particion

							flag = True
							pos = i + 1
							break

				if flag==True:
					self.particiones.insert(pos,z)
					return True
				else:
					return False

			# WF
			else:
				mayor=0
				mayorPos="null" 
				for i in range(0,len(self.particiones)):

					if self.particiones[i].proceso == 0:

						if self.particiones[i].tamaño_particion >= tamProc:
							if self.particiones[i].tamaño_particion > mayor:	
								mayor = self.particiones[i].tamaño_particion
								mayorPos=i

				if mayorPos != "null":
					if self.particiones[mayorPos].tamaño_particion == tamProc:
						self.particiones[mayorPos].proceso = idp
						return True

					elif self.particiones[mayorPos].tamaño_particion > tamProc:

						tamañoNuevo=self.particiones[mayorPos].tamaño_particion - tamProc
						z=particion_variable(tamañoNuevo)

						self.particiones[mayorPos].tamaño_particion = tamProc
						self.particiones[mayorPos].proceso = idp
						self.particiones[mayorPos].fin = self.particiones[mayorPos].inicio + tamProc

						z.proceso=0
						z.inicio=self.particiones[mayorPos].fin
						z.fin=z.inicio+z.tamaño_particion

						flag = True
						pos = mayorPos + 1
						self.particiones.insert(pos,z)
						return True
				else:
					return False

	def desasignarMemoria(self, idp):
		ant_libre = False
		pos_libre = False
		for i in range(0, len(self.particiones)):
			# buscamos la particion donde esta el proceso
			if self.particiones[i].proceso == idp:
				# la particion no es la primera, ni la utima en la memoria
				if i != 0 and i != (len(self.particiones) - 1):
					
					# la particion anterior esta libre
					if self.particiones[i-1].proceso == 0:
						ant_libre = True
						pos1 = i - 1 
						self.particiones[i].inicio = self.particiones[i-1].inicio
						self.particiones[i].tamaño_particion = self.particiones[i].tamaño_particion + self.particiones[i-1].tamaño_particion 
					
					# la particion siguiente esta libre
					if self.particiones[i+1].proceso == 0:
						pos_libre = True
						pos2 = i + 1
						self.particiones[i].tamaño_particion = self.particiones[i].tamaño_particion + self.particiones[i+1].tamaño_particion 
						self.particiones[i].fin = self.particiones[i+1].fin
					
					# la particion resultante queda libre
					self.particiones[i].proceso = 0
					break

				# es la primer particion
				if i == 0:
					# nuevo, porque daba out of index 
					if (len(self.particiones) > 1) and (self.particiones[i+1].proceso == 0):
						pos_libre = True
						pos2 = i + 1
						self.particiones[i].tamaño_particion = self.particiones[i].tamaño_particion + self.particiones[i+1].tamaño_particion 
						self.particiones[i].fin = self.particiones[i+1].fin
					self.particiones[i].proceso = 0
					break

				# es la ultima particion
				if i == (len(self.particiones) - 1):
					if self.particiones[i - 1].proceso == 0:
						ant_libre = True
						pos1 = i - 1
						self.particiones[i].inicio = self.particiones[i-1].inicio
						self.particiones[i].tamaño_particion = self.particiones[i].tamaño_particion + self.particiones[i-1].tamaño_particion 
					self.particiones[i].proceso = 0 
					break
					
		if ant_libre:
			del(self.particiones[pos1])
			if pos_libre:
				del(self.particiones[pos2 - 1])
		else:
			if pos_libre:
				del(self.particiones[pos2])

# Instancia que da inicio al programa
app = QtWidgets.QApplication(sys.argv)
# crea un objeto ventana de la clase ui
window = Ui()
# mostrar ventana
window.show()
# ejecutar 
app.exec_()