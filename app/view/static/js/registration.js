document.getElementById('button_form').addEventListener('click', async (event) => {
    event.preventDefault()

    const reg_form = document.getElementById('registration')
    
    if (reg_form.password.value !== reg_form.repeat_password.value) {
        alert("Пвроли не совпадают!")
        return
    }
    const user = {
        first_name: reg_form.first_name.value,
        last_name: reg_form.last_name.value,
        email: reg_form.email.value,
        birth_date: reg_form.birth_date.value,
        password: reg_form.password.value,
    }
    const avatar = reg_form.photo_of_profile.files[0]
    if (avatar) {
        user['photo_of_profile'] = avatar
    }
    console.log(user)
    response = await fetch('/registration', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    })
    if (response.status == 409) {
        alert("Такой пользователь уже зарегистрирован!")
        return
    } else if (response.status != 200) {
        alert("Ой! Что то пошло не так :(")
        return
    }
    window.location.href="/login"
})

