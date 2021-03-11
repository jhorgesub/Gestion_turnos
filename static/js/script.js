window.onload = function() {


    $(document).ready(function() {
        $('#example').DataTable({
            "bPaginate": false,
            "bLengthChange": false,
            "bFilter": false,
            "bInfo": false,
            "bAutoWidth": false
        });




    });


    var form_fields = document.getElementsByTagName('input')

    if (window.location.pathname == '/register/') {

        form_fields[1].placeholder = 'DNI (Sin puntos)';
        form_fields[2].placeholder = 'Nombre/s';
        form_fields[3].placeholder = 'Apellido/s';
        form_fields[4].placeholder = 'Email';
        form_fields[5].placeholder = 'Ingrese una Contraseña';
        form_fields[6].placeholder = 'Ingrese nuevamente la Contraseña';


        for (var field in form_fields) {
            form_fields[field].className += ' form-control'

        }
    }




    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1;
    var yyyy = today.getFullYear();
    if (dd < 10) {
        dd = '0' + dd
    }
    if (mm < 10) {
        mm = '0' + mm
    }

    today = yyyy + '-' + mm + '-' + dd;
    try {
        document.getElementById("datefield").setAttribute("min", today);

    } catch (error) {

    }



    let botones = document.querySelectorAll('[data-target="#registroTurno"]');

    botones.forEach(btn => {
        btn.addEventListener('click', function() {

            let hora = this.dataset.id;
            let cancha = this.dataset.cancha;
            let fecha = this.dataset.fecha;

            // Asignar datos a ventana modal:
            document.querySelector('#hora').value = hora;
            document.querySelector('#fecha').value = fecha;
            document.querySelector('#cancha').value = cancha;

        });
    });




    let btncancelarTurno = document.querySelectorAll('[data-target="#cancelarTurno"]');

    btncancelarTurno.forEach(btn => {
        btn.addEventListener('click', function() {

            let turno = this.dataset.id;
            let fecha = this.dataset.fecha;
            let hora = this.dataset.hora;
            let cancha = this.dataset.cancha;






            // Asignar datos a ventana modal:

            let c = document.getElementById('text-cancelar');
            c.innerHTML = "¿Desea cancelar el turno con los siguientes datos? <hr> <br> Fecha : " + fecha +
                "<br> Hora : " + hora +
                "<br> Cancha : " + cancha
            document.getElementById('confirmarCancelar').href = '/turnos/cancelar/' + turno




        });
    });



    let btnbloquearUsuario = document.querySelectorAll('[data-target="#bloquearusuario"]');

    btnbloquearUsuario.forEach(btn => {
        btn.addEventListener('click', function() {

            let id = this.dataset.id;

            // Asignar datos a ventana modal:



            document.getElementById('confirmarBloqueo').href = '/usuario/bloquear/' + id




        });
    });





    let btndesbloquearUsuario = document.querySelectorAll('[data-target="#desbloquearusuario"]');

    btndesbloquearUsuario.forEach(btn => {
        btn.addEventListener('click', function() {

            let id = this.dataset.id;

            // Asignar datos a ventana modal:



            document.getElementById('confirmardesbloqueo').href = '/usuario/bloquear/' + id




        });
    });

















};