from Pages.mainPage import MainPage
from Pages.settingsPage import SettingsPage

class PageManager:
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        self.main_page = MainPage(parent, theme, self)
        self.settings_page = SettingsPage(parent, theme, self)
        self.current_page = self.main_page
        self.show_page(self.current_page)

    def change_page(self, page):
        if page == 'mainPage':
            self.show_page(self.main_page)
        elif page == 'settingsPage':
            self.show_page(self.settings_page)

    def show_page(self, page):
        if self.current_page:
            self.current_page.hide()
        self.current_page = page
        self.current_page.show()