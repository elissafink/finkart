# FinkArt static site

Plain HTML, CSS and one small JavaScript file. No build step, no database.

## Put it online
Upload the whole folder (everything inside `finkart-site`) to your host, keeping the
structure as-is. Every page is `<folder>/index.html`, so the addresses match the
original site (for example `/bio/`, `/time-and-matter-photography/hair/`).
You can also double-click `index.html` to browse it on your own computer.

## Images (do this once, before you retire the old WordPress site)
Right now the pages load images from finkart.com, so they work immediately but
depend on the old site staying up. To copy them into this folder:

    python3 localize-images.py

It downloads about 390 images into `images/` and rewrites every page to use them.
Re-run it if any download fails; it skips what it already has.

## Contact form
A static site can't send email by itself. The form opens the visitor's email app
with the message filled in. For a real form, sign up with a form service
(Formspree, Netlify Forms, etc.) and point the form at it.

## Editing
- Site-wide look: `assets/style.css`
- Menu and footer are repeated in each page's HTML; edit them in each file
  (or ask Claude to regenerate the site).
