document.getElementById('registration').addEventListener('submit', async (event) => {
    event.preventDefault()
    const reg_form = document.getElementById('registration')
    response = await fetch(`/login?email=${reg_form.email.value}&password=${reg_form.password.value}`, {
        method: "POST"
    })
    if (response.status == 404) {
        alert("")
        return
    } else if (response.status != 200) {
        alert("Ой! Что то пошло не так :(")
        return
    }
    window.location.href="/users/profile"
})