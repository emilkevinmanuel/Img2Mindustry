from tkinter import filedialog
import customtkinter, tkinter
import pyperclip
from PIL import Image, ImageTk
from collections import Counter
import PIL

from more_itertools import locate

newline = "\r\n"

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("400x240")
app.iconbitmap("icon.ico")

app.state('zoomed')
print(app.attributes())
numberDS = 0
numberOS = 1
buttons = []
def checkboxClick():

    if advancedMode.get():
        advancedModeSwitch.configure(hover_color=("#ff9c5a"))
    else:
        advancedModeSwitch.configure(hover_color="#646469")
def copyInst(part):
    if part == -1:
        pyperclip.copy(instructions)
        copylabel.pack()
        copylabel.configure(text=f"Copied code for the Processor")
        return
    pyperclip.copy(instructions[part])
    copylabel.pack()
    copylabel.configure(text=f"Copied code for Processor {part+1}")
def reset_DS(part=None):
    global numberDS, numberOS, instructions


    if part != None: instructions[part] += f"drawflush display1{newline}"
    else: instructions += f"drawflush display1{newline}"
    numberDS = 0
    numberOS += 1
def button_function(px=22):
    global numberDS, numberOS, instructions, buttons

    for b in buttons: b.grid_remove()
    copylabel.pack_forget()
    progressbar.pack(padx=20, pady=10)
    button.configure(state="disabled")
    combobox.configure(state="disabled")
    combobox.configure(fg_color="#6e7080")
    combobox.configure(button_color="#6e7080")
    button.configure(fg_color="#6e7080")
    progressbar.start()
    if not advancedMode.get():
        try:
            resizesize = px
            pixelsAvailable = int(combobox.get()) * resizesize
            Ipath = filedialog.askopenfilename(filetypes=[("PNG","*.png"),("JPG","*.jpg"),("JPEG","*.jpeg")])

            if Ipath == "" or Ipath == None:
                button.configure(state="enabled")
                combobox.configure(state="enabled")
                combobox.configure(fg_color=("#f58859"))
                combobox.configure(button_color=("#f58859"))
                button.configure(fg_color=("#f58859"))
                progressbar.pack_forget()
                progressbar.stop()
                return
            image = Image.open(Ipath)


            if int(combobox.get()) == 1:
                frame.pack_forget()
                frame.pack(padx=20, pady=20)
                image.thumbnail((pixelsAvailable, pixelsAvailable), resample=PIL.Image.Resampling.LANCZOS)
                image = image.convert("RGBA")
                width, height = image.size

                buttons = []
                instructions = ""
                instructions += f"draw clear 0 0 0 0 0 0{newline}"
                numberDS = 0
                numberOS = 1

                pxlist = list(image.getdata())

                packs = Counter(list(image.getdata())).most_common()
                pxsize = 176 / resizesize
                for p in packs:
                    numberDS += 1
                    numberOS += 1
                    instructions += f"draw color {p[0][0]} {p[0][1]} {p[0][2]} {p[0][3]} 0 0{newline}"
                    indices = list(locate(pxlist, lambda x: x == p[0]))
                    if numberDS == 100:
                        reset_DS()

                    for i in range(p[1]):
                        x = indices[i] % width
                        y = indices[i] // height

                        numberDS += 1
                        numberOS += 1
                        instructions += f"draw rect {x * 8} {176- pxsize -(y * 8)} 8 8 0 0{newline}"
                        if numberDS == 100:
                            reset_DS()



                numberOS += 1
                instructions += f"drawflush display1{newline}"
                instructions += f"jump {numberOS} always x false"

                buttons.append(customtkinter.CTkButton(master=frame, width=70, height=70,
                                                       image=ImageTk.PhotoImage(image.resize((64, 64))), text=f"",
                                                       command=lambda: copyInst(-1), fg_color=("#f58859"),
                                                       hover_color=("#ff9c5a")))
                buttons[0].grid(row=1, column=1, padx=5, pady=5, sticky="n")

                copyInst(-1)
                print(f"done: {numberOS}")
            else:
                frame.pack_forget()
                parts = (int(combobox.get())) ** 2

                rows = int(combobox.get())

                image.thumbnail((pixelsAvailable, pixelsAvailable), resample=PIL.Image.Resampling.LANCZOS)
                image = image.convert("RGBA")
                newimage = Image.new("RGBA",(pixelsAvailable,pixelsAvailable),(0,0,0,0))
                newimage.paste(image)
                image = newimage

                for b in buttons: b.grid_remove()



                width, height = image.size

                instructions = []
                buttons = []
                frame.pack(padx=20, pady=20)
                for part in range(parts):

                    instructions += [""]
                    im = image.crop((resizesize*(part%rows),resizesize*(part//rows),resizesize*((part%rows)+1),resizesize*((part//rows)+1)))



                    instructions[part] += f"draw clear 0 0 0 0 0 0{newline}"
                    numberDS = 0
                    numberOS = 1

                    pxlist = list(im.getdata())

                    packs = Counter(list(im.getdata())).most_common()
                    pxsize = 176 / resizesize
                    for p in packs:
                        pwidth, pheight = im.size
                        numberDS += 1
                        numberOS += 1
                        instructions[part] += f"draw color {p[0][0]} {p[0][1]} {p[0][2]} {p[0][3]} 0 0{newline}"
                        indices = list(locate(pxlist, lambda x: x == p[0]))
                        if numberDS == 100:
                            reset_DS(part)

                        for i in range(p[1]):

                            x = indices[i] % pwidth
                            y = indices[i] // pheight

                            numberDS += 1
                            numberOS += 1
                            instructions[part] += f"draw rect {x * 8} {176 - pxsize - (y * 8)} 8 8 0 0{newline}"
                            if numberDS == 100:
                                reset_DS(part)

                    numberOS += 1
                    instructions[part] += f"drawflush display1{newline}"
                    instructions[part] += f"jump {numberOS} always x false"


                    buttons.append(customtkinter.CTkButton(master=frame,width=70,height=70,image=ImageTk.PhotoImage(im.resize((64,64))), text=f"", command=  lambda c=part: copyInst(c), fg_color=("#f58859"), hover_color=("#ff9c5a")))
                    buttons[part].grid(row=part//rows,column=part%rows,padx=5, pady=5,sticky="n")



                app.geometry(f"{200*rows}x{100*(rows+1)}")

            button.configure(state="enabled")
            combobox.configure(state="enabled")
            combobox.configure(fg_color=("#f58859"))
            combobox.configure(button_color=("#f58859"))
            button.configure(fg_color=("#f58859"))
            progressbar.stop()
            progressbar.pack_forget()

        except:
            button.configure(state="enabled")
            combobox.configure(state="enabled")
            combobox.configure(fg_color=("#f58859"))
            combobox.configure(button_color=("#f58859"))
            button.configure(fg_color=("#f58859"))
            progressbar.pack_forget()
            frame.pack_forget()
            progressbar.stop()
    else:
        #try:
        resizesize = 22
        pixelsAvailable = int(combobox.get()) * resizesize
        Ipath = filedialog.askopenfilename(filetypes=[("PNG", "*.png"), ("JPG", "*.jpg"), ("JPEG", "*.jpeg")])

        if Ipath == "" or Ipath == None:
            button.configure(state="enabled")
            combobox.configure(state="enabled")
            combobox.configure(fg_color=("#f58859"))
            combobox.configure(button_color=("#f58859"))
            button.configure(fg_color=("#f58859"))
            progressbar.pack_forget()
            progressbar.stop()
            return
        image = Image.open(Ipath)

        if int(combobox.get()) == 1:
            frame.pack_forget()
            frame.pack(padx=20, pady=20)
            image.thumbnail((pixelsAvailable, pixelsAvailable), resample=PIL.Image.Resampling.LANCZOS)
            image = image.convert("RGB")
            width, height = image.size

            buttons = []
            instructions = ""

            numberDS = 0
            numberOS = 1

            pxlist = list(image.getdata())

            packs = Counter(list(image.getdata())).most_common()

            instructions += f"draw clear {packs[0][0][0]} {packs[0][0][1]} {packs[0][0][2]} 0 0 0{newline}"
            #print(packs)
            #del packs[0]
            #print(packs)
            pxsize = 176 / resizesize
            for p in packs:
                numberDS += 1
                numberOS += 1
                colorList= list(list(p)[0])
                instructions += f"draw color {colorList[0]} {colorList[1]} {colorList[2]} 0 0 0{newline}"
                indices = list(locate(pxlist, lambda x: x == p[0]))
                if numberDS == 100:
                    reset_DS()

                for i in range(p[1]):
                    x = indices[i] % width
                    y = indices[i] // height

                    numberDS += 1
                    numberOS += 1
                    instructions += f"draw rect {x * pxsize} {176 - pxsize - (y * pxsize)} {pxsize} {pxsize} 0 0{newline}"
                    if numberDS == 100:
                        reset_DS()

            numberOS += 1
            instructions += f"drawflush display1{newline}"
            instructions += f"jump {numberOS} always x false"

            buttons.append(customtkinter.CTkButton(master=frame, width=70, height=70,
                                                   image=ImageTk.PhotoImage(image.resize((64, 64))), text=f"",
                                                   command=lambda: copyInst(-1), fg_color=("#f58859"),
                                                   hover_color=("#ff9c5a")))
            buttons[0].grid(row=1, column=1, padx=5, pady=5, sticky="n")

            copyInst(-1)
            print(f"done: {numberOS}")
        else:

            frame.pack_forget()
            parts = (int(combobox.get())) ** 2

            rows = int(combobox.get())

            image.thumbnail((pixelsAvailable, pixelsAvailable), resample=PIL.Image.Resampling.LANCZOS)
            image = image.convert("RGBA")
            newimage = Image.new("RGBA", (pixelsAvailable, pixelsAvailable), (0, 0, 0, 0))
            newimage.paste(image)
            image = newimage

            for b in buttons: b.grid_remove()

            width, height = image.size

            instructions = []
            buttons = []
            frame.pack(padx=20, pady=20)
            for part in range(parts):

                instructions += [""]
                im = image.crop(
                    (resizesize * (part % rows), resizesize * (part // rows), resizesize * ((part % rows) + 1), resizesize * ((part // rows) + 1)))

                instructions[part] += f"draw clear 0 0 0 0 0 0{newline}"
                numberDS = 0
                numberOS = 1

                pxlist = list(im.getdata())

                packs = Counter(list(im.getdata())).most_common()
                pxsize = 176 / resizesize

                for p in packs:
                    pwidth, pheight = im.size
                    numberDS += 1
                    numberOS += 1
                    instructions[part] += f"draw color {p[0][0]} {p[0][1]} {p[0][2]} {p[0][3]} 0 0{newline}"
                    indices = list(locate(pxlist, lambda x: x == p[0]))
                    if numberDS == 100:
                        reset_DS(part)
                    i = 0
                    while i < p[1]:

                        x = indices[i] % pwidth
                        y = indices[i] // pheight

                        numberDS += 1
                        numberOS += 1
                        tempstring = f"draw rect {x * pxsize} {176 - pxsize - (y * pxsize)} {pxsize} {pxsize} 0 0{newline}"

                        if i + 1 != len(indices):

                            if indices[i+1] % pwidth == (indices[i] % pwidth) +1:
                                tempstring = f"draw rect {x * pxsize * 2} {176 - pxsize - (y * pxsize)} {pxsize} {pxsize} 0 0{newline}"

                                i += 1
                        instructions[part] += tempstring

                        if numberDS == 100:
                            reset_DS(part)
                        i += 1
                numberOS += 1
                instructions[part] += f"drawflush display1{newline}"
                instructions[part] += f"jump {numberOS} always x false"
                print(f"Done: {numberOS}")
                if numberOS < 500:
                    print("REDOING")
                    resizesize = 44
                    instructions[part] = ""
                    im = image.crop(
                        (resizesize * (part % rows), resizesize * (part // rows), resizesize * ((part % rows) + 1), resizesize * ((part // rows) + 1)))

                    instructions[part] += f"draw clear 0 0 0 0 0 0{newline}"
                    numberDS = 0
                    numberOS = 1

                    pxlist = list(im.getdata())

                    packs = Counter(list(im.getdata())).most_common()
                    pxsize = 176 / resizesize

                    for p in packs:
                        pwidth, pheight = im.size
                        numberDS += 1
                        numberOS += 1
                        instructions[part] += f"draw color {p[0][0]} {p[0][1]} {p[0][2]} {p[0][3]} 0 0{newline}"
                        indices = list(locate(pxlist, lambda x: x == p[0]))
                        if numberDS == 100:
                            reset_DS(part)
                        i = 0
                        while i < p[1]:

                            x = indices[i] % pwidth
                            y = indices[i] // pheight

                            numberDS += 1
                            numberOS += 1
                            tempstring = f"draw rect {x * pxsize} {176 - pxsize - (y * pxsize)} {pxsize} {pxsize} 0 0{newline}"

                            if i + 1 != len(indices):

                                if indices[i + 1] % pwidth == (indices[i] % pwidth) + 1:
                                    tempstring = f"draw rect {x * pxsize * 2} {176 - pxsize - (y * pxsize)} {pxsize} {pxsize} 0 0{newline}"

                                    i += 1
                            instructions[part] += tempstring

                            if numberDS == 100:
                                reset_DS(part)
                            i += 1
                    numberOS += 1
                    instructions[part] += f"drawflush display1{newline}"
                    instructions[part] += f"jump {numberOS} always x false"
                    print(f"REDone: {numberOS}")
                buttons.append(customtkinter.CTkButton(master=frame, width=70, height=70,
                                                       image=ImageTk.PhotoImage(im.resize((64, 64))), text=f"",
                                                       command=lambda c=part: copyInst(c), fg_color=("#f58859"),
                                                       hover_color=("#ff9c5a")))
                buttons[part].grid(row=part // rows, column=part % rows, padx=5, pady=5, sticky="n")

            app.geometry(f"{200 * rows}x{100 * (rows + 1)}")

        button.configure(state="enabled")
        combobox.configure(state="enabled")
        combobox.configure(fg_color=("#f58859"))
        combobox.configure(button_color=("#f58859"))
        button.configure(fg_color=("#f58859"))
        progressbar.stop()
        progressbar.pack_forget()

        """except:
            button.configure(state="enabled")
            combobox.configure(state="enabled")
            combobox.configure(fg_color=("#f58859"))
            combobox.configure(button_color=("#f58859"))
            button.configure(fg_color=("#f58859"))
            progressbar.pack_forget()
            frame.pack_forget()
            progressbar.stop()"""



customtkinter.CTkButton(master=app,fg_color=None, hover=False, text="", image=ImageTk.PhotoImage((Image.open("LogoText.png")))).pack(padx=0, pady=10)
imgframe = customtkinter.CTkFrame(master=app,
                               width=150,
                               height=50,
                               corner_radius=5)
imgframe.pack(padx=20, pady=10)
advancedMode = customtkinter.BooleanVar(value=False)
button = customtkinter.CTkButton(master=imgframe, text="Open Image", command=button_function, fg_color=("#f58859"), hover_color=("#ff9c5a"))
button.pack(padx=10, pady=10, side="left")
advancedModeSwitch = customtkinter.CTkCheckBox(master=imgframe, text="Advanced",fg_color="#ec7458",hover_color="#646469",
                                   variable=advancedMode, onvalue=True, offvalue=False, command=checkboxClick)
advancedModeSwitch.pack(padx=10, pady=10, side="right")
progressbar = customtkinter.CTkProgressBar(master=app,height=10,progress_color="#f58859",mode="indeterminate",determinate_speed=2)
progressbar.set(0)

boxframe = customtkinter.CTkFrame(master=app,
                               width=100,
                               height=50,
                               corner_radius=5)
boxframe.pack(padx=20, pady=10)

boxLabel = customtkinter.CTkLabel(master=boxframe,text="Rows:").pack(padx=0, pady=10, side="left")


combobox = customtkinter.CTkOptionMenu(master=boxframe,values=["1","2","3","4","5","6"],fg_color=("#f58859"),button_color="#f58859",button_hover_color="#ff9c5a")
combobox.pack(padx=10, pady=10)
frame = customtkinter.CTkFrame(master=app,
                               width=200,
                               height=200,
                               corner_radius=10)
copylabel = customtkinter.CTkButton(master=boxLabel,fg_color=None, hover=False, text="", image=ImageTk.PhotoImage((Image.open("copy.png"))))


#scrollbar = customtkinter.CTkScrollbar(app, command=frame.yview)

app.mainloop()

