document.addEventListener('click', function(e){
  var close = e.target.closest('[data-close]');
  if (close){
    var target = close.closest('.flash');
    if (target) target.remove();
  }
});