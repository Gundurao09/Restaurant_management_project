function openNewWindow(selectedValue) {
    var url;
    if (selectedValue === "{{ url_for('login')}}") {
        url = "{{ url_for('login')}}";
    } else if (selectedValue === "{{ url_for('user_login') }}") {
        url = "{{ url_for('user_login') }}";
    }

    if (url) {
        window.open(url, "_blank");
    }
}