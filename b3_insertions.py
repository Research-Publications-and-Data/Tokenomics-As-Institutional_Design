"""
Rebuild B3_GeoDePIN_Final.docx from source with 3 precise text insertions
+ Messari [45] reference + image replacements.
Run from ~/b2-governance-data/
"""

import zipfile, re, io
from pathlib import Path
from PIL import Image

B3_SRC = Path('b3/paper/B3_GeoDePIN_PostSurgery.docx')
B3_OUT = Path('b3/paper/B3_GeoDePIN_Final.docx')
EXH    = Path('exhibits/updated')

# ── Insertion texts (verbatim from spec) ─────────────────────────────────────

# Insertion 1: §3.2 S2R definition — scope statement (25 words)
# Cite: none
INS1 = (
    'S2R measures burns against algorithmic mining emissions only; vesting '
    'unlocks from team, investor, and ecosystem allocations are excluded because '
    'they represent pre-committed supply decisions rather than ongoing incentive '
    'costs that governance can adjust.'
)

# Insertion 2: §5.2 GEODNET trajectory (89 words)
# "(Messari, 2025)" → "[45]" to match IEEE-style numbering used throughout
INS2 = (
    'The trajectory is not monotonic: accelerating vesting unlocks in Q2\u202f2025 '
    '(monthly unlocks rose 60% from 23\u202fmillion to 30\u202fmillion tokens as '
    'team and investor allocations vested) temporarily overwhelmed subscription '
    'burn growth, collapsing the absorption rate despite a scheduled '
    'June\u202f30 halving that cut mining rewards by 50% [45]. '
    'By January\u202f2026, subscription growth had partially restored absorption '
    'to 62%. This pattern exposes a supply-side risk the S2R metric does not '
    'capture: vesting-driven dilution operates independently of emission schedules '
    'and can overwhelm organic demand even when the protocol\u2019s mining '
    'rewards are contracting.'
)

# Insertion 3: §7.3 Limitations (47 words)
# Cite: none (references §7.4 Future Work inline)
INS3 = (
    'The S2R metric as currently specified measures burns against mining '
    'emissions; it does not capture vesting-driven dilution from team, '
    'investor, and ecosystem unlocks, which for GEODNET represented 54% of '
    'total supply by Q2\u202f2025. A comprehensive fiscal sustainability metric '
    'would incorporate all supply sources; this extension is specified as a '
    'future research direction.'
)

# New reference [45] — Messari GEODNET quarterly report
REF45 = (
    '[45] Messari, \u201cGEODNET Quarterly Report Q2 2025,\u201d '
    'Messari Research, Jul. 2025. [Online]. Available: '
    'https://messari.io/research (Retrieved Apr. 2026).'
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def resize_image_bytes(src_path, target_w, target_h):
    img = Image.open(src_path).convert('RGBA')
    buf = io.BytesIO()
    img.resize((target_w, target_h), Image.LANCZOS).save(buf, format='PNG')
    return buf.getvalue()


def update_extents_for_rid(xml_str, rid_to_cx_cy):
    """Update wp:extent and a:ext for each drawing block containing a target rId."""
    blocks = xml_str.split('</wp:inline>')
    for i, block in enumerate(blocks[:-1]):
        for rid, (new_cx, new_cy) in rid_to_cx_cy.items():
            if f'r:embed="{rid}"' in block:
                block = re.sub(
                    r'(<wp:extent\s+cx=")(\d+)("\s+cy=")(\d+)(")',
                    rf'\g<1>{new_cx}\g<3>{new_cy}\g<5>', block)
                block = re.sub(
                    r'(<a:ext\s+cx=")(\d+)("\s+cy=")(\d+)(")',
                    rf'\g<1>{new_cx}\g<3>{new_cy}\g<5>', block)
                blocks[i] = block
                print(f'  ✓ extents updated for {rid}: {new_cx}×{new_cy} EMU')
    return '</wp:inline>'.join(blocks)


def insert_para_after_anchor(xml, anchor_phrase, para_text):
    """
    Insert a new paragraph immediately after the </w:p> that contains anchor_phrase.
    Inherits pPr and rPr from the host paragraph.
    """
    if anchor_phrase not in xml:
        print(f'  ⚠️  Anchor not found: "{anchor_phrase[:70]}"')
        return xml

    idx     = xml.index(anchor_phrase)
    p_end   = xml.index('</w:p>', idx) + len('</w:p>')
    p_start = xml.rfind('<w:p ', 0, idx)
    if p_start == -1:
        p_start = xml.rfind('<w:p>', 0, idx)
    host = xml[p_start:p_end]

    ppr_m = re.search(r'<w:pPr>.*?</w:pPr>', host, re.DOTALL)
    ppr   = ppr_m.group(0) if ppr_m else ''
    rpr_m = re.search(r'<w:rPr>.*?</w:rPr>', host, re.DOTALL)
    rpr   = rpr_m.group(0) if rpr_m else ''

    safe = (para_text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;'))

    new_para = (
        f'<w:p>{ppr}'
        f'<w:r>{rpr}'
        f'<w:t xml:space="preserve">{safe}</w:t>'
        f'</w:r></w:p>'
    )
    result = xml[:p_end] + new_para + xml[p_end:]
    print(f'  ✓ Paragraph inserted after anchor: "{anchor_phrase[:60]}..."')
    return result


def transform_b3_xml(xml):
    # ── Image extent updates ──────────────────────────────────────────────────
    rid_cx_cy = {}
    for rid, img_path, orig_cx in [
        ('rId10', EXH / 'b3_fig2_who_burns.png',          4572000),
        ('rId11', EXH / 'b3_fig3_geodnet_trajectory.png', 4572000),
    ]:
        img = Image.open(img_path)
        w, h = img.size
        rid_cx_cy[rid] = (orig_cx, int(orig_cx * h / w))
    xml = update_extents_for_rid(xml, rid_cx_cy)

    # ── Insertion 1: §3.2 — after "avoid conflating irreversible and reversible demand." ──
    # This is the final sentence of para 126.
    xml = insert_para_after_anchor(
        xml,
        anchor_phrase='avoid conflating irreversible and reversible demand.',
        para_text=INS1,
    )

    # ── Insertion 2: §5.2 GEODNET — after entire para 203 ────────────────────
    # Para 203 ends with "...demand resilience beyond speculative token use."
    # The insertion goes AFTER this paragraph (before the blank para / figure).
    xml = insert_para_after_anchor(
        xml,
        anchor_phrase='demand resilience beyond speculative token use.',
        para_text=INS2,
    )

    # ── Insertion 3: §7.3 — after "survivorship bias" sentence in para 267 ──
    # Para 267 ends with "...would strengthen external validity."
    # That paragraph contains the survivorship sentence and closes with "external validity."
    xml = insert_para_after_anchor(
        xml,
        anchor_phrase='direct replication across multiple protocols would strengthen external validity.',
        para_text=INS3,
    )

    # ── Reference [45]: append after [44] ────────────────────────────────────
    # [44] ends with "2016."
    anchor_44 = (
        'Customer concentration risk and the cost of equity capital,'
        '&#8221; J. Account. Econ., vol. 61, no. 1, pp. 23\u201348, 2016.'
    )
    # Try decoded version first
    alt_44 = 'pp. 23\u201348, 2016.'
    if alt_44 in xml:
        xml = insert_para_after_anchor(xml, alt_44, REF45)
    else:
        # Fallback: search for [44] literally
        if '[44]' in xml:
            idx44 = xml.rindex('[44]')  # last occurrence = actual ref entry
            p_end44 = xml.index('</w:p>', idx44) + len('</w:p>')
            p_start44 = xml.rfind('<w:p ', 0, idx44)
            host44 = xml[p_start44:p_end44]
            rpr_m44 = re.search(r'<w:rPr>.*?</w:rPr>', host44, re.DOTALL)
            rpr44 = rpr_m44.group(0) if rpr_m44 else ''
            safe_ref = REF45.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            new_ref_para = f'<w:p><w:r>{rpr44}<w:t xml:space="preserve">{safe_ref}</w:t></w:r></w:p>'
            xml = xml[:p_end44] + new_ref_para + xml[p_end44:]
            print('  ✓ Reference [45] appended after [44]')
        else:
            print('  ⚠️  [44] anchor not found — reference not added')

    return xml


# ── Build ─────────────────────────────────────────────────────────────────────
print('Building B3_GeoDePIN_Final.docx from source...')

image_replacements = {
    'word/media/image2.png': resize_image_bytes(EXH / 'b3_fig2_who_burns.png',         2370, 1655),
    'word/media/image3.png': resize_image_bytes(EXH / 'b3_fig3_geodnet_trajectory.png', 2544, 1507),
}
print(f'  images prepared: {list(image_replacements.keys())}')

with zipfile.ZipFile(B3_SRC, 'r') as zin, \
     zipfile.ZipFile(B3_OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename in image_replacements:
            data = image_replacements[item.filename]
        if item.filename == 'word/document.xml':
            data = transform_b3_xml(data.decode('utf-8')).encode('utf-8')
        zout.writestr(item, data)

print(f'\n  ✓ {B3_OUT} written ({B3_OUT.stat().st_size / 1024:.0f} KB)')


# ── Verify ────────────────────────────────────────────────────────────────────
print('\nVerification:')
from docx import Document

doc = Document(str(B3_OUT))
text = ' '.join(p.text for p in doc.paragraphs)
n_images = sum(1 for r in doc.part.rels.values() if 'image' in r.reltype.lower())

checks = {
    # Existing content preserved
    'S2R 2.06 retained':          '2.06' in text,
    'Resource Dependence retained': 'Resource Dependence' in text,
    'Who Burns retained':          'Who Burns' in text,
    'images ≥ 4':                  n_images >= 4,

    # Insertion 1 (§3.2)
    'Ins1: pre-committed supply decisions': 'pre-committed supply decisions' in text,
    'Ins1: governance can adjust':          'governance can adjust' in text,

    # Insertion 2 (§5.2 GEODNET)
    'Ins2: vesting-driven dilution':        'vesting-driven dilution' in text,
    'Ins2: June 30 halving [45]':           '[45]' in text and 'mining rewards by 50%' in text,
    'Ins2: 23 million to 30 million':       '23' in text and '30' in text and 'million tokens' in text,
    'Ins2: by January 2026':               'January' in text and '62%' in text,

    # Insertion 3 (§7.3)
    'Ins3: 54% total supply Q2 2025':      '54%' in text and 'Q2' in text,
    'Ins3: future research direction':      'future research direction' in text,

    # Reference [45]
    'Ref [45] Messari GEODNET':            '[45]' in text and 'GEODNET Quarterly' in text,

    # Output file
    'B3_GeoDePIN_Final.docx exists':       B3_OUT.exists(),
}

all_pass = True
for name, passed in checks.items():
    status = '✓' if passed else '✗'
    if not passed:
        all_pass = False
    print(f'  {status}  {name}')

print(f'\n  B3: {len(text.split()):,} words, {n_images} images')
print(f'\n{"  ALL CHECKS PASS" if all_pass else "  FAILURES — see ✗ above"}')
