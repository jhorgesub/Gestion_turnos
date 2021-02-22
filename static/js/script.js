window.onload = function() {
    var form_fields = document.getElementsByTagName('input')

    if (window.location.pathname == '/register/') {

        console.log(form_fields)
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
    document.getElementById("datefield").setAttribute("min", today);



};