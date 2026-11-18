# Complex Function Explorer

A browser-based Newton's method visualiser. It uses Pyodide to run Python in the browser and Plotly.js to display interactive graphs.

## Files

- `index.html` – webpage and browser interface.
- `newtons_method_imag_function.py` – Python implementation of Newton's method and complex-plane calculations.

## Run locally

The page loads Python and plotting libraries from public CDNs, so it should be opened through a local web server rather than by double-clicking the HTML file.

From this folder, run:

```bash
python -m http.server 8000
```

Then open:

`http://localhost:8000`

## Publish on GitHub Pages

1. Upload both files to the same folder in your GitHub repository.
2. Enable GitHub Pages for the repository (Settings → Pages → Deploy from a branch).
3. Open the published `index.html` page.

## Function syntax

Use `z` as the complex variable and Python-style exponentiation (`**`).

Examples:

- `z**2 + 1`
- `z**3 + 4`
- `z**4 - 1`
- `z**5 + z + 1`
- `np.exp(z) - 1`

Supported mathematical functions include `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `sinh`, `cosh`, and `tanh`, including their `np.` forms.

## Notes

- The resolution is `n` points along each axis, so the total number of starting points is `n²`.
- High resolutions and large iteration limits take longer to calculate in a browser.
- The real-axis graph displays the real part if the expression returns complex values for real inputs.
- This browser version uses a restricted expression evaluator; it does not execute arbitrary Python code.
