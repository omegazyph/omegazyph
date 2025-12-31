# 🧮 Spin Menu Trigonometry

The menu works by mapping each item to a point on a circle using the mathematical constant $PI$ ($\pi$).

## 📐 How the Movement Works

The script calculates the position of each item using the following logic:

1. **Angle Calculation**: It divides a full circle ($2 \times \pi$) by the number of menu items to get the `pas` (step).
2. **$X$ and $Y$ Coordinates**:
   * **Horizontal**: Uses $Radius \times \cos(Angle)$ for the $X$ position.
   * **Vertical**: Uses $Radius \times \sin(Angle)$ for the $Y$ position.
3. **The 3D Illusion**: The script divides the coordinates by the `eye.s` (scale) variable. This flattens the circle into an oval, creating the appearance of depth.

## 🛠️ Internal Function Roles

* **`eye.muta()`**: This is the heart of the script. It is a recursive function that uses `setTimeout` to move the buttons smoothly whenever the user clicks the navigation arrows.
* **`getposOffset()`**: This ensures that even if you move your browser window or have the menu inside a complex layout, the buttons always know where the center of the menu is located.

---

**Original Creation:** 04-17-2003  
**Updated:** 12-31-2025  
**Developer:** omegazyph
