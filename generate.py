#!/usr/bin/env python3
"""
Matrix digital rain SVG — v6. No filters. No blur. Just crisp text on black.
Bright green on black = your monitor does the glowing.
"""
import random

random.seed(42)

WIDTH = 850
HEIGHT = 300
FONT_SIZE = 14
COL_WIDTH = 19
COLS = WIDTH // COL_WIDTH
ROW_HEIGHT = 16
ROWS_NEEDED = (HEIGHT * 2) // ROW_HEIGHT + 4

HW_KATAKANA = "ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ"
DIGITS = "0123456789"
CHAR_POOL = HW_KATAKANA + HW_KATAKANA + DIGITS
XML_ESCAPE = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}


def rc():
    c = random.choice(CHAR_POOL)
    return XML_ESCAPE.get(c, c)


def generate_svg():
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
             f'width="{WIDTH}" height="{HEIGHT}">')

    o.append('<style>')
    o.append(f'text{{font-family:"MS Gothic","Hiragino Kaku Gothic Pro","Yu Gothic",monospace;'
             f'font-size:{FONT_SIZE}px}}')

    # Head: pure white
    o.append('.h{fill:#fff}')
    # Near head: white-green
    o.append('.a{fill:#AAFFAA}')
    # Bright
    o.append('.b{fill:#4AFF4A}')
    # Phosphor green — the majority
    o.append('.c{fill:#00FF41}')
    o.append('.d{fill:#00EE38}')
    o.append('.e{fill:#00CC2E}')
    # Fading tail
    o.append('.f{fill:#00AA24;opacity:.7}')
    o.append('.g{fill:#008018;opacity:.45}')
    o.append('.i{fill:#005C12;opacity:.25}')
    o.append('.j{fill:#003D0E;opacity:.12}')

    # Fall
    o.append(f'@keyframes f{{0%{{transform:translateY(-{HEIGHT}px)}}100%{{transform:translateY({HEIGHT}px)}}}}')

    # Mutation flicker — char briefly dims then returns
    o.append('@keyframes m{0%,38%,42%,100%{opacity:inherit}40%{opacity:.1}}')

    # Per-column
    for col in range(COLS):
        dur = round(random.uniform(5.5, 11.0), 2)
        delay = round(random.uniform(-dur * 4, 0), 2)
        r = random.random()
        if r < 0.10:
            depth = round(random.uniform(0.25, 0.4), 2)
        elif r < 0.30:
            depth = round(random.uniform(0.5, 0.7), 2)
        else:
            depth = round(random.uniform(0.75, 1.0), 2)
        o.append(f'.c{col}{{animation:f {dur}s linear {delay}s infinite;opacity:{depth}}}')

    o.append('</style>')

    # Pure black background
    o.append(f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#000"/>')

    # Columns
    for col in range(COLS):
        x = col * COL_WIDTH + COL_WIDTH // 2
        o.append(f'<g class="c{col}">')

        row = 0
        while row < ROWS_NEEDED:
            stream_len = random.randint(12, 26)
            gap = random.randint(2, 7)

            for i in range(stream_len):
                if row >= ROWS_NEEDED:
                    break
                dist = stream_len - 1 - i

                if dist == 0:
                    cls = 'h'
                elif dist == 1:
                    cls = 'a'
                elif dist == 2:
                    cls = 'b'
                elif dist <= stream_len * 0.55:
                    cls = random.choice(['c', 'c', 'd'])
                elif dist <= stream_len * 0.7:
                    cls = 'e'
                elif dist <= stream_len * 0.8:
                    cls = 'f'
                elif dist <= stream_len * 0.9:
                    cls = 'g'
                elif dist <= stream_len * 0.95:
                    cls = 'i'
                else:
                    cls = 'j'

                y = row * ROW_HEIGHT
                char = rc()

                extra = ''
                if cls in ('c', 'd', 'e') and random.random() < 0.05:
                    mdur = round(random.uniform(1.5, 4.0), 1)
                    mdel = round(random.uniform(-5, 0), 1)
                    extra = f' style="animation:m {mdur}s steps(1) {mdel}s infinite"'

                o.append(f'<text x="{x}" y="{y}" class="{cls}"{extra}>{char}</text>')
                row += 1
            row += gap

        o.append('</g>')

    o.append('</svg>')
    return '\n'.join(o)


if __name__ == '__main__':
    print(generate_svg())
