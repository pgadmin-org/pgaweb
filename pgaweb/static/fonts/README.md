# Fonts

IBM Plex Sans and IBM Plex Mono, self-hosted rather than loaded from a third
party, so that no page load depends on an outside host and nothing about our
visitors is disclosed to one.

Only the `latin` and `latin-ext` subsets are here. The Google Fonts API also
offers cyrillic, cyrillic-ext, greek and vietnamese, which would roughly
quadruple the file count for glyphs no page currently uses. Each `@font-face`
rule carries its `unicode-range`, so a browser downloads only the subsets and
weights a page actually needs.

Sans upright is a **variable** font covering 400 to 700 in one file per subset,
so it is declared once with a weight range rather than once per weight. Google's
stylesheet lists it four times, once per weight, every one pointing at the same
file; following that literally would have a browser fetch the same 45KB under
four different URLs and cache it four times over. Sans italic and Mono are not
variable and keep one file per weight.

Weights: Sans 400-700 variable plus 400 italic; Mono 400, 500, 600.

## Licence

IBM Plex is licensed under the SIL Open Font License 1.1:
https://github.com/IBM/plex/blob/master/LICENSE.txt

## Regenerating

`pgaweb/static/css/_fonts.scss` is generated alongside these files. To change the
weights or subsets, refetch the stylesheet with a browser user agent so that
Google serves woff2 rather than an older format, then re-extract:

```
https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap
```

The `src` URLs in `_fonts.scss` are absolute (`/static/fonts/...`) rather than
relative, because the compiled stylesheet is served from
`/static/COMPILED/assets/css/`, and a relative URL would resolve against that
instead.
