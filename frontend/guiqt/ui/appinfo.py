# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/guiqt/ui/appinfo.ui'
#
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AppInfoDialog(object):
    def setupUi(self, AppInfoDialog):
        AppInfoDialog.setObjectName("AppInfoDialog")
        AppInfoDialog.resize(856, 453)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AppInfoDialog.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(AppInfoDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.DetailsGroupBox = QtGui.QGroupBox(AppInfoDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DetailsGroupBox.sizePolicy().hasHeightForWidth())
        self.DetailsGroupBox.setSizePolicy(sizePolicy)
        self.DetailsGroupBox.setObjectName("DetailsGroupBox")
        self.formLayout_4 = QtGui.QFormLayout(self.DetailsGroupBox)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName("formLayout_4")
        self.NameLabel = QtGui.QLabel(self.DetailsGroupBox)
        self.NameLabel.setObjectName("NameLabel")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.NameLabel)
        self.Name = QtGui.QLineEdit(self.DetailsGroupBox)
        self.Name.setMaxLength(128)
        self.Name.setObjectName("Name")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.Name)
        self.AppIDLabel = QtGui.QLabel(self.DetailsGroupBox)
        self.AppIDLabel.setObjectName("AppIDLabel")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.AppIDLabel)
        self.AppID = QtGui.QLineEdit(self.DetailsGroupBox)
        self.AppID.setMaxLength(128)
        self.AppID.setObjectName("AppID")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.AppID)
        self.PublisherLabel = QtGui.QLabel(self.DetailsGroupBox)
        self.PublisherLabel.setObjectName("PublisherLabel")
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.PublisherLabel)
        self.Publisher = QtGui.QLineEdit(self.DetailsGroupBox)
        self.Publisher.setMaxLength(128)
        self.Publisher.setObjectName("Publisher")
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.Publisher)
        self.HomepageLabel = QtGui.QLabel(self.DetailsGroupBox)
        self.HomepageLabel.setObjectName("HomepageLabel")
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.LabelRole, self.HomepageLabel)
        self.Homepage = QtGui.QLineEdit(self.DetailsGroupBox)
        self.Homepage.setMaxLength(128)
        self.Homepage.setObjectName("Homepage")
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.FieldRole, self.Homepage)
        self.CategoryLabel = QtGui.QLabel(self.DetailsGroupBox)
        self.CategoryLabel.setObjectName("CategoryLabel")
        self.formLayout_4.setWidget(4, QtGui.QFormLayout.LabelRole, self.CategoryLabel)
        self.Category = QtGui.QComboBox(self.DetailsGroupBox)
        self.Category.setObjectName("Category")
        self.Category.addItem("")
        self.Category.setItemText(0, "Accessibility")
        self.Category.addItem("")
        self.Category.setItemText(1, "Development")
        self.Category.addItem("")
        self.Category.setItemText(2, "Education")
        self.Category.addItem("")
        self.Category.setItemText(3, "Games")
        self.Category.addItem("")
        self.Category.setItemText(4, "Graphics & Pictures")
        self.Category.addItem("")
        self.Category.setItemText(5, "Internet")
        self.Category.addItem("")
        self.Category.setItemText(6, "Music & Video")
        self.Category.addItem("")
        self.Category.setItemText(7, "Office")
        self.Category.addItem("")
        self.Category.setItemText(8, "Security")
        self.Category.addItem("")
        self.Category.setItemText(9, "Utilities")
        self.formLayout_4.setWidget(4, QtGui.QFormLayout.FieldRole, self.Category)
        self.DescriptionLabel = QtGui.QLabel(self.DetailsGroupBox)
        self.DescriptionLabel.setObjectName("DescriptionLabel")
        self.formLayout_4.setWidget(5, QtGui.QFormLayout.LabelRole, self.DescriptionLabel)
        self.Description = QtGui.QLineEdit(self.DetailsGroupBox)
        self.Description.setMaxLength(512)
        self.Description.setObjectName("Description")
        self.formLayout_4.setWidget(5, QtGui.QFormLayout.FieldRole, self.Description)
        self.LanguageLabel = QtGui.QLabel(self.DetailsGroupBox)
        self.LanguageLabel.setObjectName("LanguageLabel")
        self.formLayout_4.setWidget(6, QtGui.QFormLayout.LabelRole, self.LanguageLabel)
        self.Language = QtGui.QComboBox(self.DetailsGroupBox)
        self.Language.setObjectName("Language")
        self.Language.addItem("")
        self.Language.setItemText(0, "Multilingual")
        self.Language.addItem("")
        self.Language.setItemText(1, "English")
        self.Language.addItem("")
        self.Language.setItemText(2, "Afrikaans")
        self.Language.addItem("")
        self.Language.setItemText(3, "Albanian")
        self.Language.addItem("")
        self.Language.setItemText(4, "Arabic")
        self.Language.addItem("")
        self.Language.setItemText(5, "Armenian")
        self.Language.addItem("")
        self.Language.setItemText(6, "Basque")
        self.Language.addItem("")
        self.Language.setItemText(7, "Belarusian")
        self.Language.addItem("")
        self.Language.setItemText(8, "Bosnian")
        self.Language.addItem("")
        self.Language.setItemText(9, "Breton")
        self.Language.addItem("")
        self.Language.setItemText(10, "Bulgarian")
        self.Language.addItem("")
        self.Language.setItemText(11, "Catalan")
        self.Language.addItem("")
        self.Language.setItemText(12, "Cibemba")
        self.Language.addItem("")
        self.Language.setItemText(13, "Croatian")
        self.Language.addItem("")
        self.Language.setItemText(14, "Czech")
        self.Language.addItem("")
        self.Language.setItemText(15, "Danish")
        self.Language.addItem("")
        self.Language.setItemText(16, "Dutch")
        self.Language.addItem("")
        self.Language.setItemText(17, "Efik")
        self.Language.addItem("")
        self.Language.setItemText(18, "Estonian")
        self.Language.addItem("")
        self.Language.setItemText(19, "Farsi")
        self.Language.addItem("")
        self.Language.setItemText(20, "Finnish")
        self.Language.addItem("")
        self.Language.setItemText(21, "French")
        self.Language.addItem("")
        self.Language.setItemText(22, "Galician")
        self.Language.addItem("")
        self.Language.setItemText(23, "Georgian")
        self.Language.addItem("")
        self.Language.setItemText(24, "German")
        self.Language.addItem("")
        self.Language.setItemText(25, "Greek")
        self.Language.addItem("")
        self.Language.setItemText(26, "Hebrew")
        self.Language.addItem("")
        self.Language.setItemText(27, "Hungarian")
        self.Language.addItem("")
        self.Language.setItemText(28, "Icelandic")
        self.Language.addItem("")
        self.Language.setItemText(29, "Igbo")
        self.Language.addItem("")
        self.Language.setItemText(30, "Indonesian")
        self.Language.addItem("")
        self.Language.setItemText(31, "Irish")
        self.Language.addItem("")
        self.Language.setItemText(32, "Italian")
        self.Language.addItem("")
        self.Language.setItemText(33, "Japanese")
        self.Language.addItem("")
        self.Language.setItemText(34, "Khmer")
        self.Language.addItem("")
        self.Language.setItemText(35, "Korean")
        self.Language.addItem("")
        self.Language.setItemText(36, "Kurdish")
        self.Language.addItem("")
        self.Language.setItemText(37, "Latvian")
        self.Language.addItem("")
        self.Language.setItemText(38, "Lithuanian")
        self.Language.addItem("")
        self.Language.setItemText(39, "Luxembourgish")
        self.Language.addItem("")
        self.Language.setItemText(40, "Macedonian")
        self.Language.addItem("")
        self.Language.setItemText(41, "Malagasy")
        self.Language.addItem("")
        self.Language.setItemText(42, "Malay")
        self.Language.addItem("")
        self.Language.setItemText(43, "Mongolian")
        self.Language.addItem("")
        self.Language.setItemText(44, "Norwegian")
        self.Language.addItem("")
        self.Language.setItemText(45, "NorwegianNynorsk")
        self.Language.addItem("")
        self.Language.setItemText(46, "Pashto")
        self.Language.addItem("")
        self.Language.setItemText(47, "Polish")
        self.Language.addItem("")
        self.Language.setItemText(48, "Portuguese")
        self.Language.addItem("")
        self.Language.setItemText(49, "PortugueseBR")
        self.Language.addItem("")
        self.Language.setItemText(50, "Romanian")
        self.Language.addItem("")
        self.Language.setItemText(51, "Russian")
        self.Language.addItem("")
        self.Language.setItemText(52, "Serbian")
        self.Language.addItem("")
        self.Language.setItemText(53, "SerbianLatin")
        self.Language.addItem("")
        self.Language.setItemText(54, "SimpChinese")
        self.Language.addItem("")
        self.Language.setItemText(55, "Slovak")
        self.Language.addItem("")
        self.Language.setItemText(56, "Slovenian")
        self.Language.addItem("")
        self.Language.setItemText(57, "Spanish")
        self.Language.addItem("")
        self.Language.setItemText(58, "SpanishInternational")
        self.Language.addItem("")
        self.Language.setItemText(59, "Swahili")
        self.Language.addItem("")
        self.Language.setItemText(60, "Swedish")
        self.Language.addItem("")
        self.Language.setItemText(61, "Thai")
        self.Language.addItem("")
        self.Language.setItemText(62, "TradChinese")
        self.Language.addItem("")
        self.Language.setItemText(63, "Turkish")
        self.Language.addItem("")
        self.Language.setItemText(64, "Ukranian")
        self.Language.addItem("")
        self.Language.setItemText(65, "Uzbek")
        self.Language.addItem("")
        self.Language.setItemText(66, "Valencian")
        self.Language.addItem("")
        self.Language.setItemText(67, "Vietnamese")
        self.Language.addItem("")
        self.Language.setItemText(68, "Welsh")
        self.Language.addItem("")
        self.Language.setItemText(69, "Yoruba")
        self.formLayout_4.setWidget(6, QtGui.QFormLayout.FieldRole, self.Language)
        self.TrademarksLabel = QtGui.QLabel(self.DetailsGroupBox)
        self.TrademarksLabel.setObjectName("TrademarksLabel")
        self.formLayout_4.setWidget(7, QtGui.QFormLayout.LabelRole, self.TrademarksLabel)
        self.Trademarks = QtGui.QLineEdit(self.DetailsGroupBox)
        self.Trademarks.setMaxLength(512)
        self.Trademarks.setObjectName("Trademarks")
        self.formLayout_4.setWidget(7, QtGui.QFormLayout.FieldRole, self.Trademarks)
        self.verticalLayout.addWidget(self.DetailsGroupBox)
        self.VersionGroupBox = QtGui.QGroupBox(AppInfoDialog)
        self.VersionGroupBox.setObjectName("VersionGroupBox")
        self.formLayout = QtGui.QFormLayout(self.VersionGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.DisplayVersionLabel = QtGui.QLabel(self.VersionGroupBox)
        self.DisplayVersionLabel.setObjectName("DisplayVersionLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.DisplayVersionLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.DisplayVersionBase = QtGui.QLineEdit(self.VersionGroupBox)
        self.DisplayVersionBase.setMaxLength(20)
        self.DisplayVersionBase.setObjectName("DisplayVersionBase")
        self.horizontalLayout.addWidget(self.DisplayVersionBase)
        self.DisplayVersionType = QtGui.QComboBox(self.VersionGroupBox)
        self.DisplayVersionType.setObjectName("DisplayVersionType")
        self.DisplayVersionType.addItem("")
        self.DisplayVersionType.setItemText(0, "Development Test")
        self.DisplayVersionType.addItem("")
        self.DisplayVersionType.setItemText(1, "Pre-Release")
        self.DisplayVersionType.addItem("")
        self.DisplayVersionType.setItemText(2, "(official release)")
        self.DisplayVersionType.addItem("")
        self.DisplayVersionType.setItemText(3, "Revision")
        self.horizontalLayout.addWidget(self.DisplayVersionType)
        self.DisplayVersionNum = QtGui.QSpinBox(self.VersionGroupBox)
        self.DisplayVersionNum.setMinimum(1)
        self.DisplayVersionNum.setObjectName("DisplayVersionNum")
        self.horizontalLayout.addWidget(self.DisplayVersionNum)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.PackageVersionLabel = QtGui.QLabel(self.VersionGroupBox)
        self.PackageVersionLabel.setObjectName("PackageVersionLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.PackageVersionLabel)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.PackageVersion1 = QtGui.QSpinBox(self.VersionGroupBox)
        self.PackageVersion1.setMaximum(65535)
        self.PackageVersion1.setObjectName("PackageVersion1")
        self.horizontalLayout_2.addWidget(self.PackageVersion1)
        self.PackageVersionDot1 = QtGui.QLabel(self.VersionGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PackageVersionDot1.sizePolicy().hasHeightForWidth())
        self.PackageVersionDot1.setSizePolicy(sizePolicy)
        self.PackageVersionDot1.setObjectName("PackageVersionDot1")
        self.horizontalLayout_2.addWidget(self.PackageVersionDot1)
        self.PackageVersion2 = QtGui.QSpinBox(self.VersionGroupBox)
        self.PackageVersion2.setMaximum(65535)
        self.PackageVersion2.setObjectName("PackageVersion2")
        self.horizontalLayout_2.addWidget(self.PackageVersion2)
        self.PackageVersionDot2 = QtGui.QLabel(self.VersionGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PackageVersionDot2.sizePolicy().hasHeightForWidth())
        self.PackageVersionDot2.setSizePolicy(sizePolicy)
        self.PackageVersionDot2.setObjectName("PackageVersionDot2")
        self.horizontalLayout_2.addWidget(self.PackageVersionDot2)
        self.PackageVersion3 = QtGui.QSpinBox(self.VersionGroupBox)
        self.PackageVersion3.setMaximum(65535)
        self.PackageVersion3.setObjectName("PackageVersion3")
        self.horizontalLayout_2.addWidget(self.PackageVersion3)
        self.PackageVersionDot3 = QtGui.QLabel(self.VersionGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PackageVersionDot3.sizePolicy().hasHeightForWidth())
        self.PackageVersionDot3.setSizePolicy(sizePolicy)
        self.PackageVersionDot3.setObjectName("PackageVersionDot3")
        self.horizontalLayout_2.addWidget(self.PackageVersionDot3)
        self.PackageVersion4 = QtGui.QSpinBox(self.VersionGroupBox)
        self.PackageVersion4.setMaximum(65535)
        self.PackageVersion4.setObjectName("PackageVersion4")
        self.horizontalLayout_2.addWidget(self.PackageVersion4)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.VersionGroupBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.LicenseGroupBox = QtGui.QGroupBox(AppInfoDialog)
        self.LicenseGroupBox.setObjectName("LicenseGroupBox")
        self.formLayout_5 = QtGui.QFormLayout(self.LicenseGroupBox)
        self.formLayout_5.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_5.setObjectName("formLayout_5")
        self.Shareable = QtGui.QCheckBox(self.LicenseGroupBox)
        self.Shareable.setObjectName("Shareable")
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.Shareable)
        self.OpenSource = QtGui.QCheckBox(self.LicenseGroupBox)
        self.OpenSource.setObjectName("OpenSource")
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.LabelRole, self.OpenSource)
        self.Freeware = QtGui.QCheckBox(self.LicenseGroupBox)
        self.Freeware.setObjectName("Freeware")
        self.formLayout_5.setWidget(2, QtGui.QFormLayout.LabelRole, self.Freeware)
        self.CommercialUse = QtGui.QCheckBox(self.LicenseGroupBox)
        self.CommercialUse.setObjectName("CommercialUse")
        self.formLayout_5.setWidget(3, QtGui.QFormLayout.LabelRole, self.CommercialUse)
        self.verticalLayout_2.addWidget(self.LicenseGroupBox)
        self.AdvancedGroupBox = QtGui.QGroupBox(AppInfoDialog)
        self.AdvancedGroupBox.setObjectName("AdvancedGroupBox")
        self.formLayout_7 = QtGui.QFormLayout(self.AdvancedGroupBox)
        self.formLayout_7.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_7.setObjectName("formLayout_7")
        self.PluginsPathLabel = QtGui.QLabel(self.AdvancedGroupBox)
        self.PluginsPathLabel.setObjectName("PluginsPathLabel")
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.LabelRole, self.PluginsPathLabel)
        self.PluginsPath = QtGui.QLineEdit(self.AdvancedGroupBox)
        self.PluginsPath.setMaxLength(256)
        self.PluginsPath.setObjectName("PluginsPath")
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.FieldRole, self.PluginsPath)
        self.UsesDotNetVersionLabel = QtGui.QLabel(self.AdvancedGroupBox)
        self.UsesDotNetVersionLabel.setObjectName("UsesDotNetVersionLabel")
        self.formLayout_7.setWidget(2, QtGui.QFormLayout.LabelRole, self.UsesDotNetVersionLabel)
        self.UsesDotNetVersion = QtGui.QComboBox(self.AdvancedGroupBox)
        self.UsesDotNetVersion.setEditable(True)
        self.UsesDotNetVersion.setObjectName("UsesDotNetVersion")
        self.UsesDotNetVersion.addItem("")
        self.UsesDotNetVersion.setItemText(0, "None")
        self.UsesDotNetVersion.addItem("")
        self.UsesDotNetVersion.setItemText(1, "1.1")
        self.UsesDotNetVersion.addItem("")
        self.UsesDotNetVersion.setItemText(2, "2.0")
        self.UsesDotNetVersion.addItem("")
        self.UsesDotNetVersion.setItemText(3, "3.0")
        self.UsesDotNetVersion.addItem("")
        self.UsesDotNetVersion.setItemText(4, "3.5")
        self.UsesDotNetVersion.addItem("")
        self.UsesDotNetVersion.setItemText(5, "4.0")
        self.formLayout_7.setWidget(2, QtGui.QFormLayout.FieldRole, self.UsesDotNetVersion)
        self.UsesJava = QtGui.QCheckBox(self.AdvancedGroupBox)
        self.UsesJava.setObjectName("UsesJava")
        self.formLayout_7.setWidget(3, QtGui.QFormLayout.LabelRole, self.UsesJava)
        self.EULAVersionLabel = QtGui.QLabel(self.AdvancedGroupBox)
        self.EULAVersionLabel.setObjectName("EULAVersionLabel")
        self.formLayout_7.setWidget(4, QtGui.QFormLayout.LabelRole, self.EULAVersionLabel)
        self.EULAVersion = QtGui.QLineEdit(self.AdvancedGroupBox)
        self.EULAVersion.setMaxLength(128)
        self.EULAVersion.setObjectName("EULAVersion")
        self.formLayout_7.setWidget(4, QtGui.QFormLayout.FieldRole, self.EULAVersion)
        self.verticalLayout_2.addWidget(self.AdvancedGroupBox)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(AppInfoDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)
        self.NameLabel.setBuddy(self.Name)
        self.AppIDLabel.setBuddy(self.AppID)
        self.PublisherLabel.setBuddy(self.Publisher)
        self.HomepageLabel.setBuddy(self.Homepage)
        self.CategoryLabel.setBuddy(self.Category)
        self.DescriptionLabel.setBuddy(self.Description)
        self.LanguageLabel.setBuddy(self.Language)
        self.TrademarksLabel.setBuddy(self.Trademarks)
        self.DisplayVersionLabel.setBuddy(self.DisplayVersionBase)
        self.PackageVersionLabel.setBuddy(self.PackageVersion1)
        self.PluginsPathLabel.setBuddy(self.PluginsPath)
        self.UsesDotNetVersionLabel.setBuddy(self.UsesDotNetVersion)
        self.EULAVersionLabel.setBuddy(self.EULAVersion)

        self.retranslateUi(AppInfoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), AppInfoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), AppInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AppInfoDialog)

    def retranslateUi(self, AppInfoDialog):
        AppInfoDialog.setWindowTitle(QtGui.QApplication.translate("AppInfoDialog", "App details", None, QtGui.QApplication.UnicodeUTF8))
        self.DetailsGroupBox.setTitle(QtGui.QApplication.translate("AppInfoDialog", "App details", None, QtGui.QApplication.UnicodeUTF8))
        self.NameLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "Portable app &name", None, QtGui.QApplication.UnicodeUTF8))
        self.AppIDLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "&App ID", None, QtGui.QApplication.UnicodeUTF8))
        self.PublisherLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "&Publisher", None, QtGui.QApplication.UnicodeUTF8))
        self.HomepageLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "&Homepage", None, QtGui.QApplication.UnicodeUTF8))
        self.CategoryLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "Cate&gory", None, QtGui.QApplication.UnicodeUTF8))
        self.DescriptionLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "&Description", None, QtGui.QApplication.UnicodeUTF8))
        self.LanguageLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "&Language", None, QtGui.QApplication.UnicodeUTF8))
        self.TrademarksLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "&Trademarks", None, QtGui.QApplication.UnicodeUTF8))
        self.VersionGroupBox.setTitle(QtGui.QApplication.translate("AppInfoDialog", "Version", None, QtGui.QApplication.UnicodeUTF8))
        self.DisplayVersionLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "Display &version", None, QtGui.QApplication.UnicodeUTF8))
        self.PackageVersionLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "Pac&kage version", None, QtGui.QApplication.UnicodeUTF8))
        self.PackageVersionDot1.setText(QtGui.QApplication.translate("AppInfoDialog", ".", None, QtGui.QApplication.UnicodeUTF8))
        self.PackageVersionDot2.setText(QtGui.QApplication.translate("AppInfoDialog", ".", None, QtGui.QApplication.UnicodeUTF8))
        self.PackageVersionDot3.setText(QtGui.QApplication.translate("AppInfoDialog", ".", None, QtGui.QApplication.UnicodeUTF8))
        self.LicenseGroupBox.setTitle(QtGui.QApplication.translate("AppInfoDialog", "License", None, QtGui.QApplication.UnicodeUTF8))
        self.Shareable.setText(QtGui.QApplication.translate("AppInfoDialog", "Sharea&ble", None, QtGui.QApplication.UnicodeUTF8))
        self.OpenSource.setText(QtGui.QApplication.translate("AppInfoDialog", "Op&en source", None, QtGui.QApplication.UnicodeUTF8))
        self.Freeware.setText(QtGui.QApplication.translate("AppInfoDialog", "&Freeware", None, QtGui.QApplication.UnicodeUTF8))
        self.CommercialUse.setText(QtGui.QApplication.translate("AppInfoDialog", "Co&mmercial use", None, QtGui.QApplication.UnicodeUTF8))
        self.AdvancedGroupBox.setTitle(QtGui.QApplication.translate("AppInfoDialog", "Advanced", None, QtGui.QApplication.UnicodeUTF8))
        self.PluginsPathLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "P&lugins path", None, QtGui.QApplication.UnicodeUTF8))
        self.UsesDotNetVersionLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "&Requires .NET version", None, QtGui.QApplication.UnicodeUTF8))
        self.UsesJava.setText(QtGui.QApplication.translate("AppInfoDialog", "Uses &Java", None, QtGui.QApplication.UnicodeUTF8))
        self.EULAVersionLabel.setText(QtGui.QApplication.translate("AppInfoDialog", "E&ULA version", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
