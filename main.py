from tkinter import *
from PIL import Image, ImageTk, ImageFont, ImageDraw
from tkinter import filedialog, simpledialog, messagebox

BACKGROUND_COLOR = "#303030"
FONT = ("Cantarell", 14, "normal")


def get_image():
    global new_image, image, img_type, img_path
    img_path = filedialog.askopenfilename()
    img_file = str(img_path.split('/')[-1])
    img_type = img_file.split('.')[-1].lower()
    if img_type == 'jpg' or img_type == 'png' or img_type == 'jpeg':
        save_file_btn['state'] = 'active'
        add_watermark_btn['state'] = 'active'
        clear_img_btn['state'] = 'active'
        image = (Image.open(img_path))
        resized_image = image.resize((cv_width, cv_height))
        new_image = ImageTk.PhotoImage(resized_image)
        canvas.itemconfig(img, image=new_image, anchor=NW)
    else:
        messagebox.showerror("Error", "Invalid image format.")


def add_watermark():
    global image, preview_image
    watermark_text = watermark_text_entry.get()
    title_font = ImageFont.truetype(font='ubuntu-font/Ubuntu-R.ttf', size=160)
    text_position = (image.width / 2, image.height / 2)
    anc = "mm"
    if variable.get() == 'Top Left':
        text_position = (image.width * 0.03, image.height * 0.07)
        anc = "lm"
    if variable.get() == 'Top Right':
        text_position = (image.width * 0.97, image.height * 0.07)
        anc = "rm"
    if variable.get() == 'Bottom Left':
        text_position = (image.width * 0.03, image.height * 0.9)
        anc = "lm"
    if variable.get() == 'Bottom Right':
        text_position = (image.width * 0.97, image.height * 0.9)
        anc = "rm"
    image_to_edit = ImageDraw.Draw(image)
    image_to_edit.text(text_position, watermark_text, tuple(map(int, text_color_entry.get().split(', '))),
                       font=title_font, anchor=anc)
    wm_resized = image.resize((cv_width, cv_height))
    preview_image = ImageTk.PhotoImage(wm_resized)
    canvas.itemconfig(img, image=preview_image, anchor=NW)


def clear_img():
    global img_path, image, new_image
    image = (Image.open(img_path))
    resized_image = image.resize((cv_width, cv_height))
    new_image = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig(img, image=new_image, anchor=NW)


def save_img():
    global image, img_type
    img_name = simpledialog.askstring("Save as", "Name:", parent=screen)
    if img_name is not None:
        image.save(f"{img_name}.{img_type}")


screen = Tk()
screen.title('WaterMarker')
wd_width = screen.winfo_screenwidth() * 0.5
wd_height = screen.winfo_screenheight() * 0.5
cv_width = int(round(wd_width * 0.8))
cv_height = int(round(wd_height * 0.8))

screen.config(width=wd_width, height=wd_height, padx=4, pady=4, background=BACKGROUND_COLOR)

canvas = Canvas(width=cv_width, height=cv_height, background='#202020', highlightthickness=0)
img = canvas.create_image(0, 0)
canvas.grid(column=2, row=0, rowspan=99)

watermark_text_label = Label(text='Watermark Text:', width=18, background='#303030', fg='#ffffff')
watermark_text_label.grid(column=0, row=1, columnspan=2)
text_color_label = Label(text='Text Color (RGB):', width=18, background='#303030', fg='#ffffff')
text_color_label.grid(column=0, row=3, columnspan=2)
watermark_position_label = Label(text='Watermark Position:', width=18, background='#303030', fg='#ffffff')
watermark_position_label.grid(column=0, row=5, columnspan=2)

watermark_text_entry = Entry(width=20)
watermark_text_entry.grid(column=0, row=2, columnspan=2)
text_color_entry = Entry(width=20)
text_color_entry.insert(0, '255, 255, 255')
text_color_entry.grid(column=0, row=4, columnspan=2)

select_file_btn = Button(text='Select File', highlightthickness=0, command=get_image)
select_file_btn.grid(column=0, row=0)

save_file_btn = Button(text='Save File', highlightthickness=0, command=save_img, state="disabled")
save_file_btn.grid(column=1, row=0)

add_watermark_btn = Button(text='Add Watermark', highlightthickness=0, width=18, command=add_watermark, state="disabled")
add_watermark_btn.grid(column=0, row=7, columnspan=2)

clear_img_btn = Button(text='Clear All', highlightthickness=0, width=18, command=clear_img, state="disabled")
clear_img_btn.grid(column=0, row=8, columnspan=2)


options = ['Center', 'Top Left', 'Top Right', 'Bottom Left', 'Bottom Right']

variable = StringVar()
variable.set(options[0])

watermark_location = OptionMenu(screen, variable, *options)
watermark_location.grid(column=0, row=6, columnspan=2)

screen.mainloop()
