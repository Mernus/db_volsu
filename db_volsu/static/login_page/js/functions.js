defaults_btn = document.getElementById("defaults")

defaults_btn.onclick = function get_default_params() {

    document.getElementById("defaults").onclick = function () {
        let host_input = document.getElementsByName("host")[0];
        host_input.value = '{{ host }}';
        host_input.readOnly = true;
        let database_input = document.getElementsByName("database")[0];
        database_input.value = '{{ database }}';
        database_input.readOnly = true;
        let user_input = document.getElementsByName("user")[0];
        user_input.value = '{{ user }}';
        user_input.readOnly = true;
        let password_input = document.getElementsByName("password")[0];
        password_input.value = '{{ password }}';
        password_input.readOnly = true;
        let port_input = document.getElementsByName("port")[0];
        port_input.value = '{{ port }}';
        port_input.readOnly = true;
    }

}