import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit, QSizePolicy
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QMessageBox, QComboBox
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt
from tmpeconfig import LANGUAGES, HELPLABELS

def get_version_number(filename):
   info = GetFileVersionInfo (filename, "\\")
   ms = info['FileVersionMS']
   ls = info['FileVersionLS']
   return "%d.%d.%d.%d" % (HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls))

def get_version_info(filename):
    pe = PE(filename)
    if 'VS_FIXEDFILEINFO' not in pe.__dict__:
        print("ERROR: Oops, %s has no version info. Can't continue." % (filename))
        return
    if not pe.VS_FIXEDFILEINFO:
        print("ERROR: VS_FIXEDFILEINFO field not set for %s. Can't continue." % (filename))
        return
    verinfo = pe.VS_FIXEDFILEINFO
    prodver = (verinfo[0].ProductVersionMS >> 16, verinfo[0].ProductVersionMS & 0xFFFF, verinfo[0].ProductVersionLS >> 16, verinfo[0].ProductVersionLS & 0xFFFF)
    # print("Product version: %d.%d.%d.%d" % prodver)
    return "%d.%d.%d.%d" % prodver

try:
    from win32api import GetFileVersionInfo, LOWORD, HIWORD  # type: ignore
    get_version_info = get_version_number
except ImportError:
    print('No win32 API! Tryping pefile...')
    from pefile import PE


class VersionTooOld(Exception):
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TMPE Config Editor")
        self.setMinimumSize(800, 600)

        # Center the window on the screen
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

        # Set the window icon
        self.setWindowIcon(QIcon("TMPEConfig.png"))  # Replace with your icon path

        font_bold = QFont("Arial", 14, QFont.Bold)

        # Create the tab widget
        self.tab_widget = QTabWidget()

        # Create the tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        self.tab8 = QWidget()

        # self.tab_widget.addTab(QWidget(), "a")

        # Add the tabs to the tab widget
        self.tab_widget.addTab(self.tab1, "General")
        self.tab_widget.addTab(self.tab2, "Gameplay")
        self.tab_widget.addTab(self.tab3, "Policies")
        self.tab_widget.addTab(self.tab4, "Overlays")
        self.tab_widget.addTab(self.tab5, "Maintenance")
        self.tab_widget.addTab(self.tab6, "Keybinds")
        self.tab_widget.addTab(self.tab7, "ConfigFile")
        self.tab_widget.addTab(self.tab8, "About")

        # Get language from XML
        lang = xml.xpath('//GlobalConfig/LanguageCode')
        vers = xml.xpath('//GlobalConfig/Version')

        # Set up content for Tab 1 - General
        self.tab1_layout = QVBoxLayout()
        self.tab1_layout.setAlignment(Qt.AlignTop)
        self.tab1_label_title = QLabel("General Settings")
        self.tab1_label_title.setFont(font_bold)
        self.tab1_layout.addWidget(self.tab1_label_title)
        self.tab1_label = QLabel(HELPLABELS["General"])
        self.tab1_layout.addWidget(self.tab1_label)

        self.tab1_label_vers = QLabel("Version")
        self.tab1_layout.addWidget(self.tab1_label_vers)

        self.tab1_label_vers = QLabel(vers[0].text)
        self.tab1_layout.addWidget(self.tab1_label_vers)

        self.tab1_label_lang = QLabel("Language")
        self.tab1_layout.addWidget(self.tab1_label_lang)

        # Create the dropdown (QComboBox)
        dropdown = QComboBox()

        # Add items to the dropdown
        dropdown.addItems(list(LANGUAGES.values()))

        # Set item text
        index = dropdown.findText(LANGUAGES[lang[0].text])
        dropdown.setCurrentIndex(index)

        # Add the dropdown to a layout
        self.tab1_layout.addWidget(dropdown)
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        dropdown.setSizePolicy(size_policy)
        # self.tab1_layout.addSpacing(100)

        self.tab1.setLayout(self.tab1_layout)

        # Set up content for Tab 2 - Gameplay
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.setAlignment(Qt.AlignTop)
        self.tab2_label_title = QLabel("Gameplay Settings")
        self.tab2_label_title.setFont(font_bold)
        self.tab2_layout.addWidget(self.tab2_label_title)
        self.tab2_label = QLabel(HELPLABELS["Gameplay"])
        self.tab2_layout.addWidget(self.tab2_label)
        self.tab2.setLayout(self.tab2_layout)

        # Set up content for Tab 3 - Policies
        self.tab3_layout = QVBoxLayout()
        self.tab3_layout.setAlignment(Qt.AlignTop)
        self.tab3_label_title = QLabel("Policy Settings")
        self.tab3_label_title.setFont(font_bold)
        self.tab3_layout.addWidget(self.tab3_label_title)
        self.tab3_label = QLabel(HELPLABELS["Policies"])
        self.tab3_layout.addWidget(self.tab3_label)
        self.tab3.setLayout(self.tab3_layout)

        # Set up content for Tab 4 - Overlays
        self.tab4_layout = QVBoxLayout()
        self.tab4_layout.setAlignment(Qt.AlignTop)
        self.tab4_label_title = QLabel("Overlay Settings")
        self.tab4_label_title.setFont(font_bold)
        self.tab4_layout.addWidget(self.tab4_label_title)
        self.tab4_label = QLabel(HELPLABELS["Overlays"])
        self.tab4_layout.addWidget(self.tab4_label)
        self.tab4.setLayout(self.tab4_layout)

        # Set up content for Tab 5 - Maintenance
        self.tab5_layout = QVBoxLayout()
        self.tab5_layout.setAlignment(Qt.AlignTop)
        self.tab5_label_title = QLabel("Maintenance Settings")
        self.tab5_label_title.setFont(font_bold)
        self.tab5_layout.addWidget(self.tab5_label_title)
        self.tab5_label = QLabel(HELPLABELS["Maintenance"])
        self.tab5_layout.addWidget(self.tab5_label)
        self.tab5.setLayout(self.tab5_layout)

        # Set up content for Tab 6 - Keybinds
        self.tab6_layout = QVBoxLayout()
        self.tab6_layout.setAlignment(Qt.AlignTop)
        self.tab6_label_title = QLabel("Keybindings Settings")
        self.tab6_label_title.setFont(font_bold)
        self.tab6_layout.addWidget(self.tab6_label_title)
        self.tab6_label = QLabel(HELPLABELS["Keybinds"])
        self.tab6_layout.addWidget(self.tab6_label)
        self.tab6.setLayout(self.tab6_layout)

        # Set up content for Tab 7 - XML
        self.tab7_layout = QVBoxLayout()
        self.tab7_label = QTextEdit()
        self.tab7_label.setPlainText(read_file('TMPE_GlobalConfig.xml'))
        self.tab7_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tab7_layout.addWidget(self.tab7_label)
        self.tab7.setLayout(self.tab7_layout)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()
        
        # Create the Reload and Save buttons
        reload_button = QPushButton("Reload")
        save_button = QPushButton("Save")

        # Connect buttons to their respective slot functions
        reload_button.clicked.connect(self.reload_action)
        save_button.clicked.connect(self.save_action)

        # Add buttons to the horizontal layout
        button_layout.addWidget(reload_button)
        button_layout.addWidget(save_button)

        # Add the button layout to the main tab layout
        self.tab7_layout.addLayout(button_layout)
        
        # Set up content for Tab 8
        self.tab8_layout = QVBoxLayout()
        self.tab8_layout.setAlignment(Qt.AlignTop)

        self.tab8_label_title = QLabel("About this program")
        self.tab8_label_title.setFont(font_bold)
        self.tab8_layout.addWidget(self.tab8_label_title)

        self.tab8_label = QLabel("TMPE Config Editor\nCopyright 2024, Michael John <michael.john@gmx.at>\n" + \
            read_file(os.path.join(os.path.dirname(__file__), "LICENSE")) + \
            "\n" + "TMPE version: " + get_version_info(full_path))
        self.tab8_layout.addWidget(self.tab8_label)

        # Load the icon as a QPixmap and set it in a QLabel
        icon_label = QLabel()
        icon_pixmap = QPixmap("TMPEConfig.png")  # Replace with your icon path
        icon_pixmap = icon_pixmap.scaled(128, 128)
        icon_label.setPixmap(icon_pixmap)

        # Add the icon and text to the layout
        self.tab8_layout.addWidget(icon_label)
        # self.tab8_layout.addWidget(self.tab8_label)
        self.tab8.setLayout(self.tab8_layout)

        # Set the central widget of the main window to be the tab widget
        self.setCentralWidget(self.tab_widget)

    # Slot function for the Reload button
    def reload_action(self):
        QMessageBox.information(self, "Reload", "Configuration has been reloaded.")

    # Slot function for the Save button
    def save_action(self):
        QMessageBox.information(self, "Save", "Configuration has been saved.")


try:
    from lxml import etree as ET
    print("Running with lxml.etree")
except ImportError:
    import xml.etree.ElementTree as ET  # etree
    print("Running with Python's xml.etree.ElementTree")


def read_file(filename):
    with open(filename, "r") as xmlfile:
        return xmlfile.read()

def load_xml(filename: str, debug: bool = False):
    if os.environ.get("TMPE_DEBUG") == 1:
        debug = True

    # import xml.etree.ElementTree as ET
    tree = ET.parse(filename) # TMPE_GlobalConfig_v17.xml
    encoding = tree.docinfo.encoding
    if debug:
        print(f'{encoding = }')
    root = tree.getroot()
    for child in root:
        if debug:
            print(child.tag, child.text.strip())
        if 'Version' in child.tag and child.text != '20':
            raise VersionTooOld('The version of the config file is too old!')
        for subchild in child:
            if debug:
                print('\t' + subchild.tag, subchild.text.strip() if subchild.text is not None else subchild.text)
            for subsubchild in subchild:
                if debug:
                    print('\t\t' + subsubchild.tag, subsubchild.text)

    # for neighbor in root.iter('neighbor'):
    #     print(neighbor.attrib)

    lang = root.xpath('//GlobalConfig/LanguageCode')
    lang[0].text = "de"

    # Converting the xml data to byte object,
    # for allowing flushing data to file 
    # stream
    # b_xml = ET.tostring(root)

    # Opening a file under the name `items2.xml`,
    # with operation mode `wb` (write + binary)
    # with open("TMPE_GlobalConfig2.xml", "wb") as f:
    #     f.write(b_xml)

    # tree.write("TMPE_GlobalConfig.xml", xml_declaration=True, encoding='UTF-8')
    return root


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if os.environ.get("TMPE_STEAM"):
        steam_root = os.environ.get("TMPE_STEAM")
    else:
        if sys.platform == "linux":
            # steam_root = r"/steam1/SteamLibrary"
            steam_root = os.path.expanduser("~/.local/share/Steam")
        elif sys.platform == "win32":
            steam_root = r"C:\Program Files (x86)\Steam"
        else:
            print("Could not determine platform, exiting.")
            sys.exit(-1)

    if os.path.exists(steam_root):
        tmpe_dir = "steamapps/workshop/content/255710/1637663252/TrafficManager.dll"
        full_path = os.path.join(steam_root, tmpe_dir)
    else:
        print("Could not determine Steam root, exiting.")
        sys.exit(-1)

    print(f"Checking {full_path}...")
    if os.path.exists(full_path):
        print("TMPE version: ", get_version_info(full_path))
        xml = load_xml('TMPE_GlobalConfig.xml')
    else:
        print(r"Could not determine TMPE installation, exiting.")
        print(r"Set TMPE_STEAM environment variable for an alternative location,")
        print(r"ie. TMPE_STEAM=/steam1/SteamLibrary or TMPE_STEAM=E:\SteamLibrary")
        sys.exit(-1)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
