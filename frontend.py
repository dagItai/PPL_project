import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

kivy.require('1.9.1')


def show_warning_popup(text):
    '''
    Responsible for create and preform the pop window for error message
    :param text: which text should appear on the popup
    '''
    layout = GridLayout(cols=1, rows=2, padding=5)
    popupLabel = Label(text=text, padding=(50, 50), halign="center", valign="middle", size_hint=(1.0, 1.0))
    closeButton = Button(text="Close me!")
    layout.add_widget(popupLabel)
    layout.add_widget(closeButton)
    # Instantiate the modal popup and display
    popup = Popup(title='Warning',
                  content=layout, size_hint=(None, None), size=(280, 170))
    popup.open()
    # Attach close button press with popup.dismiss action
    closeButton.bind(on_press=popup.dismiss)


def show_recommendation_popup(rec_list):
    '''
    Responsible for create and preform the pop window for error message
    :param rec_list: list of end station recommendations
    '''
    layout = GridLayout(cols=1, rows=2, padding=10)
    if len(rec_list) == 0:
        text = "Sorry, no locations \nwere found"
    else:
        text = '\n'.join(rec_list)
    popupLabel = Label(text=text, halign="center", valign="middle", size_hint=(1.0, 1.0), padding=(5, 5))
    anchorLayout = AnchorLayout(size_hint_y=None, height=50)
    closeButton = Button(text="Close me!", height=20)
    anchorLayout.add_widget(closeButton)
    layout.add_widget(popupLabel)
    layout.add_widget(anchorLayout)
    # Instantiate the modal popup and display
    popup = Popup(title='Recommended Locations',
                  content=layout, size_hint=(None, None), size=(200, 320))
    popup.open()
    # Attach close button press with popup.dismiss action
    closeButton.bind(on_press=popup.dismiss)


def check_not_empty(start_location, trip_duration, recommendations_no):
    '''
    Checks that the user insert value in all the inputs box in the GUI
    :param start_location: start location input
    :param trip_duration: trip duration input
    :param recommendations_no: recommendation number input
    :return: False if one or more from the inputs box is empty, True otherwise
    '''
    if start_location == '':
        show_warning_popup("Please insert start location")
        return False
    if trip_duration == '':
        show_warning_popup("Please insert trip duration")
        return False
    if recommendations_no == '':
        show_warning_popup("Please insert recommendations number")
        return False
    return True


def RepresentsInt(s):
    '''
    Checks that the given parameter is int type
    :param s:
    :return:
    '''
    try:
        int(s)
        return True
    except ValueError:
        return False


class MainScreen(GridLayout):

    def check_start_location(self, start_location):
        '''
        Check that the parameter 'trip duration' that have been set by the user is valid
        :param start_location: start location name
        :return: False if the start location doesn't exists in db, otherwise True
        '''
        if not self.myDB.check_if_station_exists(start_location):
            show_warning_popup("Sorry, we are not supporting \nthe start location you've inserted")
            return False
        return True

    def check_trip_duration(self, trip_duration):
        '''
        Check that the parameter 'trip duration' that have been set by the user is valid
        :param trip_duration: trip duration (minutes)
        :return: False if the parameter is bigger that 337670 (the biggest number in the db) or it isn't form int type, otherwise True
        '''
        if not RepresentsInt(trip_duration) or int(trip_duration) > 337670:
            show_warning_popup("Trip duration must be integer \nnumber and not bigger than 337670")
            return False
        return True

    def check_recommendations_no(self, recommendations_no):
        '''
        Check that the parameter 'number of recommendation' that have been set by the user is valid
        :param recommendations_no: number of recommendation
        :return: False if the parameter is bigger that 10 or it isn't form int type, otherwise True
        '''
        if not RepresentsInt(recommendations_no) or int(recommendations_no) > 10:
            show_warning_popup("Number of locations must be integer \nnumber and not bigger than 10")
            return False
        return True

    def fetch_input(self):
        '''
        Responsible for get the parameter that the user have been set in the GUI
        :return: 3 parameter that the user set: start_location, trip_duration, recommendations_no
        '''
        start_location = self.ids.startLoc.text.strip()
        trip_duration = self.ids.tripDur.text.strip()
        recommendations_no = self.ids.recNo.text.strip()
        return start_location, trip_duration, recommendations_no.strip()

    def recommend_me(self):
        '''
        The main function which run the all process
        :return: status
        '''
        # Get the inputs from the GUI
        start_location, trip_duration, recommendations_no = self.fetch_input()
        if not check_not_empty(start_location, trip_duration, recommendations_no):
            return
        # Check the values
        if not (self.check_trip_duration(
                trip_duration) and self.check_recommendations_no(recommendations_no) and self.check_start_location(start_location)):
            return
        # Send the given parameter to the the backend
        recommendations_list = self.myDB.get_recommended_trip(start_location, int(trip_duration),
                                                              int(recommendations_no))
        show_recommendation_popup(recommendations_list)


class MyApp(App):
    def build(self):
        main_screen = MainScreen()
        main_screen.myDB = mybackend.Database()
        return main_screen


kv = MyApp()
Window.size = (470, 700)
kv.run()
