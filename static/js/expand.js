function toggle_display(){
  finder = document.querySelector('.hiding');

  if(finder.style.display == 'none')
  {
      finder.style.display = 'inline'
  }
  else
  {
     finder.style.display = 'none'
  }
}
