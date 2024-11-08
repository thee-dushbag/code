reset = "\033[0m"
escape = 0o33
effects = range(0, 128)
test_text = f"%sThIs EffEcT is{reset} %s"

for effect in effects:
    effect_str = f"\\{escape:o}[{effect}m"
    effect_esc = f"{chr(escape)}[{effect}m"
    print(test_text % (effect_esc, effect_str))


