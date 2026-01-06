# 🐬 Dolphin Tabs Menu

A lightweight, CSS-driven tabbed navigation system that uses JavaScript to swap content panels dynamically. Originally created in 2007, this project demonstrates the "Sliding Doors" technique for flexible web components.

## 📂 Project Structure

The project consists of three core files that must remain in the same directory:

* **`index.htm`**: The skeletal structure containing the navigation list and the content containers.
* **`style.css`**: The visual layer handling the "Sliding Doors" backgrounds and hover effects.
* **`dolphin.js`**: The engine that manages state and visibility of the sub-content.

---

## 🚀 How It Works

### 1. The Link (Trigger)

Each tab is a standard list item with a link. The connection to the content is made using the `rel` attribute:

```html
<li><a href="#" rel="target_id"><span>Tab Name</span></a></li>
