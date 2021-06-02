from tkinter import *
from tkinter import filedialog, messagebox
import subprocess
from highlighter import highlight
from PIL import ImageDraw, Image



theme = 'light'
compiler = Tk()
compiler.title('Untitled - SimpliText')
compiler.resizable(False, False)
compiler.iconphoto(False, PhotoImage(file='icon.png'))

process = None
fnt = ("Arial",10)
def chg_theme():
    global theme
    if theme == 'light':
        compiler.config(bg='#444')
        editor.config(bg='#444',fg='#fff')
        menu_bar.config(bg='#444',fg='#fff')
        theme = 'dark'
    else:
        compiler.config(bg='#fff')
        editor.config(bg='#fff',fg='#000')
        menu_bar.config(bg='#fff',fg='#000')
        theme = 'light'
def cap_code():
    image = Image.new('RGB', (1000, 500), color = 'black')
    ImageDraw.Draw(
        image  # Image
    ).text(
        (0, 0),  # Coordinates
        editor.get('1.0', END),  # Text
        (255,255,255)  # Color
    )
    image.save("test.png")
def on_exit():
    with open("data.txt","w") as f:
        f.write(file_path)
    if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
        compiler.destroy()
def kill_process():
    if process:
        process.terminate()
def set_file_path(path):
    global file_path
    file_path = path
    compiler.title(f'{path.split("/")[-1]} - SimpliText')
    text_changed()
def clear_textwins():
    file_path = ""
    editor.delete('1.0', END)
    code_output.delete('1.0', END)
def open_file(path=None):
    if path == None:
        path = filedialog.askopenfilename(title = "Open",filetypes = (("All Files","*.*"),))
        if path == '':
            return
    with open(path, 'r') as file:
        code = file.read()
        clear_textwins()
        editor.insert('1.0', code)
        set_file_path(path)
        
   
def new_file():
    compiler.title('Untitled - SimpliText')
    clear_textwins()

def save_as():
    if file_path == '':
        path = filedialog.asksaveasfilename(title="Save As",filetypes = (("All Files","*.*"),))
    else:
        path = file_path
    if path == '':
        return
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)
def search(text_widget, keyword, tag):
    pos = '1.0'
    while True:
        idx = text_widget.search(keyword, pos, END)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(keyword))
        text_widget.tag_add(tag, idx, pos)
def text_changed(*args):
    typ = None
    if file_path.endswith(".py"):
        typ = "python"
    elif file_path.endswith(".js"):
        typ = "javascript"
    elif file_path.endswith(".html"):
        typ = "html"
    code = editor.get('1.0', END)
    res = highlight(inptext=code,mode=typ)
    for r in res:
        if r[0] != "DEFAULT":
            search(editor, r[3], r[0])
def run_py():
    if file_path == '':
        save_as()
    if file_path == '' or not filepath.endswith(".py"):
        return
    command = f'python "{file_path}"'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.delete('1.0', END)
    code_output.insert('1.0', output)
    code_output.insert('1.0',  error)
    code_op = code_output.get('1.0', END)
    res = highlight(code_op,"python")
    for r in res:
        if r[0] != "DEFAULT":
            search(code_output, r[3], r[0])
compiler.bind('<F5>',lambda x: run_py())
compiler.bind('<F1>',lambda x: cap_code())
compiler.bind("<Control-s>", lambda x: save_as())
editor = Text(undo=True,maxundo=-1)
editor.config(font=fnt)
editor.tag_config('DEFAULT', foreground='black')
editor.tag_config('FLOAT', foreground='#CC92F8')
editor.tag_config('INT', foreground='#CC92F8')
editor.tag_config('STR', foreground='#82D682')
editor.tag_config('COMMENT', foreground='#FBF07B')
editor.tag_config('KEYWORD', foreground='#FC9021')
editor.bind("<KeyRelease>", text_changed)
editor.bind("<Control-n>", lambda x: new_file())
editor.pack()
menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Exit', command=on_exit)
menu_bar.add_cascade(label='File', menu=file_menu)
options_menu = Menu(menu_bar, tearoff=0)
options_menu.add_command(label='Light Mode', command=chg_theme)
menu_bar.add_cascade(label='Options', menu=options_menu)
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run .py', command=run_py)

menu_bar.add_cascade(label='Run', menu=run_bar)



compiler.config(menu=menu_bar)


code_output = Text(height=10)
code_output.config(font=fnt,bg='#222',fg='#fff')
code_output.tag_config('FLOAT', foreground='#CC92F8')
code_output.tag_config('INT', foreground='#CC92F8')
code_output.tag_config('COMMENT', foreground='#FBF07B')
code_output.tag_config('STR', foreground='#82D682')
code_output.tag_config('KEYWORD', foreground='#FC9021')
code_output.bind("<Key>", lambda e: "break")
code_output.bind("<Control-c>", lambda x: kill_process())
code_output.pack()
compiler.protocol("WM_DELETE_WINDOW", on_exit)
chg_theme()
try:
    with open("data.txt","r") as f:
        file_path = f.read()
        open_file(file_path)
        text_change()
except:
    file_path = ''
compiler.mainloop()

