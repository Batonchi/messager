async function get_user() {
    await fetch('/users/user').then(response => {
            return response.json()
        }
    ).then((user) => {
        user_form = document.getElementById('user_form')
        user_form.about.value = user.about
        user_form.email.value = user.email
        user_form.first_name.value = user.first_name
        user_form.last_name.value = user.last_name
        user_form.birth_date.value = user.birth_date
        document.getElementById('photo-of-profile').src = `/static/avatars/${user.photo_of_profile}.png`
    })
}

document.addEventListener('DOMContentLoaded',  async () => {
    await get_user()
})

async function update_avatar(event) {
    const file = event.target.files[0]
    const formData = new FormData()
    formData.append("photo_of_profile", file)
    response = await fetch('/users/update-avatar', {method: 'POST', body: formData})
    if (response.ok) {
        location.reload()
    }
}

async function update_profile() {
    let user_form = document.getElementById('user_form')
    await fetch(`/users/update-data?first_name=${user_form.first_name.value}&last_name=${user_form.last_name.value}&email=${user_form.email.value}&birth_date=${user_form.birth_date.value}&about=${user_form.about.value}`, {
        method: "POST",
    }).then((response) => {
        if (!response.ok) {
            alert('Are you ***!!!!!')
            return
        }
        location.reload()
    })
}

document.getElementById('button_form').addEventListener('click', async e=> {
    e.preventDefault()
    await update_profile()
})