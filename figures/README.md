# Figures

Shared figures for the thesis, one folder per figure. The folder name is the figure ID, used everywhere (`.tex`, KB notes, analyses).

```
figures/<fig-id>/
  make.py | make.tex   # generates fig.pdf from analyses in projects/
  ORIGIN.md            # instead of make.*, when a figure is reused unchanged from a manuscript
  fig.pdf
```

Compose figures programmatically (LaTeX/Python) from existing code and analyses. Reuse the original figure unless it has been updated, to avoid duplication.
