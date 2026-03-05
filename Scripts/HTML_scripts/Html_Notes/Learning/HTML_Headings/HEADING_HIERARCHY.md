# 🏗️ HTML Heading Hierarchy

Headings are more than just different font sizes; they create the structural outline of your document. Search engines and screen readers use these tags to understand the relationship between different sections of content.

## 📏 Heading Levels

HTML provides six levels of headings, ranging from most important to least important:

1. **`<h1>`**: The primary title of the page. You should generally only have one `<h1>` per page.
2. **`<h2>` and `<h3>`**: Used for major sections and sub-sections.
3. **`<h4>` through `<h6>`**: Used for deep nesting and fine-grained details.

## 🔍 Technical Considerations

* **SEO Impact**: Search engines like Google prioritize text inside `<h1>` and `<h2>` tags to determine what your page is about.
* **Accessibility**: Users with visual impairments use screen readers to "jump" from heading to heading to navigate your site quickly.
* **Skipping Levels**: It is a best practice never to skip a heading level (e.g., don't jump from `<h1>` to `<h3>`) as it breaks the logical flow for accessibility tools.

---

**Original Creation:** 12-20-2014  
**Last Audit:** 12-31-2025  
**Developer:** omegazyph
