async function get_user() {
    await fetch('/users/user').then(response => {
            return response.json()
        }
    ).then((user) => {
        user_form = document.getElementById('user_form')
        user_form.email.value = user.email
        user_form.first_name.value = user.first_name
        user_form.last_name.value = user.last_name
        user_form.birth_date.value = user.birth_date
    })
}

document.addEventListener('DOMContentLoaded',  async () => {
    await get_user()
})

document.getElementById('button_form').addEventListener('click', async (event) => {
    event.preventDefault()

    const reg_form = document.getElementById('registration')

    if (reg_form.password.value !== reg_form.repeat_password.value) {
        alert("Пвроли не совпадают!")
        return
    }
    const formData = new FormData()
    formData.append('first_name', reg_form.first_name.value)
    formData.append('last_name', reg_form.last_name.value)
    formData.append('email', reg_form.email.value)
    formData.append('birth_date', reg_form.birth_date.value)
    formData.append('password', reg_form.password.value)
    response = await fetch('/registration', {
        method: "POST",
        body: formData}).then((response) => {
            window.location.href = ''
    }, (response) => {
            if (response.status != 200) {
                alert("Ой! Что то пошло не так :(")
                return
            }
    })
    // window.location.href="/login"
})