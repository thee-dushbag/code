escape = 0o33
colors = range(0, 8)
nocolor = "\033[0m"
text = f"%sThis is color:{nocolor} %s"

for base in (90, 30, 100, 40):
    for color in colors:
        color = f"[{str(base+color)}m"
        color_str = f"\\{escape:o}{color}"
        color_esc = f"{chr(escape)}{color}"
        print(text %(color_esc, color_str))

