import os
import re
import codecs
import tkinter as tk
from tkinter import filedialog

def ass_mod(output_folder, ass_filepath):
    with codecs.open(ass_filepath, "r", "utf-8") as f:
        lines = f.readlines()

    lines.insert(15, "YCbCr Matrix: TV.709\n")
    lines.insert(16, "ScaledBorderAndShadow: yes\n")

    new_lines = []
    for line in lines:
        if "PlayResX:" in line or "PlayResY:" in line:
            if "PlayResX:" in line:
                new_lines.append("PlayResX: 1920\n")
            if "PlayResY:" in line:
                new_lines.append("PlayResY: 1080\n")
        elif line.startswith("Style:"):
            parts = line.split(",")
            if len(parts) > 3:
                # Cambiamo il font a "Gandhi Sans Bold"
                parts[1] = "Gandhi Sans Bold"
            if len(parts) > 3 and parts[0] == "Default" or "Default Top" or "Italics" or "Italics Top" or "Narrator" or "Narrator Top" or "Overlap" or "Internat" or "Internal Top" or "Flashback" or "Flashback Internal" or "Flashback - Top" or "Flashback - Inception" :
                parts[2] = str(int(round(float(parts[2]) * 3.27)))
                parts[16] = str(int(round(float(parts[16]) * 1.77)))
                parts[19] = str(int(int(parts[19]) * 17.7))
                parts[20] = str(int(int(parts[20]) * 17.7))
                parts[21] = str(int(int(parts[21]) * 3))
            new_line = ",".join(parts)
            new_lines.append(new_line)
        elif line.startswith("Dialogue:"):
            new_line = re.sub(r'\\fs([\d]+)', lambda x: f"\\fs{str(int(round(float(x.group(1)) * 3.27)))}", line)
            new_line = re.sub(r'\\pos\(([\d.]+),([\d.]+)\)', lambda x: f"\\pos({str(round(float(x.group(1)) * 3.01, 2))},{str(round(float(x.group(2)) * 3.01, 2))})", new_line)
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    output_filename = os.path.join(output_folder, os.path.basename(ass_filepath))
    with codecs.open(output_filename, 'w', encoding='utf-8-sig') as f:
        f.writelines(new_lines)

def browse():
    folder_selected = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_selected)

def start_modification():
    user_input = entry.get().strip('\"')
    if os.path.isdir(user_input):
        ass_files = [filename for filename in os.listdir(user_input) if filename.endswith(".ass")]
        output_folder = user_input
        for ass_filename in ass_files:
            ass_filepath = os.path.join(user_input, ass_filename)
            ass_mod(output_folder, ass_filepath)
    else:
        ass_filepath = user_input
        output_folder = os.path.dirname(ass_filepath)
        ass_mod(output_folder, ass_filepath)
    print("Operazione completata.")

window = tk.Tk()
window.title("Modificatore di file .ass")

entry = tk.Entry(window, width=50)
entry.pack()
entry.insert(0, "Inserisci il percorso del file .ass o della cartella")

browse_button = tk.Button(window, text="Sfoglia", command=browse)
browse_button.pack()

start_button = tk.Button(window, text="Inizia", command=start_modification)
start_button.pack()

window.mainloop()
