// Invoke Functions Call on Document Loaded
document.addEventListener("DOMContentLoaded", function () {
  hljs.highlightAll();
});

// had to look online on how to close messages if there was more than two popup errors
// this is what you should use instead of the default
let alertWrapper = document.querySelectorAll(".alert");
let alertClose = document.querySelectorAll(".alert__close");

if (alertWrapper) {
  for (let i = 0; i < alertClose.length; i++) {
    alertClose[i].addEventListener("click", () => {
      alertWrapper[i].style.display = "none";
    });
  }
}
