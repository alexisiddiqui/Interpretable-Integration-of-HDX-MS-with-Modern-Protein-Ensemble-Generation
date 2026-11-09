#!/usr/bin/env python3
"""Apply thesis presentation to the four archived jax-Ka SVG figures.

Run with Python containing matplotlib and Pillow, plus rsvg-convert on PATH:
    MPLCONFIGDIR=/tmp/jaxka-mpl python figures/style_jaxka_artwork.py

SVGs are the editable artwork sources. This idempotent pass removes figure-level
methods footnotes, changes the width-control legend, crops unused whitespace and
exports PDF/PNG. It checks that every axes group remains identical after
XML parsing and whitespace normalisation. Numerical summaries and data files are
not modified. If the original cluster plotting scripts regenerate the SVGs, rerun
this pass before compiling. PDF export composites embedded image transparency
onto the white axes background to avoid Cairo edge artefacts; vectors stay intact.
"""
from pathlib import Path
import copy
import base64
import io
import os
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

os.environ.setdefault('MPLCONFIGDIR', '/tmp/jaxka-mpl')
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextToPath
from matplotlib.path import Path as MplPath
from PIL import Image, ImageChops

FIGURES = Path(__file__).resolve().parent
SVG = '{http://www.w3.org/2000/svg}'
OLD_LEGEND = 'Width only, no explicit sequence edges'
NEW_LEGEND = 'Width controls, no relation maps'
FOOTERS = {
    'jaxka-relational-edges': '50% training pool',
    'jaxka-relational-memory': 'Left: 300 PINDER graphs',
    'jaxka-component-cutoffs': 'PROPKA 3.5.1, fixed coordinates',
    'jaxka-gap-cutoffs': 'Rows: terminal gaps',
}


def parse(source):
    return ET.fromstring(source, ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))


def axes(source):
    result = {}
    for g in parse(source).iter(SVG+'g'):
        if g.attrib.get('id', '').startswith('axes_'):
            node = copy.deepcopy(g)
            for element in node.iter():
                element.attrib.update({k: ' '.join(v.split()) for k,v in element.attrib.items()})
                if element.text is not None and not element.text.strip(): element.text = None
                if element.tail is not None and not element.tail.strip(): element.tail = None
            node.tail = None
            result[g.attrib['id']] = ET.tostring(node)
    return result


def text_group(source, prefix):
    for g in parse(source).iter(SVG+'g'):
        if g.attrib.get('id', '').startswith('text_'):
            if any(c.tag is ET.Comment and c.text.strip().startswith(prefix) for c in g):
                return g.attrib['id']
    return None


def span(source, identifier):
    match = re.search(r'<g\s+id="'+re.escape(identifier)+r'"[^>]*>', source)
    assert match, identifier
    depth = 0
    for tag in re.finditer(r'<g\b[^>]*>|</g>', source[match.start():]):
        depth += -1 if tag.group() == '</g>' else 1
        if not depth:
            return match.start(), match.start()+tag.end()
    raise ValueError('Unclosed SVG group '+identifier)


def replace_group(source, identifier, replacement):
    start, end = span(source, identifier)
    removed = source[start:end]
    # Glyph definitions nested in removed text may also be used by later labels.
    definitions = re.findall(r'<defs>(.*?)</defs>', removed, re.S)
    source = source[:start]+replacement+source[end:]
    if definitions:
        source = source.replace('<defs>', '<defs>\n'+'\n'.join(definitions), 1)
    return source


def legend_path(label):
    vertices, codes = TextToPath().get_text_path(FontProperties(family='DejaVu Sans', size=100), label)
    path = MplPath(vertices, codes)
    command = {MplPath.MOVETO:'M', MplPath.LINETO:'L', MplPath.CURVE3:'Q', MplPath.CURVE4:'C'}
    parts = []
    for points, code in path.iter_segments(curves=True, simplify=False):
        parts.append('Z' if code == MplPath.CLOSEPOLY else
                     command[code]+' '+' '.join(f'{x:.6f}' for x in points))
    return ' '.join(parts)


def update(source, prefix):
    before = axes(source)
    identifier = text_group(source, prefix)
    if identifier:
        source = replace_group(source, identifier, '')
    identifier = text_group(source, OLD_LEGEND)
    if identifier:
        a,b = span(source, identifier)
        transform = re.search(r'<g transform="([^"]+)"', source[a:b]).group(1)
        replacement = (f'<g id="{identifier}">\n    <!-- {NEW_LEGEND} -->\n'
                       f'    <g transform="{transform}"><path d="{legend_path(NEW_LEGEND)}"/></g>\n   </g>')
        source = replace_group(source, identifier, replacement)
    assert axes(source) == before, 'A plotted axes group changed'
    assert text_group(source, prefix) is None
    assert text_group(source, OLD_LEGEND) is None
    return source


def crop(source):
    # Measure ink bounds on a temporary rendering; keep all scientific marks.
    with tempfile.TemporaryDirectory(prefix='jaxka-svg-') as directory:
        probe = Path(directory)/'probe.svg'; png = Path(directory)/'probe.png'
        probe.write_text(source)
        subprocess.run(['rsvg-convert','--dpi-x','72','--dpi-y','72','-o',str(png),str(probe)],check=True)
        with Image.open(png) as im:
            canvas = Image.new('RGB',im.size,'white')
            if im.mode == 'RGBA': canvas.paste(im,mask=im.getchannel('A'))
            else: canvas.paste(im.convert('RGB'))
            bbox = ImageChops.difference(canvas,Image.new('RGB',canvas.size,'white')).convert('L').point(lambda p:255 if p>3 else 0).getbbox()
            width,height = canvas.size
    x,y,w,h = map(float,parse(source).attrib['viewBox'].split())
    left=x+bbox[0]*w/width-7.2; top=y+bbox[1]*h/height-7.2
    right=x+bbox[2]*w/width+7.2; bottom=y+bbox[3]*h/height+7.2
    # Original backgrounds are white and cover the complete retained viewport.
    def viewport(match):
        tag=match.group()
        for key,value in [('width',f'{right-left:.6f}pt'),('height',f'{bottom-top:.6f}pt'),
                          ('viewBox',f'{left:.6f} {top:.6f} {right-left:.6f} {bottom-top:.6f}')]:
            tag=re.sub(key+r'="[^"]+"',key+'="'+value+'"',tag)
        return tag
    return re.sub(r'<svg\b[^>]+>',viewport,source,count=1)


def backdrop(source):
    x,y,w,h=map(float,parse(source).attrib['viewBox'].split())
    start,end=span(source,'patch_1')
    path=f'M {x} {y} L {x+w} {y} L {x+w} {y+h} L {x} {y+h} Z'
    group=re.sub(r'(?<![\w-])d="[^"]+"','d="'+path+'"',source[start:end],count=1)
    return source[:start]+group+source[end:]


def export_pdf(source, output):
    def opaque(match):
        im = Image.open(io.BytesIO(base64.b64decode(match[1]))).convert('RGBA')
        white = Image.new('RGBA', im.size, 'white')
        white.alpha_composite(im)
        encoded = io.BytesIO()
        white.convert('RGB').save(encoded, format='PNG')
        return 'data:image/png;base64,'+base64.b64encode(encoded.getvalue()).decode()
    # Cairo's PDF image masks can introduce dark cell boundaries on resampling.
    # Only the temporary export copy composites those images onto their white
    # axes background; canonical SVG groups and density values remain unchanged.
    with tempfile.TemporaryDirectory(prefix='jaxka-pdf-') as directory:
        temporary = Path(directory)/'export.svg'
        temporary.write_text(re.sub(r'data:image/png;base64,([^"]+)', opaque, source))
        subprocess.run(['rsvg-convert', '-f', 'pdf', '-o', str(output), str(temporary)], check=True)


def main():
    for folder,prefix in FOOTERS.items():
        path=FIGURES/folder/'fig.svg'; original=path.read_text()
        source=update(original,prefix)
        # Crop only when removing the original footnote, avoiding repeated raster rounding.
        if text_group(original,prefix): source=crop(source)
        source=backdrop(source)
        source='\n'.join(line.rstrip() for line in source.splitlines())+'\n'
        assert axes(original)==axes(source)
        path.write_text(source)
        export_pdf(source, path.with_suffix('.pdf'))
        subprocess.run(['rsvg-convert','--dpi-x','190','--dpi-y','190','-o',str(path.with_suffix('.png')),str(path)],check=True)
        print(folder+': artwork exported; plotted axes unchanged')


if __name__ == '__main__':
    main()
