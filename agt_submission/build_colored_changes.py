"""Build a minimally marked comparison to the accepted article."""
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'agt_submission'
BASE = '6e23f50a836f2437f624fc83c1c04cf8bfd0df53'

def source(name, old):
    if old:
        return subprocess.check_output(['git', 'show', f'{BASE}:{name}'], cwd=ROOT, text=True)
    return (ROOT / name).read_text()

def flatten(name, old):
    text = source(name, old)
    text = re.sub(r'(?m)(?<!\\)%.*$', '', text)
    def include(match):
        target = match[1]
        if not Path(target).suffix:
            target += '.tex'
        return '\n' + flatten(target, old) + '\n'
    text = re.sub(r'\\input\{([^}]+)\}', include, text)
    # Identical rendered notation must not be marked as a change.
    return text.replace(r'^{\mathrm{st}}', r'^\st').replace(r'^{\st}', r'^\st')

old, new = flatten('vr_st.tex', True), flatten('vr_st.tex', False)
protected = {}
def protect(before, after, marked):
    global old, new
    assert before in old, before
    assert after in new, after
    token = r'\AGT' + chr(65 + len(protected)//26) + chr(65 + len(protected)%26)
    old = old.replace(before, token)
    new = new.replace(after, token)
    protected[token] = marked

protect(r'$\img_\theta(\cM) \neq 0$.', '\\[\n\t\\img_\\theta(\\cM) \\neq 0\n\t\\quad\\text{and}\\quad\n\t\\dim \\opH_m(\\cM) = 1.\n\t\\]', r'\[\img_\theta(\cM)\neq0\quad\newmath{\text{and}\quad\dim\opH_m(\cM)=1}.\]')

protect(r'\theta_{\cX}^{[f]}(g^*(\iota_m))', r'\theta_{\cX}^{[f]}(g^*(\iota_n))', r'\theta_{\cX}^{[f]}(g^*(\iota_{\oldmath{m}\newmath{n}}))')
protect(r'\set{\theta^n \in \cO(n,\pi ; n+k,G)}', r'\set{\theta^n \in \cO(\pi, n; G, n+k)}', r'\set{\theta^n \in \cO(\oldmath{n,\pi}\newmath{\pi,n};\oldmath{n+k,G}\newmath{G,n+k})}')
for op in ('img', 'ker'):
    protect('\\'+op+r'(\theta_s)', '\\'+op+r'(\theta_t)', '\\'+op+r'(\theta_{\oldmath{s}\newmath{t}})')
for formula in (r'\Sq^i(\alpha) = 0, \quad \text{if } i > \deg\alpha', r'\Sq^i(\alpha) = \alpha^2, \quad \text{if } i = \deg\alpha'):
    protect(r'\('+formula+r'.\)', r'\('+formula+r',\)', r'\('+formula+r'\oldmath{.}\newmath{,}\)')
protect(r'$\crit(\rp^n)=\frac{2\pi}{3}$', r'$2\crit(\rp^n)=\frac{2\pi}{3}$', r'$\newmath{2}\crit(\rp^n)=\frac{2\pi}{3}$')
protect(r'\(\rH^\ast(\rp^n; \Ftwo) \cong \frac{\Ftwo[\sigma]}{(\sigma^{n+1} = 1)}.\)', r'\(\rH^\ast(\rp^n; \Ftwo) \cong \frac{\Ftwo[\sigma]}{(\sigma^{n+1})}.\)', r'\(\rH^\ast(\rp^n; \Ftwo) \cong \frac{\Ftwo[\sigma]}{(\sigma^{n+1}\oldmath{=1})}.\)')
protect(r'$\cost(Q) = \|(0,\gamma_\theta ) - (a,b)\|_\infty \geq a \geq \zeta_n$', r'$\cost(Q) \geq \|(0,\gamma_\theta ) - (a,b)\|_\infty \geq a \geq \zeta_n$', r'$\cost(Q) \oldmath{=}\newmath{\geq} \|(0,\gamma_\theta ) - (a,b)\|_\infty \geq a \geq \zeta_n$')
protect(r'$\firstdeath{\Sq^k}{\rp^n} = \tfrac{2\pi}{3}$', r'$\firstdeath{\Sq^k}{\rp^n} = \tfrac{\pi}{3}$', r'$\firstdeath{\Sq^k}{\rp^n} = \tfrac{\oldmath{2}\pi}{3}$')
protect(r'$n,k,\Sq^k$', r'$n,m,k,\Sq^k$', r'$n,\newmath{m,}k,\Sq^k$')
protect(r'\(m \leq n\), \(k \leq \tfrac{n-1}{2}\),', r'\(0 < k \leq m \leq n\)', r'\(\newmath{0 < k \leq{}}m \leq n\)\DIFdel{, }\(\oldmath{k \leq \tfrac{n-1}{2}}\)\DIFdel{,}')
protect(r'\(\opH_m(\cM)\) is non-zero', r'\(\dim \opH_m(\cM) = 1\)', r'\(\newmath{\dim{}}\opH_m(\cM)\newmath{{}=1}\)\DIFdel{ is non-zero}')
protect(r'\(\bS^{u_i}\)', r'\(\bS^i\)', r'\(\bS^{\oldmath{u_i}\newmath{i}}\)')
# Preserve complete cases structure and mark only the changed condition.
before = r'\tfrac{\pi}{3} & k \leq \frac{n-1}{2} \text{ and }'
after = r'\tfrac{\pi}{3} & m \leq n \text{ and }'
protect(before, after, r'\tfrac{\pi}{3} & \oldmath{k \leq \frac{n-1}{2}}\newmath{m\leq n}\text{ and }')
# Citation labels are unchanged; mark only changed visible locators.
protect(r'\cite[Cor.~2.25.]{hatcher2000}', r'\cite[Corollary~2.25]{hatcher2000}', r'\cite[\DIFdel{Cor.}\DIFadd{Corollary}~2.25\DIFdel{.}]{hatcher2000}')
protect(r'\cite[Thm.~1.9 \& 1.10]{blumberg2023interleaving}', r'\cite[Theorems~1.9 and~1.10]{blumberg2023interleaving}', r'\cite[\DIFdel{Thm.}\DIFadd{Theorems}~1.9 \DIFdel{\&}\DIFadd{and}~1.10]{blumberg2023interleaving}')
for a, b in [('Thm.', 'Theorem'), ('Prop.', 'Proposition'), ('Cor.', 'Corollary'), ('Defn.', 'Definition'), ('p.', 'page')]:
    for match in list(re.finditer(r'\\cite\[('+re.escape(a)+r'~[^\]]+)\]\{[^}]+\}', old)):
        before = match[0]
        after = before.replace(a+'~', b+'~')
        if after in new:
            protect(before, after, before.replace(a, r'\DIFdel{'+a+r'}\DIFadd{'+b+'}', 1))
protect(r'\fillrad(\rL^1_q)', r'\fillrad(\rL^0_q)', r'\fillrad(\rL^{\oldmath{1}\newmath{0}}_q)')
protect(r'\fillrad(\rL^1_p)', r'\fillrad(\rL^0_p)', r'\fillrad(\rL^{\oldmath{1}\newmath{0}}_p)')
protect(r'\tfrac{1}{q} \fillrad', r'\tfrac{1}{2} \fillrad', r'\tfrac{1}{\oldmath{q}\newmath{2}} \fillrad')
protect(r'$1\leq \tilde{n} \leq n$', r'$0\leq \tilde{n} \leq n$', r'$\oldmath{1}\newmath{0}\leq \tilde{n} \leq n$')
with tempfile.TemporaryDirectory(prefix='vr-st-colored-') as temp:
    temp = Path(temp)
    (temp / 'old.tex').write_text(old)
    (temp / 'new.tex').write_text(new)
    result = subprocess.run(['latexdiff', '--math-markup=3', '--config', 'MINWORDSBLOCK=1', '--disable-citation-markup', str(temp/'old.tex'), str(temp/'new.tex')], text=True, capture_output=True, check=True)
    diff = result.stdout
for token, marked in protected.items():
    diff = diff.replace(token, marked)
diff = diff.replace(r'\addbibresource{aux/bibliography.bib}', r'\addbibresource{../aux/bibliography.bib}')
custom = r'''
\usepackage{cancel}
\definecolor{deletedpurple}{RGB}{128,32,160}
\definecolor{darkblue}{rgb}{0,0,0}
\renewcommand{\DIFadd}[1]{{\color{red}#1}}
\renewcommand{\DIFdel}[1]{{\color{deletedpurple}\ifmmode\oldmath{#1}\else\sout{#1}\fi}}
\renewcommand{\DIFaddFL}[1]{\DIFadd{#1}}
\renewcommand{\DIFdelFL}[1]{\DIFdel{#1}}
\newcommand{\oldmath}[1]{{\color{deletedpurple}\mathpalette\horizontalstrike{#1}}}
\newcommand{\horizontalstrike}[2]{\sbox0{$#1#2$}\rlap{\raisebox{.5\ht0}{\rule{\wd0}{.4pt}}}\usebox0}
\newcommand{\newmath}[1]{{\color{red}#1}}
\AtEveryBibitem{\iffieldequalstr{entrykey}{barham2025group}{\color{red}}{}}
\hypersetup{allcolors=black}
\AtBeginDocument{\sloppy\emergencystretch=3em}
'''
diff = diff.replace(r'\begin{document}', custom + '\n'+r'\begin{document}', 1)
(OUT / 'annotated_article.tex').write_text(diff)

def escape(text):
    table = {'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(table.get(c,c) for c in text).replace('—','---').replace('–','--')

paragraphs = (OUT / 'final_upload/change_list.txt').read_text().split('\n\n')[2:]
body = []
for paragraph in paragraphs:
    paragraph = paragraph.strip()
    if not paragraph or paragraph.startswith('7.3.'):
        continue
    paragraph = paragraph.replace(' Standardized the source notation for the superscript “st”.','')
    paragraph = paragraph.replace(" and in the existing personal-communication bibliography entry",'')
    if re.match(r'^\d+\. ', paragraph):
        body.append(r'\subsection*{' + escape(paragraph) + '}')
    else:
        for line in paragraph.splitlines():
            body.append(escape(line.strip()) + '\n\n')
# Preserve the editor-facing list, which is maintained directly in TeX.
if not (OUT / 'change_list_body.tex').exists():
    (OUT / 'change_list_body.tex').write_text('\n'.join(body))
