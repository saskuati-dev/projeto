function showSidebar(){
    const sidebar= document.querySelector('.sidebar')
    sidebar.style.display= 'flex'
}
function hideSidebar(){
    const sidebar= document.querySelector('.sidebar')
    sidebar.style.display= 'none'
}

document.addEventListener('DOMContentLoaded', function() {
   
    function showSidebar() {
        const sidebar = document.querySelector('.sidebar');
        sidebar.style.display = 'flex';
    }

    function hideSidebar() {
        const sidebar = document.querySelector('.sidebar');
        sidebar.style.display = 'none';
    }

    
    var headers = document.querySelectorAll('.gaveta-header');
    
    headers.forEach(function(header) {
        header.addEventListener('click', function() {
            var content = this.nextElementSibling;
            
            if (content.style.display === 'block') {
                content.style.display = 'none';
                this.classList.remove('active');
            } else {
                content.style.display = 'block';
                this.classList.add('active');
            }
        });
    });
    
   
    const showButton = document.querySelector('#show-sidebar');
    const hideButton = document.querySelector('#hide-sidebar');

    if (showButton) {
        showButton.addEventListener('click', showSidebar);
    }

    if (hideButton) {
        hideButton.addEventListener('click', hideSidebar);
    }
});


document.addEventListener('DOMContentLoaded', function() {
    // Selecionar o checkbox "marcar/desmarcar todas"
    const selectAllCheckbox = document.getElementById('select-all');
  
    // Adicionar evento para "marcar/desmarcar tudo"
    selectAllCheckbox.addEventListener('change', function() {
      const checkboxes = document.querySelectorAll('input[name="divisoes"]');
      checkboxes.forEach(function(checkbox) {
        checkbox.checked = selectAllCheckbox.checked;
      });
    });
  });
  
  