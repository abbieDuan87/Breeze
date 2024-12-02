from breeze.utils.cli_utils import clear_screen_and_show_banner, direct_to_dashboard
from breeze.utils.constants import MHWP_BANNER_STRING

def view_calendar(user):
    clear_screen_and_show_banner(MHWP_BANNER_STRING)
    user.display_calendar()
    print()
    direct_to_dashboard()