"""Dark design board (.dc.html) -> light theme.

Light tokens = Stipop FANZA design system (code: constants/darkPalette.js light values):
bg #f6f6f9, sidebar/surface #ffffff, surface-2 #f1f0f6, line rgba(20,16,40,.08), ink #17151f, sub #6c6878.
Brand gradients, photo overlays, dark scrims and point-yellow keep their colors (and their children too).
"""
import re, sys, colorsys

HEX = re.compile(r'#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b')
WHITE_A = re.compile(r'rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*([0-9.]+)\s*\)')
VOID = {'img', 'br', 'input', 'link', 'meta', 'hr', 'source', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon',
        'stop', 'use', 'ellipse', 'col', 'wbr', 'dc-import'}
KEEP_TOKENS = ['rgba(15,13,23', 'rgba(0,0,0', 'rgba(11,10,16', 'url(', '#000000', '#000;', '#000)']


def hsl(h):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    return hh, s, l


def to_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return '#%02x%02x%02x' % tuple(round(x * 255) for x in (r, g, b))


def is_brand(hx):
    """Saturated mid/bright colours (brand pink/violet, tones, yellow): keep, and keep their children."""
    h, s, l = hsl(hx)
    return s > 0.45 and 0.35 < l < 0.85 and not (l > 0.72 and s < 0.6)


def bg_hex(hx):
    h, s, l = hsl(hx)
    if l < 0.3:
        if s < 0.4 or l < 0.12:
            if l < 0.075: return '#f6f6f9'
            if l < 0.13: return '#ffffff'
            return '#f1f0f6'
        return to_hex(h, min(0.7, s), 0.95)       # dark tinted chip -> light tint of same hue
    return hx


BRAND = {'#ff3d7f', '#c04dff', '#6f5bff', '#7c5cff', '#8b5cf6', '#ff6d24', '#f97316', '#ef4444', '#3b82f6', '#e11d63'}


def text_hex(hx):
    if hx in BRAND:
        return hx
    h, s, l = hsl(hx)
    chroma = s * (1 - abs(2 * l - 1))           # real colourfulness
    if 0.1 <= h <= 0.17 and chroma > 0.25 and l >= 0.5:
        return '#b45309'                         # yellow/amber text -> readable amber
    if l >= 0.6:
        if chroma < 0.12:                        # near-white / grey text -> ink tiers
            if l > 0.9: return '#17151f'
            if l > 0.75: return '#3d3a4a'
            return '#6c6878'
        if chroma < 0.7:                         # pastel accent -> deeper same hue
            return to_hex(h, min(s, 0.8), 0.42)
        return hx
    if 0.45 <= l < 0.6 and chroma < 0.12:
        return '#8a8698'
    return hx


def sub_hex(v, fn):
    return HEX.sub(lambda m: fn(m.group(0).lower()), v)


DARK_A = re.compile(r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([0-9.]+)\s*\)')


def bg_value(v):
    v = sub_hex(v, bg_hex)
    v = DARK_A.sub(lambda m: ('rgba(255,255,255,%s)' % m.group(4)) if max(int(m.group(1)), int(m.group(2)), int(m.group(3))) < 60 and float(m.group(4)) >= 0.8 and 'gradient' not in v else m.group(0), v)
    return WHITE_A.sub(lambda m: 'rgba(20,16,40,%s)' % round(min(float(m.group(1)) * 0.8, 0.12), 3), v)


def text_value(v):
    v = sub_hex(v, text_hex)
    return WHITE_A.sub(lambda m: 'rgba(23,21,31,%s)' % m.group(1), v)


def border_value(v):
    def f(hx):
        h, s, l = hsl(hx)
        if l < 0.3 and s < 0.4:
            return 'rgba(20,16,40,0.10)' if l > 0.12 else '#ffffff'
        return text_hex(hx)
    v = sub_hex(v, f)
    return WHITE_A.sub(lambda m: 'rgba(20,16,40,%s)' % round(min(float(m.group(1)) + 0.02, 0.14), 3), v)


def bg_decls(style):
    return ';'.join(d for d in style.split(';') if d.strip().lower().startswith('background'))


def is_keep(style):
    bg = bg_decls(style).lower()
    if not bg:
        return False
    if any(k in bg.replace(' ', '') for k in KEEP_TOKENS):
        return True
    hexes = HEX.findall(bg)
    if any(is_brand(x) for x in hexes):
        return True
    # dark gradient placeholders behind photos
    if 'gradient' in bg and hexes and all(hsl(x)[2] < 0.3 for x in hexes) and any(hsl(x)[1] >= 0.4 for x in hexes):
        return True
    return False


def conv_style(style):
    out = []
    for d in style.split(';'):
        if ':' not in d:
            out.append(d); continue
        p, v = d.split(':', 1)
        pl = p.strip().lower()
        if pl.startswith('background'):
            if not is_keep(d):
                v = bg_value(v)
        elif pl in ('color', 'fill', 'stroke', 'caret-color', 'accent-color'):
            v = text_value(v)
        elif pl.startswith('border') or pl.startswith('outline'):
            v = border_value(v)
        elif pl in ('box-shadow', 'text-shadow'):
            v = WHITE_A.sub(lambda m: 'rgba(20,16,40,%s)' % m.group(1), v)
            v = re.sub(r'rgba\(0,\s*0,\s*0,\s*([0-9.]+)\)', lambda m: 'rgba(20,16,40,%s)' % round(float(m.group(1)) * 0.35, 3), v)
        out.append(p + ':' + v)
    return ';'.join(out)


TAG = re.compile(r'<(/?)([a-zA-Z][\w-]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*?)(/?)>', re.S)


def photo_parents(body):
    """Ordinals of open tags whose direct child is a covering photo (text on it must stay light)."""
    keep, stack, n = set(), [], 0
    for m in TAG.finditer(body):
        close, name, attrs, selfc = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if close:
            if stack: stack.pop()
            continue
        n += 1
        st = re.search(r'style="([^"]*)"', attrs)
        st = st.group(1) if st else ''
        if name == 'svg' and '<lineargradient' in body[m.end():body.find('</svg>', m.end())].lower():
            keep.add(n)
        if name == 'img' and 'object-fit: cover' in st and ('position: absolute' in st or 'inset' in st) and stack:
            keep.add(stack[-1])
        if not selfc and name not in VOID:
            stack.append(n)
    return keep


def convert(html):
    head, sep, rest = html.partition('</helmet>')
    head = re.sub(r'background:\s*#0b0a10', 'background:#f6f6f9', head)
    head = re.sub(r'(a\{color:)(#[0-9a-fA-F]{3,6})', lambda m: m.group(1) + text_hex(m.group(2).lower()), head)
    body, sep2, tail = rest.partition('</x-dc>')
    photos = photo_parents(body)
    out, pos, stack, n = [], 0, [False], 0
    for m in TAG.finditer(body):
        out.append(body[pos:m.start()]); pos = m.end()
        close, name, attrs, selfc = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if close:
            if len(stack) > 1: stack.pop()
            out.append(m.group(0)); continue
        n += 1
        dark = stack[-1]
        sm = re.search(r'style="([^"]*)"', attrs)
        style = sm.group(1) if sm else ''
        keep_here = is_keep(style) or n in photos
        if not dark:
            if sm and not keep_here:
                attrs = attrs.replace('style="%s"' % style, 'style="%s"' % conv_style(style), 1)
            elif sm and n in photos and not is_keep(style):
                conv = ';'.join(d if d.split(':', 1)[0].strip().lower() == 'color' else conv_style(d) for d in style.split(';'))
                attrs = attrs.replace('style="%s"' % style, 'style="%s"' % conv, 1)
            if not keep_here:
                for a in ('stroke', 'fill'):
                    attrs = re.sub(r'(\s%s=")([^"]*)"' % a, lambda mm: mm.group(1) + text_value(mm.group(2)) + '"', attrs)
        out.append('<' + m.group(2) + attrs + selfc + '>')
        if not selfc and name not in VOID:
            stack.append(dark or keep_here)
    out.append(body[pos:])
    return head + sep + ''.join(out) + sep2 + tail


if __name__ == '__main__':
    open(sys.argv[2], 'w').write(convert(open(sys.argv[1]).read()))
