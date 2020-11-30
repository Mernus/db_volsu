function get_param(parameterName) {
    let result = null, tmp = [];

    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
            tmp = item.split("=");
            if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });

    return result;
}

active_table = document.getElementById("nav-" + get_param("table_name") + "-tab");
active_table.className = "active";