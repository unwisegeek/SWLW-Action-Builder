#!./venv/bin/python3
import argparse
import math
import os
import re
import tkinter
import xerox
import sys

try:
    import tkinter as tk
    from tkinter import ttk
    gui_possible = True
except ModuleNotFoundError:
    gui_possible = False


def send_to_clipboard(formatted_msg):
    print(formatted_msg)
    try:
        xerox.copy(formatted_msg)
    except xerox.XclipNotFound:
        print('Unable to copy to clipboard. You must install xclip on your Linux system.')
    except Exception as e:
        print(f'Unhandled exception: {e}')

VALID_TAGS = {
    "Hy Newn": "hy",
    "Character 2": "c2",
}

parser = argparse.ArgumentParser()
parser.add_argument('--tag', type=str, choices=VALID_TAGS.values(), default=None)
parser.add_argument('--msg', type=str, nargs="*", default=None)
parser.add_argument('--file', type=str, default=None)
parser.add_argument('--clipboard', action='store_true')
parser.add_argument('--gui', action='store_true')


arg = parser.parse_args()

if arg.gui:

    if not gui_possible:
        print("GUI is not available. Please install the tkinter package for your operating system.")
        sys.exit()

    def convert_action(*_):
        try:
            tag = VALID_TAGS[tag_input_box.get()]
        except KeyError:
            tag = tag_input_box.get()
        except NameError:
            tag = ""
        try:
            action_text = input_box.get("1.0", tk.END)
            pattern1 = '\s"'
            pattern2 = '"\s'
            pattern3 = '"\n'
            action_text = re.sub(pattern1, ' "**', action_text)
            action_text = re.sub(pattern2, '**" ', action_text)
            action_text = re.sub(pattern3, '**"', action_text)
        except:
            pass
        try:
            output_box.delete("1.0", tk.END)
        except tkinter.TclError as e:
            print(f"Captured Exception: {e}")
        output_box.insert("1.0", f"{tag}:{action_text}")

    def clear_input_box():
        input_box.delete("1.0", tk.END)
        convert_action()

    # Set up main window
    root = tk.Tk()
    root.title("SWLW Action Formatter")
    tag = tk.StringVar()
    tag.trace('w', convert_action)
    input_text = tk.StringVar()
    input_text.trace('w', convert_action)

    # Configure widgets
    
    ## Text box for action entry, and vertical scrollbar
    ### Input Box and Vertical Scroll Bar
    input_box = tk.Text(root, wrap=tk.WORD, height=3)
    input_vsb = ttk.Scrollbar(root, command=input_box.yview, orient="vertical")
    input_box.configure(yscrollcommand=input_vsb.set)
    input_box.grid(column=2, row=1, rowspan=3, padx=1, pady=1, sticky=tk.NS)
    input_vsb.grid(column=3, row=1, rowspan=3, padx=0, pady=0, sticky=tk.NS)

    ### Text box for action output and horizontal scrollbar
    output_box = tk.Text(root, wrap=tk.NONE, height=1)
    output_hsb = ttk.Scrollbar(root, command=output_box.xview, orient="horizontal")
    output_box.configure(xscrollcommand=output_hsb.set)
    output_box.grid(column=2, row=4, padx=1, pady=1, sticky=tk.NSEW)
    output_hsb.grid(column=2, row=5, padx=1, pady=0, sticky=tk.NSEW)

    ## Input boxes
    ### List of Character Tags
    tag_input_box = ttk.Combobox(values=list(VALID_TAGS.keys()), textvariable=tag, width=8)
    tag_input_box.current(0)
    tag_input_box.grid(column=1, row=1, columnspan=2, sticky=tk.NW, padx=1, pady=1)

    ## Buttons
    clr_button = ttk.Button(root, text='Clear', command=clear_input_box)
    clr_button.grid(column=1, row=2, sticky=tk.W, padx=1, pady=1)
    conv_button = ttk.Button(root, text='Convert', command=convert_action)
    conv_button.grid(column=1, row=3, sticky=tk.W, padx=1, pady=1)
    copy_button = ttk.Button(root, text='Copy', command=lambda:send_to_clipboard(output_box.get("1.0", tk.END)[:-1]))
    copy_button.grid(column=1, row=4, sticky=tk.W, padx=1, pady=1)

    # Binds
    input_box.bind('<Return>', convert_action)
    input_box.bind('<Button-1>', convert_action)
    input_box.bind('<Escape>', lambda e: clear_input_box())
    input_box.bind('<Double-3>', lambda e: clear_input_box())    
    root.mainloop()
    sys.exit()

if arg.file:
    print("Files aren't yet supported. Exiting.")
    sys.exit()

if arg.msg:
    # Pull msg into single string from list
    formatted_msg = f'{arg.tag}:'
    for word in arg.msg:
        formatted_msg += f'"**{word}**" ' if ' ' in word else f'{word} '
else:
    print("No message found.")
    sys.exit()

if arg.clipboard:
    send_to_clipboard(formatted_msg)
else:
    print(formatted_msg)