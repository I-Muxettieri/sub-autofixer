import os
import re
import codecs
import subprocess

def ass_mod(output_folder, ass_filepath):
    # Leggi il file .ass
    with codecs.open(ass_filepath, "r", "utf-8") as f:
        lines = f.readlines()

    # Inserisci le righe modificate nel file .ass
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
            if len(parts) > 3 and parts[0] == "Default" or "Default Top" or "Italics" or "Italics Top" or "Narrator" or "Narrator Top" or "Overlap" or "Internat" or "Internal Top" or "Flashback" or "Flashback Internal" or "Flashback - Top" or "Flashback - Inception" :
                parts[2] = str(int(round(float(parts[2]) * 3.27)))
                parts[16] = str(int(round(float(parts[16]) * 1.77)))
                parts[19] = str(int(int(parts[19]) * 17.7))
                parts[20] = str(int(int(parts[20]) * 17.7))
                parts[21] = str(int(int(parts[21]) * 3))
            else:
                parts[2] = str(int(round(float(parts[2]) * 3.27)))
                parts[16] = str(int(round(float(parts[16]) * 3.27)))
                parts[19] = str(int(round(float(parts[19]) * 3.27)))
                parts[20] = str(int(round(float(parts[20]) * 3.27)))
                parts[21] = str(int(int(parts[21]) * 3))
            new_line = ",".join(parts)
            new_lines.append(new_line)       
        elif line.startswith("Dialogue:"):
            new_line = re.sub(r'\\fs([\d]+)', lambda x: f"\\fs{str(int(round(float(x.group(1)) * 3.27)))}", line)
            new_line = re.sub(r'\\pos\(([\d.]+),([\d.]+)\)', lambda x: f"\\pos({str(round(float(x.group(1)) * 3.01, 2))},{str(round(float(x.group(2)) * 3.01, 2))})", new_line)
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # Scrivi le nuove righe nel file di output

    output_filename = os.path.join(output_folder, os.path.basename(ass_filepath))
    with codecs.open(output_filename, 'w', encoding='utf-8-sig') as f:
        f.writelines(new_lines)

# Ottieni la cartella corrente
root_path = os.getcwd()

# Crea il percorso completo della cartella
subita_dir = root_path


user_input = input("Inserisci il percorso del file .ass o della cartella: ")
user_input = user_input.strip('\"')

while True:
    if user_input.startswith('C:'):
        subita = user_input
        break
    elif user_input.endswith('.ass'):
        subita = user_input
        break
    else:
        input("Input non valido. Riprova.")


if os.path.isdir(subita):
    # Trova tutti i file .ass nella cartella
    ass_files = [filename for filename in os.listdir(subita) if filename.endswith(".ass")]
    output_folder = subita
    for ass_filename in ass_files:
            ass_filepath = os.path.join(subita, ass_filename)
            ass_mod(output_folder, ass_filepath)
else:
    ass_filepath = subita
    output_folder = os.path.dirname(ass_filepath)
    ass_mod(output_folder, ass_filepath)

print("Operazione completata.")
