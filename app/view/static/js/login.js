document.getElementById('login').addEventListener('submit', async (event) => {
    event.preventDefault()
    const log_form = document.getElementById('login')
    response = await fetch(`/login?email=${log_form.email.value}&password=${log_form.password.value}`, {
        method: "POST"
    })
    if (response.status == 200){
        window.location.href="/chat"
        return
    }
    if (response.status == 409) {
        alert("Не верный пароль")
        return
    } else {
        alert("Ой! Что то пошло не так :(")
        return
    }

})