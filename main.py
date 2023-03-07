from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
# global variable
current_card = {}
to_learn = {}
# handling the FileNotFoundError
try:

    # reading the csv file from the
    # original database of french_words.csv
    # data = pandas.read_csv("data/french_words.csv")

    # now reading from words_to_learn instead
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    # then the original data
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="record")
# if the program has run before
else:

    # print(data)
    # using orient attribute in pandaDataframe
    to_learn = data.to_dict(orient="records")

current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    # accessing the key: "French"
    # print(current_card["French"])
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=front_card_image)
    # to repeat after the next card
    # wait for 3s to flip the card
    flip_timer = window.after(3000, func=flip_card)


# function to show the English Translation
# when the card or windows flips
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_card_image)


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    # using pandas to create a new dataframe
    data = pandas.DataFrame(to_learn)
    # save the file as a csv file
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("French Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# to flip the card after 3s, after(self, seconds, function)
flip_timer = window.after(3000, func=flip_card)

# canvas widget
canvas = Canvas(width=800, height=526)
front_card_image = PhotoImage(file="images/card_front.png")
back_card_image = PhotoImage(file="images/card_back.png")
# create_image(self, args, kw)
card_background = canvas.create_image(400, 263, image=front_card_image)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))

# text of the actual word
# center the canvas Text
# Half the canvas width and height

card_word = canvas.create_text(400, 263, text="", font=("Arial", 40, "italic"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
# layout the wrong button
# for the wrong button to show-up using the grid
unknown_button.grid(row=1, column=0)

# check mark for the flash card
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()
