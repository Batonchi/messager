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