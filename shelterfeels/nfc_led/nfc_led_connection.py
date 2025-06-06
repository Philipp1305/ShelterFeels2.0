from shelterfeels.nfc_led.nfc import read_emotion_from_nfc
from shelterfeels.nfc_led.neo_pixel import (
    fill_circle,
    turn_off,
    upload_day_state,
    load_state_file,
)
from shelterfeels.nfc_led.config import daynum_to_day
from datetime import datetime
from shelterfeels.database.db import insert_emotion


def read_nfc_and_change_led(*args):
    """s
    Read nfc and adds new color to the circle
    """
    if args:
        word = args[0]
        print(f"Received word: {word}")  # zur Kontrolle
    else:
        word = None

    weekday = str(datetime.today().weekday())
    day = daynum_to_day[weekday]
    colors = load_state_file()[weekday]
    emotion = read_emotion_from_nfc()
    print(emotion)
    insert_emotion(emotion, word)
    colors.append(emotion.value)
    print(colors)
    fill_circle(day, colors)
    upload_day_state(weekday, colors)
    pass  # funky.next() in the end.


if __name__ == "__main__":
    read_nfc_and_change_led("testemotion")
    for i in range(5):
        read_nfc_and_change_led()
    turn_off()
