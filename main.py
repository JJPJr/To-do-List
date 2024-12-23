import tkinter as tk  # import module 
import os # I want to make this to do list like mac sticky note feature

def load_tasks(): # need this to load the tasks from the file from last time
    if os.path.exists("tasks.txt"): # need the thing to exist to get the tasks
        with open("tasks.txt", "r") as file: # read the file 
            for task in file: 
                task_list.insert(tk.END, task.strip()) # each new task added to bottom of listbox 

def save_tasks(): 
    with open("tasks.txt","w" ) as file: # when we close and save, the current list will overwirte the last opening 
            for task in task_list.get(0, tk.END): # for all the tasks 
                file.write(task + "\n") # added them to the listbox

""" The key handling will basically handle handling individual tasks
and I still will keep the clear all just to make it easier for the user"""
def keys(event):
    if event.keysym == "Return": 
        select = task_list.curselection()
        if select: 
            index = select [0]
            task_list.insert(tk.END,"") # adds a blank line like in vscode
            task_list.selection_clear(0,tk.END) # clear selections
            task_list.selection_set(index + 1) # now we select the new blank row to type in
            task_list.activate(tk.END) # moves the highlight with it
    elif event.keysym == "BackSpace":
        select = task_list.curselection()
        index = select[0] if select else 0 
        if select: 
            index = select [0]
            current = task_list.get(index)
            if current:
                task_list.delete(index)
                task_list.insert(index, current[:-1])
                # tkinter doesnt let me do in place mod on the listbox so I remove the whole row and add it back with one less character
            else: 
                task_list.delete(index) 
                if index > 0: 
                    index -= 1 
                if task_list.size() == 0:
                    task_list.insert(tk.END, "")
                    task_list.selection_clear(0, tk.END)
                    task_list.selection_set(index)  
                    task_list.activate(index)

        task_list.selection_clear(0, tk.END)
        task_list.selection_set(index)
        task_list.activate(index)
        # this stuff above made it so we can type again right after backspacing

    else: 
        select = task_list.curselection()
        if select: 
            index = select [0]
            current = task_list.get(index)
            task_list.delete(index) # this will remove the current row because we have to use similar logic as before due to in place mod issue 
            task_list.insert(index, current + event.char) # add the row with the new character 
            task_list.selection_clear(0,tk.END) # clear selections
            task_list.selection_set(index) # select same row we are in
            task_list.activate(index) 
    task_list.focus_set()

def clear_all(): 
    task_list.delete(0, tk.END)  # the 0, tk.END will clear the listbox free
    if task_list.size() == 0:
        task_list.insert(tk.END, "")
        task_list.selection_clear(0, tk.END)
        task_list.selection_set(0)  
        task_list.activate(0)
    task_list.focus_set()

def up_arrow(event=None): 
    select = task_list.curselection()
    if select: 
        index = select[0]
        if index > 0: 
            task_list.selection_clear(0,tk.END) # clearing the prev selection so its just one at a time
            task_list.selection_set(index - 1) # can do index because its stored as integer
            task_list.activate(index - 1) # moves the blue highlight on an item
    task_list.focus_set()

def down_arrow(event=None):
    select = task_list.curselection()
    if select: 
        index = select[0]
        if index < task_list.size() - 1: 
            task_list.selection_clear(0,tk.END) # clearing the prev selection so its just one at a time
            task_list.selection_set(index + 1) 
            task_list.activate(index + 1) 
    task_list.focus_set()
    """ The down and up arrow movements are awkward to think about because you have to 
imagine where the selection is moving once the arrow is clicked when coding"""

def on_click(event=None):
    select = task_list.curselection()
    if not select and task_list.size() > 0:
        task_list.selection_set(0)  # Default to the first row if no selection exists
        task_list.activate(0)
    task_list.focus_set()

def main(): 
    global task_list
    window = tk.Tk()   # create a window which is instance
    window.title("To do list sticky note") 

    list_font = ("Calibri",16, "italic")
    global task_list
    task_list = tk.Listbox(window, width=40, height=10, selectmode= tk.SINGLE, font=list_font,activestyle="none", bg= "#FFD700",fg="black", selectbackground="#FFD700", selectforeground="black")
    task_list.pack(pady=10)
    task_list.bind("<Up>", up_arrow)
    task_list.bind("<Down>", down_arrow)
    task_list.bind("<Key>", keys)
    task_list.bind("<Button-1>", on_click)

    button_font = ("Calibri", 12, "bold")
    clear_all_button = tk.Button(window, text="Clear All Tasks", command=clear_all,  bg="black", fg="white", font=button_font)
    clear_all_button.pack(pady=10)
    
    load_tasks()

    task_list.focus_force()
    if task_list.size() == 0:
        task_list.insert(tk.END,"")
    task_list.selection_set(0)
    task_list.activate(0)

    window.protocol("WM_DELETE_WINDOW",lambda: [save_tasks(), window.destroy()]) 
    """ This line is a callback function that passes to the lambda function once the window is attempted to be closed, 
    which then saves tasks and actually destroys the window after in one line of code via the lambda function"""
    task_list.focus_force()

    window.mainloop() # execution line

if __name__ == "__main__":
    main()
