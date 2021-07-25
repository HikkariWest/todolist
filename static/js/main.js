let bool = true;

click.addEventListener("click", function() {
  block.innerHTML = bool;
  bool = !bool;
})

$(document).ready(function() {
   let form = $('form');
   form.submit(function(e) {
       e.preventDefault();
       e.stopPropagation();
       
       let data = $(this).serialize(); // Данные формы

       $.ajax({
           method: 'post',
           data: data,
           url: $(this).attr('action'),
           success: function () {...}
       });
   })
});

function openCity(evt, categoryName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(categoryName).style.display = "block";
    evt.currentTarget.className += " active";
}