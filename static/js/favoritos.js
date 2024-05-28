$(document).ready(function() {
    // Configurar el token CSRF para todas las peticiones AJAX
    $.ajaxSetup({
      headers: {
        'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
      }
    });
  
    // Agregar a favoritos
    $(document).on('click', '.agregar-favorito', function() {
      var productoId = $(this).data('producto-id');
      $.ajax({
        url: '/agregar-a-favoritos/' + productoId + '/',
        method: 'POST',
        success: function(response) {
          if (response.status === 'added') {
            $('#favorito-' + productoId).html('<button class="btn btn-danger eliminar-favorito" data-producto-id="' + productoId + '">Eliminar de favoritos</button>');
          }
        }
      });
    });
  
    // Eliminar de favoritos
    $(document).on('click', '.eliminar-favorito', function() {
      var productoId = $(this).data('producto-id');
      $.ajax({
        url: '/eliminar-a-favoritos/' + productoId + '/',
        method: 'POST',
        success: function(response) {
          if (response.status === 'removed') {
            $('#favorito-' + productoId).html('<button class="btn btn-success agregar-favorito" data-producto-id="' + productoId + '">Agregar a favoritos</button>');
          }
        }
      });
    });
  });
