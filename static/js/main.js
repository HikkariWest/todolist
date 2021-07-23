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