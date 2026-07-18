// Tab switching for the game hub. Each tab button's data-tab attribute
// matches the id of the panel it should reveal.
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".tab-button");
  const panels = document.querySelectorAll(".tab-panel");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const target = button.dataset.tab;

      buttons.forEach((b) => {
        b.classList.toggle("active", b === button);
        b.setAttribute("aria-selected", b === button ? "true" : "false");
      });

      panels.forEach((panel) => {
        panel.classList.toggle("active", panel.id === target);
      });
    });
  });
});
