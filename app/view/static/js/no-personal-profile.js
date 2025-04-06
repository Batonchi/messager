const current_user_id = document.getElementById('current_user_id').value
const parts = window.location.href.split('/')
const friend_id = parts[parts.length - 1]

const ws = new WebSocket(`/users/friend/add/${current_user_id}?friend_id=${friend_id}`)


async function get_user() {
    await fetch(`/users/user?user_id=${friend_id}`).then(response => {
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
            console.log(status)
            const button = document.getElementById('add_friend')
            switch (status) {
                case FRIEND.YES:
                    button.textContent = FRIEND.YES
                    break
                case FRIEND.FROM:
                    button.textContent = FRIEND.FROM
                    break
                case FRIEND.FOR:
                    button.textContent = FRIEND.FOR
                    button.addEventListener('click', async (event) => {
                        event.preventDefault()
                        await fetch(`/users/friend/accept?friend_id=${friend_id}`, {'method': 'POST'})
                        location.reload()
                    })
                    break
                case FRIEND.NOT:
                    button.textContent = FRIEND.NOT
                    button.addEventListener('click', async (event) => {
                        event.preventDefault()
                        ws.send(FRIEND.FROM)
                        location.reload()
                    })
                    break
            }
            button.style.display = 'block'
        })
    })
}


document.addEventListener('DOMContentLoaded',  async () => {
    await get_user()
})


class FRIEND {
    static NOT = 'Добавить в друзья'
    static FROM = 'Заявка отправлена'
    static FOR = 'Принять заявку'
    static YES = 'В друзьях'
}

