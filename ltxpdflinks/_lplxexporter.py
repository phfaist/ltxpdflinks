import os
import os.path
import logging
logger = logging.getLogger(__name__)

def _makeltxsafe(s):
    return s.replace('{', '\{').replace('}','\}').replace('\n', ' ')


class LplxPictureEnvExporter:
    def __init__(self):
        super().__init__()

    def export(self, extractedgraphiclinks):
        e = extractedgraphiclinks # shorthand
        graphic_basefname, graphic_ext = os.path.splitext(e.graphic_fname)

        s = \
r"""% LPLX file for """ + _makeltxsafe(e.graphic_fname) + r"""
%
\begingroup
\def\lplxiGraphicFname{""" + _makeltxsafe(e.graphic_fname) + r"""}%
\def\lplxiGraphicBaseFname{""" + _makeltxsafe(graphic_basefname) + r"""}%
\def\lplxiGraphicExt{""" + _makeltxsafe(graphic_ext) + r"""}%
\lplxIncludeGraphics
\lplxSetBbox{0}{0}""" + "{{{:.6g}}}{{{:.6g}}}".format(e.size[0], e.size[1]) + r"""%
%%BoundingBox: 0 0 """ + "{:d} {:d}".format(int(e.size[0]), int(e.size[1])) + r"""
%%HiResBoundingBox: 0 0 """ + "{:.6g} {:.6g}".format(e.size[0], e.size[1]) + r"""
\unitlength=""" + e.unitlength + r"""\relax
\lplxSetupScaleAndBbox
\lplxaDoScale{%
\begin{picture}(\lplxvCropW,\lplxvCropH)(\lplxvCropX,\lplxvCropY)%
"""

        for el in e.links:
            x, y, w, h = el.link_bbox
            if el.link_type == 'URI':
                s2 = r"""\href{{{tgt}}}""".format(tgt=el.link_target)
            elif el.link_type == 'latex-ref':
                s2 = r"""\hyperref[{tgt}]""".format(tgt=el.link_target)
            elif el.link_type == 'latex-cite':
                s2 = r"""\hyperlink{{cite.{tgt}}}""".format(tgt=el.link_target)
            else:
                logger.warning("Ignoring link with unsupported link_type: %r", el)
                continue

            # s += (
            #     r"\put({x},{y})".format(x=el.link_bbox[0], y=el.link_bbox[1]) +
            #     "{" + s2 + "}\n"
            # )
            s += (
                r"\lplxPutLink{{{x}}}{{{y}}}{{{w}}}{{{h}}}{{{hrstart}}}{{{hrend}}}"
                .format(x=x, y=y, w=w, h=h, hrstart=s2, hrend='')
                + "%\n"
            )

        s += r"""\end{picture}""" + "%\n}" + """\endgroup""" + "\n"
        
        return s
