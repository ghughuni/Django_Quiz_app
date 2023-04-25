const form = document.getElementById("myForm");

form.addEventListener("submit", function (event) {
  event.preventDefault();
  const selectOption = document.getElementById("category_options").value;

  fetch("action", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({category: selectOption}),
  })
    .then((response) => response.text())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => console.error(error));
});
