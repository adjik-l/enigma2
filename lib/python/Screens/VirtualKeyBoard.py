# -*- coding: UTF-8 -*-
from enigma import eListboxPythonMultiContent, gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER, getPrevAsciiCode
from Screen import Screen
from Components.Language import language
from Components.ActionMap import NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.Input import Input
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from Tools.NumericalTextInput import NumericalTextInput
import skin

class VirtualKeyBoardList(MenuList):
	def __init__(self, list, enableWrapAround=False):
		MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
		font = skin.fonts.get("VirtualKeyboard", ("Regular", 28, 45))
		self.l.setFont(0, gFont(font[0], font[1]))
		self.l.setItemHeight(font[2])

class VirtualKeyBoardEntryComponent:
	pass

class VirtualKeyBoard(Screen):

	def __init__(self, session, title="", **kwargs):
		Screen.__init__(self, session)
		self.setTitle(_("Virtual keyboard"))
		self.keys_list = []
		self.shiftkeys_list = []
		self.lang = language.getLanguage()
		self.nextLang = None
		self.shiftMode = False
		self.selectedKey = 0
		self.smsChar = None
		self.sms = NumericalTextInput(self.smsOK)

		self.key_bg = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_bg.png"))
		self.key_sel = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_sel.png"))
		self.key_backspace = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_backspace.png"))
		self.key_all = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_all.png"))
		self.key_clr = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_clr.png"))
		self.key_esc = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_esc.png"))
		self.key_ok = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_ok.png"))
		self.key_shift = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_shift.png"))
		self.key_shift_sel = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_shift_sel.png"))
		self.key_space = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_space.png"))
		self.key_left = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_left.png"))
		self.key_right = LoadPixmap(path=resolveFilename(SCOPE_CURRENT_SKIN, "skin_default/vkey_right.png"))

		self.keyImages =  {
				"BACKSPACE": self.key_backspace,
				"ALL": self.key_all,
				"EXIT": self.key_esc,
				"OK": self.key_ok,
				"SHIFT": self.key_shift,
				"SPACE": self.key_space,
				"LEFT": self.key_left,
				"RIGHT": self.key_right
			}
		self.keyImagesShift = {
				"BACKSPACE": self.key_backspace,
				"CLEAR": self.key_clr,
				"EXIT": self.key_esc,
				"OK": self.key_ok,
				"SHIFT": self.key_shift_sel,
				"SPACE": self.key_space,
				"LEFT": self.key_left,
				"RIGHT": self.key_right
			}

		self["country"] = StaticText("")
		self["header"] = Label(title)
		self["text"] = Input(currPos=len(kwargs.get("text", "").decode("utf-8",'ignore')), allMarked=False, **kwargs)
		self["list"] = VirtualKeyBoardList([])

		self["actions"] = NumberActionMap(["OkCancelActions", "WizardActions", "ColorActions", "KeyboardInputActions", "InputBoxActions", "InputAsciiActions"],
			{
				"gotAsciiCode": self.keyGotAscii,
				"ok": self.okClicked,
				"cancel": self.exit,
				"left": self.left,
				"right": self.right,
				"up": self.up,
				"down": self.down,
				"red": self.exit,
				"green": self.ok,
				"yellow": self.switchLang,
				"blue": self.shiftClicked,
				"deleteBackward": self.backClicked,
				"deleteForward": self.forwardClicked,
				"back": self.exit,
				"pageUp": self.cursorRight,
				"pageDown": self.cursorLeft,
				"1": self.keyNumberGlobal,
				"2": self.keyNumberGlobal,
				"3": self.keyNumberGlobal,
				"4": self.keyNumberGlobal,
				"5": self.keyNumberGlobal,
				"6": self.keyNumberGlobal,
				"7": self.keyNumberGlobal,
				"8": self.keyNumberGlobal,
				"9": self.keyNumberGlobal,
				"0": self.keyNumberGlobal,
			}, -2)
		self.setLang()
		self.onExecBegin.append(self.setKeyboardModeAscii)
		self.onLayoutFinish.append(self.buildVirtualKeyBoard)
		self.onClose.append(self.__onClose)

	def __onClose(self):
		self.sms.timer.stop()

	def switchLang(self):
		self.lang = self.nextLang
		self.setLang()
		self.buildVirtualKeyBoard()

	def setLang(self):
		if self.lang == 'cs_CZ':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"??", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"??", u"@", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"OK"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"??", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"??", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"??", u"??", u"'"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"OK"]]
			self.nextLang = 'de_DE'
		elif self.lang == 'de_DE':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"??", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"??", u"??", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"@", u"??", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"??", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"??", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"??", u"??", u"'"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'el_GR'
		elif self.lang == 'el_GR':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"=", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"[", u"]"],
				[u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u";", u"'", u"-"],
				[u"\\", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u",", ".", u"/", u"ALL"],
				[u"SHIFT", u"SPACE", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"OK"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u"@", u"#", u"$", u"%", u"^", u"&", u"*", u"(", u")", u"BACKSPACE"],
				[u"+", u"???", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"{", u"}"],
				[u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u":", u'"', u"_"],
				[u"|", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"<", u">", u"?", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"OK"]]
			self.nextLang = 'es_ES'
		elif self.lang == 'es_ES':
			#still missing keys (u"????")
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"??", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"??", u"??", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"@", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"OK"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"??", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"??", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"??", u"??", u"'"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"OK"]]
			self.nextLang = 'fa_IR'
		elif self.lang == 'fa_IR':
			self.keys_list = [
				[u"EXIT", u"\u06F1", u"\u06F2", u"\u06F3", u"\u06F4", u"\u06F5", u"\u06F6", u"\u06F7", u"\u06F8", u"\u06F9", u"\u06F0", u"BACKSPACE"],
				[u"\u0636", u"\u0635", u"\u062B", u"\u0642", u"\u0641", u"\u063A", u"\u0639", u"\u0647", u"\u062E", u"\u062D", u"-", u"\u062C"],
				[u"\u0634", u"\u0633", u"\u06CC", u"\u0628", u"\u0644", u"\u0627", u"\u062A", u"\u0646", u"\u0645", u"\u06A9", u"\u06AF", u"\u067E"],
				[u"<", u"\u0638", u"\u0637", u"\u0632", u"\u0631", u"\u0630", u"\u062F", u"\u0626", u"\u0648", ".", u"/", u"ALL"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT", u"*"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u"@", u"#", u"$", u"%", u"^", u"&", u"(", u")", u"=", u"BACKSPACE"],
				[u"\u0636", u"\u0635", u"\u062B", u"\u0642", u"\u060C", u"\u061B", u"\u0639", u"\u0647", u"\u062E", u"\u062D", u"+", u"\u0686"],
				[u"\u0634", u"\u0633", u"\u06CC", u"\u0628", u"\u06C0", u"\u0622", u"\u062A", u"\u0646", u"\u0645", u"?", u'"', u"|"],
				[u">", u"\u0629", u"\u064A", u"\u0698", u"\u0624", u"\u0625", u"\u0623", u"\u0621", u";", u":", u"\u061F", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT", u"~"]]
			self.nextLang = 'fi_FI'
		elif self.lang == 'fi_FI':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"??", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"??", u"??", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"@", u"??", u"??", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"??", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"??", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"??", u"??", u"'"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"??", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'fr_FR'
		elif self.lang == 'fr_FR':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"a", u"z", u"e", u"r", u"t", u"y", u"u", u"i", u"o", u"p", u"??", u"??"],
				[u"q", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"m", u"??", u"??"],
				[u"<", u"w", u"x", u"c", u"v", u"b", u"n", u",", u";", u":", u"=", u"ALL"],
				[u"SHIFT", u"SPACE", u"??", u"??", u"??", u"??", u"??", u"#", u"-", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"&", u'@', u'"', u"???", u"??", u"!", u"??", u"(", u")", u"_", u"BACKSPACE"],
				[u"A", u"Z", u"E", u"R", u"T", u"Y", u"U", u"I", u"O", u"P", u"??", u"??"],
				[u"Q", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"M", u"??", u"??"],
				[u">", u"W", u"X", u"C", u"V", u"B", u"N", u"?", u".", u"+", u"~", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"??", u"??", u"??", u"??", u"??", u"/",u"\\", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'lv_LV'
		elif self.lang == 'lv_LV':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"y", u"u", u"i", u"o", u"p", u"-", u"??"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u";", u"'", u"??"],
				[u"<", u"z", u"x", u"c", u"v", u"b", u"n", u"m", u",", u".", u"??", u"ALL"],
				[u"SHIFT", u"SPACE", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u"@", u"$", u"*", u"(", u")", u"_", u"=", u"/", u"\\", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Y", u"U", u"I", u"O", u"P", u"+", u"??"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u":", u'"', u"??"],
				[u">", u"Z", u"X", u"C", u"V", u"B", u"N", u"M", u"#", u"?", u"??", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"LEFT", u"RIGHT"]]
			self.nextLang = 'pl_PL'
		elif self.lang == 'pl_PL':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"y", u"u", u"i", u"o", u"p", u"-", u"["],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u";", u"'", u"\\"],
				[u"<", u"z", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"/", u"ALL"],
				[u"SHIFT", u"SPACE", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"OK"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u"@", u"#", u"$", u"%", u"^", u"&", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Y", u"U", u"I", u"O", u"P", u"*", u"]"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"?", u'"', u"|"],
				[u">", u"Z", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"OK"]]
			self.nextLang = 'ru_RU'
		elif self.lang == 'ru_RU':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"+"],
				[u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"#"],
				[u"<", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u",", u".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"@", u"??", u"??", u"??", u"??", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"??", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"*"],
				[u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"'"],
				[u">", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"??", u"??", u"??", u"??", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'sk_SK'
		elif self.lang =='sk_SK':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"??", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"??", u"@", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"??", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"??", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"??", u"??", u"'"],
				[u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??", u"??"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"??", u"??", u"??", u"??", u"??", u"??", u"OK"]]
			self.nextLang = 'sv_SE'
		elif self.lang == 'sv_SE':
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"z", u"u", u"i", u"o", u"p", u"??", u"+"],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u"??", u"??", u"#"],
				[u"<", u"y", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"-", u"ALL"],
				[u"SHIFT", u"SPACE", u"@", u"??", u"??", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u'"', u"??", u"$", u"%", u"&", u"/", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Z", u"U", u"I", u"O", u"P", u"??", u"*"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"??", u"??", u"'"],
				[u">", u"Y", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"?", u"\\", u"??", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'th_TH'
		elif self.lang == 'th_TH':
			self.keys_list = [[u"EXIT", "\xe0\xb9\x85", "\xe0\xb8\xa0", "\xe0\xb8\x96", "\xe0\xb8\xb8", "\xe0\xb8\xb6", "\xe0\xb8\x84", "\xe0\xb8\x95", "\xe0\xb8\x88", "\xe0\xb8\x82", "\xe0\xb8\x8a", u"BACKSPACE"],
				["\xe0\xb9\x86", "\xe0\xb9\x84", "\xe0\xb8\xb3", "\xe0\xb8\x9e", "\xe0\xb8\xb0", "\xe0\xb8\xb1", "\xe0\xb8\xb5", "\xe0\xb8\xa3", "\xe0\xb8\x99", "\xe0\xb8\xa2", "\xe0\xb8\x9a", "\xe0\xb8\xa5"],
				["\xe0\xb8\x9f", "\xe0\xb8\xab", "\xe0\xb8\x81", "\xe0\xb8\x94", "\xe0\xb9\x80", "\xe0\xb9\x89", "\xe0\xb9\x88", "\xe0\xb8\xb2", "\xe0\xb8\xaa", "\xe0\xb8\xa7", "\xe0\xb8\x87", "\xe0\xb8\x83"],
				["\xe0\xb8\x9c", "\xe0\xb8\x9b", "\xe0\xb9\x81", "\xe0\xb8\xad", "\xe0\xb8\xb4", "\xe0\xb8\xb7", "\xe0\xb8\x97", "\xe0\xb8\xa1", "\xe0\xb9\x83", "\xe0\xb8\x9d", "", u"ALL"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT"]]
			self.shiftkeys_list = [[u"EXIT", "\xe0\xb9\x91", "\xe0\xb9\x92", "\xe0\xb9\x93", "\xe0\xb9\x94", "\xe0\xb8\xb9", "\xe0\xb9\x95", "\xe0\xb9\x96", "\xe0\xb9\x97", "\xe0\xb9\x98", "\xe0\xb9\x99", u"BACKSPACE"],
				["\xe0\xb9\x90", "", "\xe0\xb8\x8e", "\xe0\xb8\x91", "\xe0\xb8\x98", "\xe0\xb9\x8d", "\xe0\xb9\x8a", "\xe0\xb8\x93", "\xe0\xb8\xaf", "\xe0\xb8\x8d", "\xe0\xb8\x90", "\xe0\xb8\x85"],
				["\xe0\xb8\xa4", "\xe0\xb8\x86", "\xe0\xb8\x8f", "\xe0\xb9\x82", "\xe0\xb8\x8c", "\xe0\xb9\x87", "\xe0\xb9\x8b", "\xe0\xb8\xa9", "\xe0\xb8\xa8", "\xe0\xb8\x8b", "", "\xe0\xb8\xbf"],
				["", "", "\xe0\xb8\x89", "\xe0\xb8\xae", "\xe0\xb8\xba", "\xe0\xb9\x8c", "", "\xe0\xb8\x92", "\xe0\xb8\xac", "\xe0\xb8\xa6", "", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT"]]
			self.nextLang = 'en_EN'
		else:
			self.keys_list = [
				[u"EXIT", u"1", u"2", u"3", u"4", u"5", u"6", u"7", u"8", u"9", u"0", u"BACKSPACE"],
				[u"q", u"w", u"e", u"r", u"t", u"y", u"u", u"i", u"o", u"p", u"-", u"["],
				[u"a", u"s", u"d", u"f", u"g", u"h", u"j", u"k", u"l", u";", u"'", u"\\"],
				[u"<", u"z", u"x", u"c", u"v", u"b", u"n", u"m", u",", ".", u"/", u"ALL"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT", u"*"]]
			self.shiftkeys_list = [
				[u"EXIT", u"!", u"@", u"#", u"$", u"%", u"^", u"&", u"(", u")", u"=", u"BACKSPACE"],
				[u"Q", u"W", u"E", u"R", u"T", u"Y", u"U", u"I", u"O", u"P", u"+", u"]"],
				[u"A", u"S", u"D", u"F", u"G", u"H", u"J", u"K", u"L", u"?", u'"', u"|"],
				[u">", u"Z", u"X", u"C", u"V", u"B", u"N", u"M", u";", u":", u"_", u"CLEAR"],
				[u"SHIFT", u"SPACE", u"OK", u"LEFT", u"RIGHT", u"~"]]
			self.lang = 'en_EN'
			self.nextLang = 'cs_CZ'
		self["country"].setText(self.lang)
		self.max_key=47+len(self.keys_list[4])

	def virtualKeyBoardEntryComponent(self, keys):
		w, h = skin.parameters.get("VirtualKeyboard",(45, 45))
		key_bg_width = self.key_bg and self.key_bg.size().width() or w
		key_images = self.shiftMode and self.keyImagesShift or self.keyImages
		res = [keys]
		text = []
		x = 0
		for key in keys:
			png = key_images.get(key, None)
			if png:
				width = png.size().width()
				res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=png))
			else:
				width = key_bg_width
				res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=self.key_bg))
				text.append(MultiContentEntryText(pos=(x, 0), size=(width, h), font=0, text=key.encode("utf-8"), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
			x += width
		return res + text

	def buildVirtualKeyBoard(self):
		self.previousSelectedKey = None
		self.list = []
		for keys in self.shiftMode and self.shiftkeys_list or self.keys_list:
			self.list.append(self.virtualKeyBoardEntryComponent(keys))
		self.markSelectedKey()

	def markSelectedKey(self):
		w, h = skin.parameters.get("VirtualKeyboard",(45, 45))
		if self.previousSelectedKey is not None:
			self.list[self.previousSelectedKey /12] = self.list[self.previousSelectedKey /12][:-1]
		width = self.key_sel.size().width()
		x = self.list[self.selectedKey/12][self.selectedKey % 12 + 1][1]
		self.list[self.selectedKey / 12].append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=self.key_sel))
		self.previousSelectedKey = self.selectedKey
		self["list"].setList(self.list)

	def backClicked(self):
		self["text"].deleteBackward()

	def forwardClicked(self):
		self["text"].deleteForward()

	def shiftClicked(self):
		self.smsChar = None
		self.shiftMode = not self.shiftMode
		self.buildVirtualKeyBoard()

	def okClicked(self):
		self.smsChar = None
		text = (self.shiftMode and self.shiftkeys_list or self.keys_list)[self.selectedKey / 12][self.selectedKey % 12].encode("UTF-8")

		if text == "EXIT":
			self.close(None)

		elif text == "BACKSPACE":
			self["text"].deleteBackward()

		elif text == "ALL":
			self["text"].markAll()

		elif text == "CLEAR":
			self["text"].deleteAllChars()
			self["text"].update()

		elif text == "SHIFT":
			self.shiftClicked()

		elif text == "SPACE":
			self["text"].char(" ".encode("UTF-8"))

		elif text == "OK":
			self.close(self["text"].getText())

		elif text == "LEFT":
			self["text"].left()

		elif text == "RIGHT":
			self["text"].right()

		else:
			self["text"].char(text)

	def ok(self):
		self.close(self["text"].getText())

	def exit(self):
		self.close(None)

	def cursorRight(self):
		self["text"].right()

	def cursorLeft(self):
		self["text"].left()

	def left(self):
		self.smsChar = None
		self.selectedKey = self.selectedKey / 12 * 12 + (self.selectedKey + 11) % 12
		if self.selectedKey > self.max_key:
			self.selectedKey = self.max_key
		self.markSelectedKey()

	def right(self):
		self.smsChar = None
		self.selectedKey = self.selectedKey / 12 * 12 + (self.selectedKey + 1) % 12
		if self.selectedKey > self.max_key:
			self.selectedKey = self.selectedKey / 12 * 12
		self.markSelectedKey()

	def up(self):
		self.smsChar = None
		self.selectedKey -= 12
		if self.selectedKey < 0:
			self.selectedKey = self.max_key / 12 * 12 + self.selectedKey % 12
			if self.selectedKey > self.max_key:
				self.selectedKey -= 12
		self.markSelectedKey()

	def down(self):
		self.smsChar = None
		self.selectedKey += 12
		if self.selectedKey > self.max_key:
			self.selectedKey %= 12
		self.markSelectedKey()

	def keyNumberGlobal(self, number):
		self.smsChar = self.sms.getKey(number)
		self.selectAsciiKey(self.smsChar)

	def smsOK(self):
		if self.smsChar and self.selectAsciiKey(self.smsChar):
			print "pressing ok now"
			self.okClicked()

	def keyGotAscii(self):
		self.smsChar = None
		if self.selectAsciiKey(str(unichr(getPrevAsciiCode()).encode('utf-8'))):
			self.okClicked()

	def selectAsciiKey(self, char):
		if char == " ":
			char = "SPACE"
		for keyslist in (self.shiftkeys_list, self.keys_list):
			selkey = 0
			for keys in keyslist:
				for key in keys:
					if key == char:
						self.selectedKey = selkey
						if self.shiftMode != (keyslist is self.shiftkeys_list):
							self.shiftMode = not self.shiftMode
							self.buildVirtualKeyBoard()
						else:
							self.markSelectedKey()
						return True
					selkey += 1
		return False
