const current_user_id = document.getElementById('current_user_id').value
const parts = window.location.href.split('/')
const friend_id = parts[parts.length - 1]

const ws = new WebSocket(`/users/friend/add/${current_user_id}?friend_id=${friend_id}`)


async function get_user() {
    await fetch('/users/user').then(response => {
            return response.json()
        }
    ).then(async (user) => {
        user_form = document.getElementById('user_form')
        user_form.first_name.value = user.first_name
        user_form.last_name.value = user.last_name
        user_form.birth_date.value = user.birth_date
        document.getElementById('photo-of-profile').src = `/static/avatars/${user.photo_of_profile}.png`
        await fetch(`/users/check_friend?friend_id=${friend_id}`).then(response => {
            return response.json()
        }).then((status) => {
            let button = document.getElementById('add_friend')
            switch (status) {
                case true:
                    button.textContent = 'В ДРУЗЬЯХ'
                    break
                case false:
                    button.textContent = 'Заявка отправлена'
                    break
                case null:
                    button.textContent = 'Добавить в друзья'
                    button.addEventListener('click', async (event) => {
                        event.preventDefault()
                        ws.send('************')
                        location.reload()
                    })
                    break
            }
        })
    })
}

document.addEventListener('DOMContentLoaded',  async () => {
    await get_user()
})

