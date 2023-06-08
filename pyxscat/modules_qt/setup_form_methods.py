
from modules_qt.gui_widget_setup import GUIPyX_Widget_setupform
from modules_qt import lineedit_methods as le
from modules_qt import listwidget_methods as lt
from os.path import join
from pyxscat.decorators import try_or_continue
from pyxscat.setup_methods import DIRECTORY_SETUPS
import os

class SetUpForm(GUIPyX_Widget_setupform):

    def __init__(self):
        super(SetUpForm, self).__init__()
        self.init_callbacks()
        self.update_setup_dictionaries()

    def init_callbacks(self):
        """
            Activate the callbacks regarding the integration form
        """
        self.list_setups.clicked.connect(
            lambda: self.activate_setup_form(
                name_dict=lt.click_values(
                    listwidget=self.list_setups
                )[0]
            )
        )

        # Callback for add a new set-up form
        self.button_input_setup.clicked.connect(
            lambda: self.add_new_setup(
                dict_setup=self.get_setup_attributes()
            )
        )


    def get_setup_attributes(self) -> dict:
        """
            Return a dictinary with all the attributes for the creation of a new setup
        """
        return {
            'Name':le.text(self.lineedit_setup),
            'Angle':le.text(self.lineedit_incidentangle),
            'Tilt angle':le.text(self.lineedit_tiltangle),
            'Norm':le.text(self.lineedit_normfactor),
            'Exposure':le.text(self.lineedit_exposure),
        }

    @try_or_continue('')
    def add_new_setup(self, dict_setup=dict()):
        """
            Introduce a new setup option if the values are valid
        """
        import json
        with open(join(DIRECTORY_SETUPS, f"{dict_setup['Name']}.json"), 'w+') as fp:
            json.dump(dict_setup, fp)
        
        self.update_setup_dictionaries()

    def activate_setup_form(self, name_dict=str()):
        """
            Updates the setup form with a dictionary       
        """
        import json
        with open(join(DIRECTORY_SETUPS, f"{name_dict}.json"), 'r') as fp:
            dict_integration = json.load(fp)

        # Feed each combobox with their respective dictionaries
        le.substitute(
            lineedit=self.lineedit_setup,
            new_text=dict_integration['Name'],
        )

        le.substitute(
            lineedit=self.lineedit_exposure,
            new_text=dict_integration['Exposure'],
        )

        le.substitute(
            lineedit=self.lineedit_normfactor,
            new_text=dict_integration['Norm'],
        )

        le.substitute(
            lineedit=self.lineedit_incidentangle,
            new_text=dict_integration['Angle'],
        )

        le.substitute(
            lineedit=self.lineedit_tiltangle,
            new_text=dict_integration['Tilt angle'],
        )

    def update_setup_dictionaries(self):
        """
            Feed the list_widget with all the available setup dictionaries
        """
        import json
        list_dicts = []
        for file in os.listdir(DIRECTORY_SETUPS):
            if file.endswith('json'):
                with open(join(DIRECTORY_SETUPS, file), 'r') as fp:
                    list_dicts.append(
                        json.load(fp)
                    )

        # Feed each combobox with their respective dictionaries
        lt.insert_list(
            listwidget=self.list_setups,
            item_list=[
                d['Name'] for d in list_dicts
            ],
            reset=True,
        )

    def get_dictionaries_setup(self) -> list:
        """
            Return a list with the dictionaries of all the available setups
        """
        import json
        list_dicts = []
        for file in os.listdir(DIRECTORY_SETUPS):
            if file.endswith('json'):
                with open(join(DIRECTORY_SETUPS, file), 'r') as fp:
                    list_dicts.append(
                        json.load(fp)
                    )
        return list_dicts

    def get_dict_setup(self, name=str()) -> dict:
        """
            Return a dictionary of setup giving a name
        """
        for d in self.get_dictionaries_setup():
            if name == d['Name']:
                return d
        return