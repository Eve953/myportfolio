import tkinter
from PIL import Image
from customtkinter import *
from transformers import pipeline
import torch
from autocorrect import Speller
from fpdf import FPDF


# gui creation 
root = CTk()                    

# app format
root.geometry("600x650")
set_appearance_mode("dark")

# label format
label = CTkLabel(root, 
                 text="Enter Your Text Here:", 
                 fg_color="transparent", 
                 font = ("Lexend", 27, 'bold'))
label.pack(pady = 15)

# textbox for the summary that the user types in 
text = CTkTextbox(master=root,
                   border_color="#6FC276",
                     border_width=1.5, height = 480, 
                     width = 400, wrap="word", 
                     scrollbar_button_color = "#87CDF6", 
                     corner_radius=25)

text.pack(pady = 15)

# summarize function
def summarize():
    new_window = CTkToplevel(root)
    new_window.minsize(500, 630)
    sum_label = CTkLabel(new_window, 
                         text="Here is your summary:", 
                         fg_color="transparent", 
                         font = ("Lexend", 27, 'bold'))
    sum_label.pack(pady=15)

    user_input=text.get("1.0","end-1c")
    

    # hugging face model
    summary = pipeline("summarization", model="facebook/bart-large-cnn")
    txt = summary(user_input, max_length=120, min_length=25, do_sample=False)
    final_summary = txt[0]['summary_text']

    

    summary_box = CTkTextbox(master=new_window, 
                             border_color="#6FC276", 
                             border_width=1.5, 
                             height = 480, width = 400, 
                             wrap="word", 
                             scrollbar_button_color = "#87CDF6", 
                             corner_radius=25)
    
    # autocorrect the summary
    spelling = Speller(lang='en')
    autocorrected_text = spelling(final_summary)
    summary_box.insert("1.0", autocorrected_text)
    summary_box.pack(pady = 15)

    # function to export as pdf
    def toggle_box(c):
        if(c == "PDF"):
            
            summary_pdf = FPDF(orientation='P', unit='mm', format='letter')
            summary_pdf.set_font("Times", size = 15)
            summary_pdf.add_page()
            summary_pdf.multi_cell(0, 18, autocorrected_text)
            summary_pdf.output("summary.pdf")

        elif(c == 'text file'):

            with open('summary.txt', 'a') as f:
                f.write(autocorrected_text)

    # option to export the summary as text file or pdf checkbox
    var = StringVar(value="Export as...")
    export_combobox = CTkComboBox(new_window, 
                                  values=["PDF", "text file"], 
                                  variable=var, 
                                  border_color ="#6FC276", 
                                  dropdown_hover_color = "#0000CD", 
                                  command = toggle_box)
    
    export_combobox.pack(pady=15)

    new_window.grab_set()


# summary button
button = CTkButton(root,
                    text="Summarize", 
                    font = ("Lexend", 18, 'bold'), 
                    fg_color = "#0082cb", 
                    border_color="#6FC276", 
                    border_width=2, 
                    height=35, 
                    corner_radius=25, 
                    hover_color = "#87CDF6", 
                    command=summarize)

button.pack(pady=15)

# settings image
icon = CTkImage(dark_image=Image.open("gear_icon.png"))

# settings function
def settings_functions():

    # we go to the settings window
    settings_window=CTkToplevel(root)
    settings_window.minsize(500,580)
    slabel = CTkLabel(settings_window,
                       text="System Settings", 
                       fg_color="transparent", 
                       font = ("Lexend", 27, 'bold'))
    slabel.pack(pady=15)
    settings_window.grab_set()

    # function for lighting 
    def toggle_lighting():
        if(button_val.get() == 1):
            set_appearance_mode("light")
        elif(button_val.get() == 2):
            set_appearance_mode("dark")

    

    # label for lighting
    light_label = CTkLabel(settings_window,
                            text = "lighting options:", 
                            fg_color = "transparent", 
                            font =("Lexend", 20),
                            text_color="#6FC276")
    
    light_label.place(relx=0.02, rely=0.13, anchor="nw")


    # lighting options
    button_val = tkinter.IntVar(value=0)

    light_mode = CTkRadioButton(settings_window,
                                 text="light mode",
                                 variable= button_val,
                                 value=1,
                                font = ("Lexend", 20),
                                  fg_color="#6FC276",
                                  command=toggle_lighting)
    light_mode.pack(pady=15)

    dark_mode = CTkRadioButton(settings_window,
                                 text="dark mode",
                                 variable= button_val,
                                 value=2,
                                 font = ("Lexend", 20),
                                  fg_color = "#6FC276",
                                  command=toggle_lighting)
    
    dark_mode.pack(pady=7)

# settings button 
settings = CTkButton(root, 
                     corner_radius=25, 
                     fg_color = "#0082cb", 
                     width=4, 
                     height=40, 
                     border_color="#6FC276", 
                     border_width=2, 
                     image=icon,
                     text="",
                     hover_color = "#87CDF6", command=settings_functions)

settings.place(relx=0.01, rely=0.96, anchor="sw")

root.mainloop()