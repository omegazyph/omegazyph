# 🖼️ HTML Image Embedding

This script demonstrates how to render a local image file within a webpage. Unlike text, images are "replaced elements," meaning the browser fetches the file and swaps the tag for the actual graphic.

## 🏗️ Attribute Definitions

To display an image correctly, the following attributes are used:

1. **`src` (Source)**: The file path. Using `imgs/` indicates the image is stored in a subfolder relative to this HTML file.
2. **`alt` (Alternative Text)**: Used by screen readers for accessibility and displayed if the image link is broken.
3. **`width` & `height`**: Explicitly defines the space the image occupies in pixels ($px$).

## 🔍 Path Management

When working with images in subfolders, ensure your folder structure looks like this:

* **root_folder/**
* `HTML_Link.html`
* **imgs/**
* `2022-11-30 Woman 6.jpg`

---

**Original Creation:** 12-20-2014  
**Last Audit:** 12-31-2025  
**Developer:** omegazyph
