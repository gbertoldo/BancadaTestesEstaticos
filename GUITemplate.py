# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Bancada de testes estáticos - GFT/Carl Sagan", pos = wx.DefaultPosition, size = wx.Size( 1000,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 1000,700 ), wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.panelControl = wx.Panel( self.panelMain, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.panelControl.SetMaxSize( wx.Size( 300,-1 ) )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.panelControl, wx.ID_ANY, u"Conexão" ), wx.VERTICAL )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.bmpConnStatus = wx.StaticBitmap( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.bmpConnStatus, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		choiceSerialChoices = []
		self.choiceSerial = wx.Choice( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choiceSerialChoices, 0 )
		self.choiceSerial.SetSelection( 0 )
		bSizer4.Add( self.choiceSerial, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.bmpBtnReload = wx.BitmapButton( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|0 )
		bSizer4.Add( self.bmpBtnReload, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer12.Add( bSizer4, 1, wx.EXPAND, 5 )

		self.btnConnect = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Conectar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.btnConnect, 0, wx.ALL|wx.EXPAND, 5 )


		sbSizer2.Add( bSizer12, 1, wx.EXPAND, 5 )


		bSizer2.Add( sbSizer2, 0, wx.ALL|wx.EXPAND, 5 )

		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.panelControl, wx.ID_ANY, u"Configuração" ), wx.VERTICAL )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		self.btnCalibrate = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Calibrar", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.btnCalibrate.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer5.Add( self.btnCalibrate, 0, wx.ALL|wx.EXPAND, 5 )

		radioBoxUnitsChoices = [ u"N", u"kgf", u"gf" ]
		self.radioBoxUnits = wx.RadioBox( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Unidade", wx.DefaultPosition, wx.DefaultSize, radioBoxUnitsChoices, 1, wx.RA_SPECIFY_ROWS )
		self.radioBoxUnits.SetSelection( 0 )
		bSizer5.Add( self.radioBoxUnits, 0, wx.ALL|wx.EXPAND, 5 )

		radioBoxGraphOptionChoices = [ u"Acumulado", u"Deslizante" ]
		self.radioBoxGraphOption = wx.RadioBox( sbSizer3.GetStaticBox(), wx.ID_ANY, u"Gráfico", wx.DefaultPosition, wx.DefaultSize, radioBoxGraphOptionChoices, 1, wx.RA_SPECIFY_ROWS )
		self.radioBoxGraphOption.SetSelection( 0 )
		bSizer5.Add( self.radioBoxGraphOption, 0, wx.EXPAND|wx.ALL, 5 )


		sbSizer3.Add( bSizer5, 0, wx.EXPAND, 5 )


		bSizer2.Add( sbSizer3, 0, wx.ALL|wx.EXPAND, 5 )

		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self.panelControl, wx.ID_ANY, u"Dados" ), wx.VERTICAL )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )

		self.sTxtForceLabel = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Força (kgf):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtForceLabel.Wrap( -1 )

		gSizer1.Add( self.sTxtForceLabel, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.sTxtForce = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"---", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtForce.Wrap( -1 )

		gSizer1.Add( self.sTxtForce, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.sTxtMaxForceLabel = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Força máxima (kgf)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtMaxForceLabel.Wrap( -1 )

		gSizer1.Add( self.sTxtMaxForceLabel, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.sTxtMaxForce = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"---", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtMaxForce.Wrap( -1 )

		gSizer1.Add( self.sTxtMaxForce, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer6.Add( gSizer1, 1, wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText7 = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Status:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		self.m_staticText7.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer11.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.sTxtStatus = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"PRONTO PARA GRAVAR", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtStatus.Wrap( -1 )

		self.sTxtStatus.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		bSizer11.Add( self.sTxtStatus, 0, wx.ALL, 5 )


		bSizer6.Add( bSizer11, 1, wx.EXPAND, 5 )

		self.sTxtOFileName = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"---", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtOFileName.Wrap( -1 )

		bSizer6.Add( self.sTxtOFileName, 0, wx.ALL|wx.EXPAND, 5 )


		sbSizer4.Add( bSizer6, 1, wx.EXPAND, 5 )


		bSizer2.Add( sbSizer4, 0, wx.ALL|wx.EXPAND, 5 )

		sbSizer41 = wx.StaticBoxSizer( wx.StaticBox( self.panelControl, wx.ID_ANY, u"Controle" ), wx.VERTICAL )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.btnClearPlot = wx.Button( sbSizer41.GetStaticBox(), wx.ID_ANY, u"Limpar", wx.DefaultPosition, wx.Size( -1,35 ), 0 )
		self.btnClearPlot.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer14.Add( self.btnClearPlot, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.btnTare = wx.Button( sbSizer41.GetStaticBox(), wx.ID_ANY, u"Tara", wx.DefaultPosition, wx.Size( -1,35 ), 0 )
		self.btnTare.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer14.Add( self.btnTare, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		sbSizer41.Add( bSizer14, 0, wx.EXPAND, 5 )

		self.btnStartRec = wx.Button( sbSizer41.GetStaticBox(), wx.ID_ANY, u"Iniciar gravação", wx.DefaultPosition, wx.Size( -1,35 ), 0 )
		self.btnStartRec.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		sbSizer41.Add( self.btnStartRec, 0, wx.ALL|wx.EXPAND, 5 )

		self.btnStopRecClick = wx.Button( sbSizer41.GetStaticBox(), wx.ID_ANY, u"Parar gravação", wx.DefaultPosition, wx.Size( -1,35 ), 0 )
		self.btnStopRecClick.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		sbSizer41.Add( self.btnStopRecClick, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( sbSizer41, 0, wx.EXPAND|wx.ALL, 5 )


		self.panelControl.SetSizer( bSizer2 )
		self.panelControl.Layout()
		bSizer2.Fit( self.panelControl )
		fgSizer1.Add( self.panelControl, 1, wx.EXPAND |wx.ALL, 5 )

		self.panelPlotBackground = wx.Panel( self.panelMain, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.panelPlotBackground.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )

		fgSizer1.Add( self.panelPlotBackground, 1, wx.EXPAND |wx.ALL, 5 )


		self.panelMain.SetSizer( fgSizer1 )
		self.panelMain.Layout()
		fgSizer1.Fit( self.panelMain )
		bSizer1.Add( self.panelMain, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.bmpBtnReload.Bind( wx.EVT_BUTTON, self.onBmpBtnReloadClick )
		self.btnConnect.Bind( wx.EVT_BUTTON, self.onBtnConnectClick )
		self.btnCalibrate.Bind( wx.EVT_BUTTON, self.onBtnCalibrateClick )
		self.radioBoxUnits.Bind( wx.EVT_RADIOBOX, self.onRadioBoxUnitsClick )
		self.radioBoxGraphOption.Bind( wx.EVT_RADIOBOX, self.onRadioBoxGraphOptionClick )
		self.btnClearPlot.Bind( wx.EVT_BUTTON, self.onBtnClearPlotClick )
		self.btnTare.Bind( wx.EVT_BUTTON, self.onBtnTareClick )
		self.btnStartRec.Bind( wx.EVT_BUTTON, self.onBtnStartRecClick )
		self.btnStopRecClick.Bind( wx.EVT_BUTTON, self.onBtnStopRecClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onBmpBtnReloadClick( self, event ):
		event.Skip()

	def onBtnConnectClick( self, event ):
		event.Skip()

	def onBtnCalibrateClick( self, event ):
		event.Skip()

	def onRadioBoxUnitsClick( self, event ):
		event.Skip()

	def onRadioBoxGraphOptionClick( self, event ):
		event.Skip()

	def onBtnClearPlotClick( self, event ):
		event.Skip()

	def onBtnTareClick( self, event ):
		event.Skip()

	def onBtnStartRecClick( self, event ):
		event.Skip()

	def onBtnStopRecClick( self, event ):
		event.Skip()


###########################################################################
## Class CalibrationFrame
###########################################################################

class CalibrationFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Assistente de calibração", pos = wx.DefaultPosition, size = wx.Size( 500,320 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 500,320 ), wx.DefaultSize )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel5 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel4 = wx.Panel( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.sTxtStep1 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"1) Informe a massa padrão de calibração (kg):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtStep1.Wrap( -1 )

		bSizer10.Add( self.sTxtStep1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.txtCtrlMass = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.txtCtrlMass, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer9.Add( bSizer10, 0, wx.EXPAND, 5 )

		self.sTxtStep2 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"2) Posicione a célula de carga na vertical.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtStep2.Wrap( -1 )

		bSizer9.Add( self.sTxtStep2, 0, wx.ALL, 5 )

		self.sTxtStep3 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"3) Efetuando leitura sem carga.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtStep3.Wrap( -1 )

		bSizer9.Add( self.sTxtStep3, 0, wx.ALL, 5 )

		self.gaugeStep3 = wx.Gauge( self.m_panel4, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.gaugeStep3.SetValue( 0 )
		bSizer9.Add( self.gaugeStep3, 0, wx.ALL|wx.EXPAND, 10 )

		self.sTxtStep4 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"4) Insira a massa de calibração.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtStep4.Wrap( -1 )

		bSizer9.Add( self.sTxtStep4, 0, wx.ALL, 5 )

		self.sTxtStep5 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"5) Efetuando leitura com a massa de calibração.", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.sTxtStep5.Wrap( -1 )

		bSizer9.Add( self.sTxtStep5, 0, wx.ALL, 5 )

		self.gaugeStep5 = wx.Gauge( self.m_panel4, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.gaugeStep5.SetValue( 0 )
		bSizer9.Add( self.gaugeStep5, 0, wx.ALL|wx.EXPAND, 10 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.btnCancel = wx.Button( self.m_panel4, wx.ID_ANY, u"Cancelar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.btnCancel, 0, wx.ALL, 5 )

		self.btnNext = wx.Button( self.m_panel4, wx.ID_ANY, u"Próximo", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.btnNext, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer11, 0, wx.ALIGN_RIGHT, 5 )


		self.m_panel4.SetSizer( bSizer9 )
		self.m_panel4.Layout()
		bSizer9.Fit( self.m_panel4 )
		bSizer12.Add( self.m_panel4, 1, wx.EXPAND|wx.ALL, 15 )


		self.m_panel5.SetSizer( bSizer12 )
		self.m_panel5.Layout()
		bSizer12.Fit( self.m_panel5 )
		bSizer8.Add( self.m_panel5, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer8 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.btnCancel.Bind( wx.EVT_BUTTON, self.onBtnCancelClick )
		self.btnNext.Bind( wx.EVT_BUTTON, self.onBtnNextClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def onBtnCancelClick( self, event ):
		event.Skip()

	def onBtnNextClick( self, event ):
		event.Skip()


