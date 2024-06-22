from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"
#----- Flash Card -----#
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def known_words():
    to_learn.remove(current_card)
    canvas.itemconfig(timer_clock, text="")
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

def next_card():
    global current_card, one_second, count
    current_card = random.choice(to_learn)
    count = 5
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=f"{current_card['French']}", fill="black")
    canvas.itemconfig(timer_clock, text=f"Remaining time: {count}s")
    while count != 0:
        one_second = root.after(1000)
        count -= 1
        canvas.itemconfig(timer_clock, text=f"Remaining time: {count}s")
        root.update()
        if count==0:
            flip_card()
    
def flip_card():
    canvas.itemconfig(timer_clock, text="")
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=f"{current_card['English']}", fill="white")
    root.update()

def finish_game():
    global count
    count = None
    source_num = len(pandas.read_csv("data/french_words.csv"))
    data_num = len(pandas.read_csv("data/words_to_learn.csv"))
    cross_button.grid_forget()
    check_button.grid_forget()
    finish_button.grid_forget()
    canvas.itemconfig(card_title, text=f"Congratulations!\nYou learned {source_num-data_num} words")
    canvas.itemconfig(card_word, text="Try again?")
    canvas.itemconfig(timer_clock, text="")
    canvas.itemconfig(canvas_image, image=card_front)
    start_button.place(x=225, y=350)

def start_game():
    start_button.place_forget()
    canvas.grid(row=0, column=0, columnspan=2)
    cross_button.grid(row=1, column=0)
    check_button.grid(row=1, column=1)
    finish_button.grid(row=2, column=0, columnspan=2)
    next_card()

#----- UI SETUP -----#
root = Tk()
root.title("Flash Card Fr-En")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR, width=900, height=750)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
timer_clock = canvas.create_text(150, 30, text="", font=("Arial", 20, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
cross_button = Button(image=wrong_img, command=next_card, highlightthickness=0)

right_img = PhotoImage(file="images/right.png")
check_button = Button(image=right_img, command=known_words, highlightthickness=0)

start_button = Button(text="Start Game", font=("Arial", 40, "bold"), command=start_game, highlightthickness=0)
start_button.place(x=225, y=200)

finish_button = Button(text="EXIT GAME", command=finish_game, highlightthickness=0, font=("Arial", 12, "bold"))

root.mainloop()
