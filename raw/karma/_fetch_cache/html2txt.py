# One-off converter: budsas HTML -> plain text (giữ nguyên văn, bỏ ads/nav)
import re, sys, html as h

def convert(path):
    html = open(path, encoding='utf-8', errors='replace').read()
    # cắt head + scripts/styles/ads
    html = re.sub(r'(?s)<head.*?</head>', '', html, flags=re.I)
    html = re.sub(r'(?s)<script.*?</script>', '', html, flags=re.I)
    html = re.sub(r'(?s)<style.*?</style>', '', html, flags=re.I)
    html = re.sub(r'(?s)<ins .*?</ins>', '', html, flags=re.I)
    # block tags -> newline
    html = re.sub(r'(?i)<br\s*/?>', '\n', html)
    html = re.sub(r'(?i)</(p|div|blockquote|h[1-6]|li|tr|ol|ul)>', '\n\n', html)
    html = re.sub(r'(?i)<hr[^>]*>', '\n----\n', html)
    # strip remaining tags
    html = re.sub(r'(?s)<[^>]+>', '', html)
    text = h.unescape(html)
    # normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r' ?\n ?', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

if __name__ == '__main__':
    for path in sys.argv[1:]:
        out = path.rsplit('.', 1)[0] + '.txt'
        text = convert(path)
        open(out, 'w', encoding='utf-8').write(text)
        print(out, len(text), 'chars')
