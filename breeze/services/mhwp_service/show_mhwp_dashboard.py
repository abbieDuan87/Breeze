from breeze.utils.cli_utils import show_disabled_account_dashboard_menu
from breeze.utils.cli_utils import clear_screen
from breeze.utils.constants import MHWP_BANNER_STRING

def show_mhwp_dashboard(user, mhwp_service):


    while True:
        clear_screen()
        print(MHWP_BANNER_STRING)

        if user.get_is_disabled():

            return show_disabled_account_dashboard_menu(user.get_username())

        print(f"Hi {user.get_username()}!")
        print("What do you want to do today?")
        print("[C] View Calendar of Appointments")
        print("[M] Manage Appointments (Confirm or Cancel)")
        print("[A] Add Patient Information (Condition, Notes)")
        print("[D] Display Patient Summary with Mood Chart")
        print("[E] Edit Personal Information")
        print("[X] Log out")

        user_input = input("> ").strip().lower()

        if user_input in ["c", "m", "a", "d", "e", "x"]:
            match user_input:
                case "c":
                    mhwp_service.view_calendar(user)
                case "m":
                    mhwp_service.manage_appointments(user)
                case "a":
                    mhwp_service.add_patient_information(user)
                case "d":
                    mhwp_service.display_patient_summary(user)
                case "e":
                    mhwp_service.edit_personal_information(user)
                case "x":
                    return True