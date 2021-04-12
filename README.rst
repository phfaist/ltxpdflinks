ltxpdflinks — include PDF graphics with links in LaTeX documents  
================================================================

To include fancy graphics (say a diagram) in your LaTeX document, a common
process is to design the diagram using your favorite graphics designer program,
to export the figure as a PDF graphic, and to use::

  \includegraphics[width=10cm]{my_figure}

And it works great.  Until you'd like to have figures with clickable links.  You
might even want to have links in your diagram to within the document—maybe a
clickable link to a document section, equation, or an item in your bibliography.

The ``ltxpdflinks`` tool provides a simple solution to include a PDF with its
links.  It includes ways to encode links to within the document, like you'd
obtain with ``\ref`` and ``\cite`` in LaTeX.


Quick Start
~~~~~~~~~~~

To get started:

  1. Install ``ltxpdflinks``::

       pip3 install ltxpdflinks

  2. Download the ``phflplx.sty`` file here::

     https://github.com/phfaist/ltxpdflinks/releases

[Self-note TODO: I still need to publish releases on github.com & on PyPI! For
now, you need to run ``poetry build``, ``pip3 install
dist/ltxpdflinks-0.1.0.tar.gz`` and ``(cd phflplx && latex phflplx.ins)``. ]

To compile your document:

  1. Drop the file ``phflplx.sty`` in the same folder as your latex source file,
     and add to your document preamble::

       \usepackage{phflplx}
       \DeclareGraphicsExtensions{.lplx,.pdf}

     [I'm assuming you're loading the ``graphicx`` (or alternatively
     ``graphics``) and the ``hyperref`` packages, too.]

     Note: If you'd like to include also other file types in your document
     (e.g., ``.png``, ``.jpeg``, etc.), you need to add them to the
     ``\DeclareGraphicsExtensions`` argument, too.  See doc for the
     `graphicx package <https://mirror.clientvps.com/CTAN/macros/latex/required/graphics/grfguide.pdf>`_.

  2. Run the |ltxpdflinks| command-line program for all your PDF files that
     contain links::

       > ltxpdflinks myfigure1.pdf

  3. Compile your LaTeX document as usual.


How to include links to other parts of the LaTeX document:

  1. When creating your figure in your favorite drawing software, create a "web
     hyperlink" with an URL of the following form::

       latexref://<type-of-reference>/<reference-target>
       
     For a link to a section, equation, etc. (when you'd use ``\ref`` /
     ``\autoref`` / ``\cref`` in LaTeX), use ``latexref://ref/<label-target>``
     where you replace ``<label-target>`` by the LaTeX label of the object
     you're referencing (the argument of the ``\label{...}`` command in LaTeX).

     For a link to a bibliographic reference entry (as in ``\cite{...}``), use
     ``latexref://cite/<bibtex-key>``, where you replace ``<bibtex-key>`` by the
     bibliographic reference key you'd like to refer to (the argument you'd use
     to the ``\cite{...}`` command).

  2. These special URL links are automatically converted to LaTeX references by
     the ``ltxpdflinks`` utility and the ``phflplx`` package.


Features
~~~~~~~~

  - Special link conversions::

      latexref://ref/XXXXXX   →   link to XXXXXX label as via \ref{XXXXXX}

      latexref://cite/XXXXXX   →   link to XXXXXX citation as via \cite{XXXXXX}

    (In the future I'll probably add ways to plug in custom link conversions.
    The code is extendible & you can add them yourself already if you invoke
    ``ltxpdflinks`` via your own python script.)

  - Full support for rotation, scaling and clipping via options to
    ``\includegraphics[...]{...}``

  - Links use the format defined in the LaTeX document (colors & border relevant
    for link type URL/internal reference/citation as specified via the
    ``hyperref`` package.)


Planned improvements
~~~~~~~~~~~~~~~~~~~~

  - Support the possibility (as an opt-in option) to preserve link styling
    (border, color, etc.)  instead if using the document links style

  - Support for internal annotations within the PDF graphic (from one part of
    the graphic to another)

  - Support for other types of annotations ?
