import json
import diarylist as dl
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from datetime import date
from tkinter import scrolledtext

year: int
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']
twenty_eight_days = [str(i) for i in range(1, 29)]
twenty_nine_days = [str(i) for i in range(1, 30)]
thirty_days = [str(i) for i in range(1, 31)]
thirty_one_days = [str(i) for i in range(1, 32)]
days_in_month = {
    "January": thirty_one_days,
    "March": thirty_one_days,
    "April": thirty_days,
    "May": thirty_one_days,
    "June": thirty_days,
    "July": thirty_one_days,
    "August": thirty_one_days,
    "September": thirty_days,
    "October": thirty_one_days,
    "November": thirty_days,
    "December": thirty_one_days
}

# transfer diary array to linked list
diary_book: dl.DiaryList
current: dl.DiaryNode
day_times: dict


def set_datas():
    global day_times
    global diary_book
    data = json.load(open('diary_book.json', 'r'))
    day_times = data[0]
    diary_book = dl.DiaryList()
    i = 0
    while i < len(data[1]):
        y, m, d = map(int, data[1][i][0].split('-'))
        new_story = dl.DiaryNode(date(y, m, d), dl.StoryNode(data[1][i][1][0], data[1][i][1][1]))
        j = 2
        while j < len(data[1][i]):
            new_story.append(dl.StoryNode(data[1][i][j][0], data[1][i][j][1]))
            j += 1
        diary_book.append(new_story)
        i += 1


# display control and data manipulation
def to_write_story():
    notebook.hide(0)
    notebook.hide(2)
    notebook.hide(3)
    toggle_today()
    notebook.select(write_story_frame)


def to_read_story():
    notebook.hide(0)
    notebook.hide(1)
    notebook.hide(3)
    notebook.select(read_diary_frame)
    if diary_book.head:
        global current
        current = diary_book.head
        read_stories()
        if current.next:
            next_button.grid(row=1, column=2)
        else:
            next_button.grid_forget()
    else:
        nothing_label = tk.Label(read_story_frame, text="There is nothing to read.")
        nothing_label.pack()


def to_quit():
    window.destroy()
    data1 = [day_times, diary_book.to_list()]
    json.dump(data1, open('diary_book.json', 'w'))


def from_write_story_to_opening():
    notebook.hide(1)
    notebook.select(opening_frame)
    clear_input()


def from_read_diary_to_opening():
    notebook.hide(2)
    notebook.select(opening_frame)
    clear_reading()


def choose_month(event):
    global year
    try:
        year = int(year_entry.get())
        month_combobox.config(values=months)
    except:
        month_combobox.config(values=[])
    finally:
        month_combobox.set('')
        day_combobox.set('')
        day_combobox.config(values=[])


def choose_day(event):
    selected_value = month_combobox.get()
    day_combobox.set('')
    day_combobox.config(values=[])
    if selected_value == 'February':
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            day_combobox.config(values=twenty_nine_days)
        else:
            day_combobox.config(values=twenty_eight_days)
    else:
        day_combobox.config(values=days_in_month[selected_value])


def show_enter(event):
    text1 = headline_entry.get("1.0", "end-1c")  # Get all text excluding the trailing newline character
    text2 = content_entry.get("1.0", "end-1c")
    if text1.strip() and text2.strip():
        from_write_story_to_opening_button.pack_forget()
        enter_button.pack()
        from_write_story_to_opening_button.pack()
    else:
        enter_button.pack_forget()


is_today: bool


def click_enter():
    global is_today
    today = date.today()
    if is_today:
        new_date2 = today
    else:
        global year
        year = int(year_entry.get())
        month = months.index(month_combobox.get()) + 1
        day = int(day_combobox.get())
        new_date2 = date(year, month, day)
    today_string = today.strftime('%Y-%m-%d')
    if today_string in list(day_times.keys()):
        day_times[today_string] += 1
    else:
        day_times[today_string] = 1
    new_story2 = dl.StoryNode(headline_entry.get("1.0", "end-1c"), content_entry.get("1.0", "end-1c"))
    diary_book.sorted_insert(new_date2, new_story2)
    clear_input()


def clear_input():
    year_entry.delete(0, 'end')
    month_combobox.set('')
    day_combobox.set('')
    month_combobox.config(values=[])
    day_combobox.config(values=[])
    headline_entry.delete("1.0", "end")
    content_entry.delete("1.0", "end")
    enter_button.pack_forget()


def read_stories():
    read_story_frame.config(text=current.date.strftime("%Y/%m/%d"))
    stories = current.stories
    while stories:
        frame = tk.LabelFrame(read_story_frame, text=stories.headline)
        frame.pack(fill=tk.BOTH, padx=5, pady=5)
        label = tk.Label(frame, text=stories.content)
        label.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        stories = stories.next


def clear_reading():
    for widget in read_story_frame.winfo_children():
        widget.destroy()
    first_page_button.grid_forget()
    prev_button.grid_forget()
    next_button.grid_forget()


def click_first_page():
    clear_reading()
    global current
    current = diary_book.head
    read_stories()
    first_page_button.grid_forget()
    prev_button.grid_forget()
    if current.next:
        next_button.grid(row=1, column=2)
    else:
        next_button.grid_forget()


def click_prev():
    clear_reading()
    global current
    current = current.prev
    read_stories()
    next_button.grid(row=1, column=2)
    if current.prev:
        first_page_button.grid(row=1, column=0)
        prev_button.grid(row=1, column=1)
    else:
        first_page_button.grid_forget()
        prev_button.grid_forget()


def click_next():
    clear_reading()
    global current
    current = current.next
    read_stories()
    first_page_button.grid(row=1, column=0)
    prev_button.grid(row=1, column=1)
    if current.next:
        next_button.grid(row=1, column=2)
    else:
        next_button.grid_forget()


def toggle_today():
    global is_today
    is_today = True
    checkbox_var1.set(True)
    checkbox_var2.set(False)
    date_frame.pack_forget()
    story_frame.pack()


def toggle_select():
    global is_today
    is_today = False
    checkbox_var1.set(False)
    checkbox_var2.set(True)
    story_frame.pack_forget()
    date_frame.pack()
    story_frame.pack()


# reset diary book
def to_erase():
    sub_window = tk.Toplevel(window)
    sub_window.title("Erase the diary")

    label = tk.Label(sub_window, text="Are you sure do you want to reset?")
    label.pack()

    accept_button = tk.Button(sub_window, text="Yes", command=lambda: (
        sub_window.destroy(),
        day_times.clear(),
        diary_book.clear()
    ))
    accept_button.pack()

    refuse_button = tk.Button(sub_window, text="No", command=lambda: sub_window.destroy())
    refuse_button.pack()


# look overview
def to_overview():
    notebook.hide(0)
    notebook.hide(1)
    notebook.select(overview_frame)
    overview_label = tk.Label(overview_frame, text='OVERVIEW')
    overview_label.pack()

    # Create a figure and plot the bar chart
    fig, ax = plt.subplots()
    ax.bar(list(day_times.keys()), list(day_times.values()))

    # Add labels and title
    ax.set_xlabel('date')
    ax.set_ylabel('times of write new story')

    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=overview_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    from_overview_to_opening_button = tk.Button(overview_frame, text='Back', command=from_overview_to_opening)
    from_overview_to_opening_button.pack()


def from_overview_to_opening():
    notebook.hide(3)
    notebook.select(0)
    for widget in overview_frame.winfo_children():
        widget.destroy()


# display and setup
window = tk.Tk()
window.geometry("1000x800")
window.title("My Dear Diary")

set_datas()

notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill="both")

# opening
opening_frame = tk.Frame(notebook)
notebook.add(opening_frame, text='opening')
opening_label = tk.Label(opening_frame, text="MY DEAR DIARY")
opening_label.pack()
menus_frame = tk.LabelFrame(opening_frame)
menus_frame.pack()
write_story_button = tk.Button(menus_frame, text="Write a story", command=to_write_story)
write_story_button.pack(fill=tk.BOTH, padx=5, pady=5)
read_diary_button = tk.Button(menus_frame, text="Read the diary", command=to_read_story)
read_diary_button.pack(fill=tk.BOTH, padx=5, pady=5)
reset_button = tk.Button(menus_frame, text="Erase the diary", command=to_erase)
reset_button.pack(fill=tk.BOTH, padx=5, pady=5)
overview_button = tk.Button(menus_frame, text="Overview", command=to_overview)
overview_button.pack(fill=tk.BOTH, padx=5, pady=5)
recover_button = tk.Button(menus_frame, text="Recover", command=set_datas)
recover_button.pack(fill=tk.BOTH, padx=5, pady=5)
quit_button = tk.Button(menus_frame, text="Quit", command=to_quit)
quit_button.pack(fill=tk.BOTH, padx=5, pady=5)

# write a story
write_story_frame = tk.Frame(notebook)
notebook.add(write_story_frame, text='write story')
write_story_label = tk.Label(write_story_frame, text="WRITE A STORY")
write_story_label.pack()

checkbox_var1 = tk.BooleanVar()
checkbox_var2 = tk.BooleanVar()
today_checkbutton = tk.Checkbutton(write_story_frame, text="Today", variable=checkbox_var1, command=toggle_today)  #
today_checkbutton.pack()
select_day_checkbutton = tk.Checkbutton(write_story_frame, text="Select day", variable=checkbox_var2,
                                        command=toggle_select)  #
select_day_checkbutton.pack()

input_frame = tk.LabelFrame(write_story_frame)
input_frame.pack()

date_frame = tk.Frame(input_frame)
story_frame = tk.Frame(input_frame)

year_label = tk.Label(date_frame, text="Year")
year_entry = tk.Entry(date_frame)
year_entry.bind("<KeyRelease>", choose_month)
year_label.grid(row=0, column=0, padx=5, pady=5)
year_entry.grid(row=1, column=0, padx=5, pady=5)

month_label = tk.Label(date_frame, text="Month")
month_combobox = ttk.Combobox(date_frame, state='readonly')
month_combobox.bind("<<ComboboxSelected>>", choose_day)
month_label.grid(row=0, column=1, padx=5, pady=5)
month_combobox.grid(row=1, column=1, padx=5, pady=5)

day_label = tk.Label(date_frame, text="Day")
day_combobox = ttk.Combobox(date_frame, state='readonly')
day_label.grid(row=0, column=2, padx=5, pady=5)
day_combobox.grid(row=1, column=2, padx=5, pady=5)

headline_label = tk.Label(story_frame, text="Headline")
headline_entry = scrolledtext.ScrolledText(story_frame, width=40, height=5)
headline_entry.bind("<KeyRelease>", show_enter)
headline_label.pack()
headline_entry.pack(padx=5, pady=5)
content_label = tk.Label(story_frame, text="Content")
content_entry = scrolledtext.ScrolledText(story_frame, width=40, height=10)
content_entry.bind("<KeyRelease>", show_enter)
content_label.pack()
content_entry.pack(padx=5, pady=5)

enter_button = tk.Button(write_story_frame, text="Enter", command=click_enter)
from_write_story_to_opening_button = tk.Button(write_story_frame, text="Back", command=from_write_story_to_opening)
from_write_story_to_opening_button.pack()

# read diary
read_diary_frame = tk.Frame(notebook)
notebook.add(read_diary_frame, text='read diary')
read_diary_label = tk.Label(read_diary_frame, text='READ DIARY')
read_diary_label.pack()
read_story_frame = tk.LabelFrame(read_diary_frame)
read_story_frame.pack()

reading_console = tk.Frame(read_diary_frame)
reading_console.pack()
first_page_button = tk.Button(reading_console, text='First page', command=click_first_page)
prev_button = tk.Button(reading_console, text='Before', command=click_prev)
from_read_diary_to_opening_button = tk.Button(reading_console, text='Back', command=from_read_diary_to_opening)
next_button = tk.Button(reading_console, text='After', command=click_next)
from_read_diary_to_opening_button.grid(row=1, column=3)

# overview
overview_frame = tk.Frame(notebook)
notebook.add(overview_frame, text='overview')

notebook.select(opening_frame)
notebook.hide(1)
notebook.hide(2)
notebook.hide(3)

window.protocol("WM_DELETE_WINDOW", to_quit)

window.mainloop()
