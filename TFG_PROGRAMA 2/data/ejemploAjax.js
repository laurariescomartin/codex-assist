$(document).ready(function() {
  boton.onclick = hacerPeticionAjax;    
});

function hacerPeticionAjax() {
    num = $("#numElems").val();
    
    $.ajax({
       data: {num},
       url: 'ajax.php',
       type: 'get',
       beforeSend: function () {
         $("#mensaje").show();
       },
       success: function(respuesta) {
         procesaRespuestaAjax(respuesta);
         $("#mensaje").hide();
       }
    });
}

function procesaRespuestaAjax(respuesta) {
    res = "";
    
    for (i = 0 ; i < respuesta.length ; i++) {
        res += "<tr><td>" + respuesta[i].obj + "</td><td>" + respuesta[i].cant + "</td></tr>\n";
    }
    
    $("#tabla > tbody").html(res);
}
