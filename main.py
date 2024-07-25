from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
COUNT = 5
TURN_ON_TIMER = True
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv", encoding="utf-8")
except FileNotFoundError:
    original_data = pandas.read_csv("data/hiragana.csv", encoding="utf-8")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

# Timer become more than one and works independently to each other whenever known or unknown button clicked
# It will be best to wait clock timer ends -> flip card -> known or unknown button pressed
# When clock timer is still ongoing, clicking known or unknown button do not make previous clock timer ends!
def next_card():
    global current_card, flip_timer
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Hiragana", fill="black")
    canvas.itemconfig(card_word, text=current_card["Hiragana"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    # Disabling clock_timer enabled to not flip_card entirely
    clock_timer()
    
def flip_card():
    canvas.itemconfig(timer_clock, text="", state="disabled")
    canvas.itemconfig(card_title, text="Meaning", fill="white")
    canvas.itemconfig(card_word, text=current_card["Meaning"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def clock_timer():
    global flip_timer
    count = COUNT
    while count > 0:
        canvas.itemconfig(timer_clock, text=f"Remaining time: {count}s", state="normal")
        window.update()
        flip_timer = window.after(1000)
        count -= 1
    canvas.itemconfig(timer_clock, text="")
    flip_card()

def is_known():
    canvas.itemconfig(timer_clock, text="")
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False, encoding="utf-8")
    next_card()

def start_game():
    start_button.place_forget()
    canvas.grid(row=0, column=0, columnspan=2)
    unknown_button.grid(row=1, column=0)
    known_button.grid(row=1, column=1)
    finish_button.grid(row=2, column=0, columnspan=2)
    next_card()

def finish_game():
    try: 
        data_num = len(pandas.read_csv("data/words_to_learn.csv"))
    except FileNotFoundError:
        data_num = 0
    finally:
        source_num = len(pandas.read_csv("data/hiragana.csv"))
        canvas.itemconfig(card_title, text=f"Congratulations!\nYou learned {source_num-data_num} words", fill="black")
        canvas.itemconfig(card_word, text="Try again?", fill="black")
        canvas.itemconfig(card_background, image=card_front_img)

window = Tk()
window.title("Flash Card Program")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
canvas = Canvas(width=800, height=550)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Let's Learn Basic Hiragana\nwith Flash Card\n", font=("Ariel", 40, "italic"), justify="center")
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
timer_clock = canvas.create_text(150, 30, text="", font=("Arial", 20, "bold")) # Timer to show remaining time left

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Button that hidden after start game clicked
start_button = Button(text="Start Game", font=("Arial", 40, "bold"), command=start_game, highlightthickness=0)
start_button.place(x=225, y=220)

# Button that shown after start game clicked
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)

finish_button = Button(text="EXIT GAME", command=finish_game, highlightthickness=0, font=("Arial", 12, "bold"))

window.mainloop()
