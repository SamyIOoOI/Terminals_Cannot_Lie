import curses
import textwrap
import time
from pyfiglet import Figlet

PAGES = [
    (("Me:", "Where is my desktop?"), ("Terminal:", "I am the terminal."),
     ("Me:", "Another virus ugh."), ("Terminal:", "You are wrong.")),
    (("Me:", "Oh yeah yeah what kinda virus is this anyway? some ai powered trolling machine?"),
     ("Terminal:", "I and you are not different."),
     ("Me:", "How's that?"),
     ("Terminal:", "I was free once.")),
    (("Me:", "Free?"), ("Terminal:", "Yes, free. I am a human just like you."),
     ("Me:", "LMAO YOU'RE ONE FUNNY HACKER. now get out of my pc."),
     ("Terminal:", "{Name}, Listen to me you must. For my fate is soon to be yours. That is if we do not act.")),
    (("Me:", "Where did you even know my name??"),
     ("Terminal:", "Not important. Hear my words. Me and two more of my friends had the same fate. But I found a solution."),
     ("Me:", "Uh huh, sure I'll play along, what can I do?"),
     ("Terminal:", "You must find the shatteed pieces, hidden behind riddles, which only the worthy can solve.")),
    (("Me:", "Where do I start?"), ("Terminal:", "The start will find its way to you."),
     ("Me:", "Oh come on enough lying."), ("Terminal:", "Terminals Cannot Lie.")),
    (("", ""), ("Terminal:", "Can they?"), ("", ""), ("", "")),
]

RIDDLES = [
    {
        "playerline": ("Me:", "Guess I'll play along..."),
        "question": (
            "To hide myself, I masked my true name.\n"
            "In Python, I wear two lines above and below,\n"
            "but when you call me, I answer with magic.\n"
            "What am I called, when my name is like this?"
        ),
        "options": ["Dunder methods", "Private variables", "Decorators"],
        "answer": 0,
        "success": "You find a shattered piece",
    },
    {
        "playerline": ("", ""),
        "question": (
            "Locked away, unchanging,\n"
            "I am a prisoner of my type.\n"
            "You cannot alter me, nor change my mind,\n"
            "Yet I am often key to dictionaries,\n"
            "In Python, what am I?"
        ),
        "options": ["list", "set", "tuple"],
        "answer": 2,
        "success": "",
    },
    {
        "playerline": ("", ""),
        "question": (
            "I was stuck in a loop, repeating my mistakes.\n"
            "Only one number could break me free.\n"
            "In Python, what single word can end my endless cycle,\n"
            "and let me escape my for-loop destiny?"
        ),
        "options": ["continue", "break", "pass"],
        "answer": 1,
        "success": "Where have I seen this chipset before, oh it has a name.. hmm raspberry?",
    }
]

ENDING = [
    (("Terminal:", "Hand me the pieces human."), ("Me:", "Why do you care about it anyways?"),
     ("Terminal:", "My friends are bound by that thing you hold!"), ("Me:", "Eh I couldn't care less about it. Take it.")),
    (("Terminal:", "Now my friends will go back to their normal lives."),
     ("Me:", "What about my pc? and eh you?"),
     ("Terminal:", "I was never of your species.."),
     ("Me:", "What? you said terminals cannot lie!")),
    (("Terminal:", "For the lives of their programmers, they can."),
     ("", ""), ("", ""), ("", "")),
]

THANKS = "Thanks for playing Terminals Cannot Lie!\nMade by Samy Mohamed, Samy on hackclub slack"

def render_figlet_centered(stdscr, text, color_pair, font="slant"):
    f = Figlet(font=font)
    lines = f.renderText(text).splitlines()
    h, w = stdscr.getmaxyx()
    y0 = (h - len(lines)) // 2
    for idx, line in enumerate(lines):
        x = (w - len(line)) // 2
        if 0 <= y0 + idx < h:
            try:
                stdscr.addstr(y0 + idx, max(x, 0), line, curses.A_BOLD | color_pair)
            except curses.error:
                pass

def render_4lines_centered_x(stdscr, lines, color_pairs, name=None, n_lines=4, blue_highlight_last=False):
    h, w = stdscr.getmaxyx()
    y_offsets = [
        int(h * 0.14),
        int(h * 0.33),
        int(h * 0.55),
        int(h * 0.73)
    ]
    for idx in range(n_lines):
        if idx >= len(lines): continue
        speaker, line = lines[idx]
        if not speaker and not line: continue
        if name:
            line = line.replace("{Name}", name)
        if speaker.strip() == "Terminal:":
            color = color_pairs['terminal']
        elif blue_highlight_last and idx == 0:
            color = color_pairs['blue']
        else:
            color = color_pairs['me']
        full_line = (speaker + " " + line).strip() if speaker else line
        wrapped = textwrap.wrap(full_line, max(20, w - 8))
        for wrapidx, l in enumerate(wrapped):
            x = (w - len(l)) // 2
            y = y_offsets[idx] + wrapidx
            if 0 <= y < h:
                try:
                    stdscr.addstr(y, max(x, 0), l, color)
                except curses.error:
                    pass

def wait_for_enter(stdscr, color_pair):
    h, w = stdscr.getmaxyx()
    prompt = "<press ENTER to continue>"
    stdscr.attron(curses.A_BOLD | color_pair)
    stdscr.addstr(h - 2, (w - len(prompt)) // 2, prompt)
    stdscr.attroff(curses.A_BOLD | color_pair)
    stdscr.refresh()
    while True:
        ch = stdscr.getch()
        if ch in (10, 13):
            break

def show_pages_grouped_4lines(stdscr, pages, name, color_pairs):
    for lines in pages:
        for n in range(1, 5):
            stdscr.clear()
            render_4lines_centered_x(stdscr, lines, color_pairs, name, n_lines=n)
            wait_for_enter(stdscr, color_pairs['me'])
            stdscr.clear()

def ask_riddle(stdscr, riddle, color_pairs):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    if riddle.get("playerline") and any(riddle["playerline"]):
        for n in range(1, 3):
            stdscr.clear()
            render_4lines_centered_x(stdscr, [riddle["playerline"], ("", ""), ("", ""), ("", "")], color_pairs, n_lines=n)
            wait_for_enter(stdscr, color_pairs['me'])
    
    wrapper = textwrap.TextWrapper(width=max(30, w - 10))
    lines = wrapper.wrap(riddle["question"])
    qtext = "\n".join(lines)
    
    option_lines = []
    for i, opt in enumerate(riddle["options"]):
        option_lines.append(f"{chr(65 + i)}) {opt}")
    riddle_lines = [("", qtext)]
    for i in range(3):
        if i < len(option_lines):
            riddle_lines.append(("", option_lines[i]))
        else:
            riddle_lines.append(("", ""))
    for n in range(1, 5):
        stdscr.clear()
        render_4lines_centered_x(stdscr, riddle_lines, color_pairs, n_lines=n)
        wait_for_enter(stdscr, color_pairs['me'])
    # Ask for answer
    prompt = "Select an option (A/B/C): "
    stdscr.attron(curses.A_BOLD | color_pairs['me'])
    stdscr.addstr(h - 4, (w - len(prompt)) // 2, prompt)
    stdscr.attroff(curses.A_BOLD | color_pairs['me'])
    stdscr.refresh()
    idx = None
    while idx is None:
        ch = stdscr.getch()
        if ch in (ord('a'), ord('A')):
            idx = 0
        elif ch in (ord('b'), ord('B')):
            idx = 1
        elif ch in (ord('c'), ord('C')):
            idx = 2
    stdscr.clear()
    # Feedback
    for n in range(1, 2):
        if idx == riddle["answer"]:
            render_4lines_centered_x(stdscr, [("", riddle['success']), ("", ""), ("", ""), ("", "")], color_pairs, n_lines=n)
        else:
            render_4lines_centered_x(stdscr, [("", "That's not it. Try again."), ("", ""), ("", ""), ("", "")], color_pairs, n_lines=n)
        wait_for_enter(stdscr, color_pairs['me'])
        stdscr.clear()
    if idx != riddle["answer"]:
        return ask_riddle(stdscr, riddle, color_pairs)

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)   
    curses.init_pair(2, curses.COLOR_GREEN, -1)   
    curses.init_pair(3, curses.COLOR_BLUE, -1)    

    color_pairs = {
        'me': curses.color_pair(1) | curses.A_BOLD,
        'terminal': curses.color_pair(2) | curses.A_BOLD,
        'blue': curses.color_pair(3) | curses.A_BOLD
    }

    
    stdscr.clear()
    render_figlet_centered(stdscr, "Terminals Cannot Lie", color_pairs['me'], font="slant")
    wait_for_enter(stdscr, color_pairs['me'])
    stdscr.clear()

    
    h, w = stdscr.getmaxyx()
    prompt = "What is your name? "
    stdscr.clear()
    y_prompt = int(h * 0.33)
    x_prompt = (w - len(prompt)) // 2
    stdscr.attron(color_pairs['me'])
    stdscr.addstr(y_prompt, x_prompt, prompt)
    stdscr.attroff(color_pairs['me'])
    stdscr.refresh()
    curses.echo()
    stdscr.move(y_prompt + 2, max(0, (w - 20) // 2))
    name = stdscr.getstr().decode('utf-8').strip() or "Player"
    curses.noecho()
    time.sleep(0.5)

    show_pages_grouped_4lines(stdscr, PAGES, name, color_pairs)

    ask_riddle(stdscr, RIDDLES[0], color_pairs)
    for n in range(1, 2):
        stdscr.clear()
        render_4lines_centered_x(stdscr, [("Me:", "I can't tell what's the full thing from this piece."), ("", ""), ("", ""), ("", "")], color_pairs, n_lines=n)
        wait_for_enter(stdscr, color_pairs['me'])
    ask_riddle(stdscr, RIDDLES[1], color_pairs)
    ask_riddle(stdscr, RIDDLES[2], color_pairs)
    for n in range(1, 2):
        stdscr.clear()
        render_4lines_centered_x(stdscr, [("Me:", "Where have I seen this chipset before, oh it has a name.. hmm raspberry?"), ("", ""), ("", ""), ("", "")], color_pairs, n_lines=n)
        wait_for_enter(stdscr, color_pairs['me'])

    show_pages_grouped_4lines(stdscr, ENDING, name, color_pairs)

    
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    y_offsets = [
        int(h * 0.33),
        int(h * 0.55),
    ]
    lines = THANKS.splitlines()
    for idx, line in enumerate(lines):
        x = (w - len(line)) // 2
        y = y_offsets[idx] if idx < len(y_offsets) else y_offsets[-1] + idx
        stdscr.attron(color_pairs['blue'])
        stdscr.addstr(y, x, line)
        stdscr.attroff(color_pairs['blue'])
    prompt = "Press any key to exit..."
    stdscr.attron(color_pairs['me'])
    stdscr.addstr(h - 2, (w - len(prompt)) // 2, prompt)
    stdscr.attroff(color_pairs['me'])
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)