# Black Seam

A Victorian point-and-click adventure: a voiced prologue (London, September 1869) and Act 1 (Cwm Du, Glamorgan).

**Play:** the site is `docs/index.html`, served by GitHub Pages from the `docs/` folder on `main`.

## Building

Edit the chapters in `mockups/prologue.html` and `mockups/act1.html`, then run:

```
python3 build_site.py
```

This rebuilds `docs/index.html` with both chapters and the recorded voices (`voices/samples/office`) built in. Commit and push `docs/` to update the site.
