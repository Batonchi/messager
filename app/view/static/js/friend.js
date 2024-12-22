async function get_users(e) {
    e.preventDefault()
    const search = document.getElementById('input_str').value
    if (search === '') {
        return
    }
    await fetch(`/users/search?search_str=${search}`).then(response => {
            return response.json()
        }
    ).then((users) => {
        const users_div = document.getElementById('users')
        users_div.innerHTML = ''
        console.log(users)
        for (const user of users) {
            users_div.insertAdjacentHTML('beforeend', `
                <div class="scroll-elem">
                    <div class="image-box" style="background-image: url(/static/avatars/${user.photo_of_profile}.png);" onclick=""></div>
                    <div class="content">
                        <span>ФАМИЛИЯ: ${user.last_name}</span>
                        <span>ИМЯ: ${user.first_name}</span>
                    </div>
                    <button onclick="alert('tam')" style="background: none; background-color: rgb(71, 71, 71); width: 200px; height: 100px; outline: none; font-family: inherit; font-size: 28px; color: white; cursor: pointer;">Добавить</button>
                </div>`)
        }
    })
}


document.getElementById('search-form').addEventListener('submit', get_users)

document.addEventListener('DOMContentLoaded',  async () => {
    await fetch('/users/friend/list').then(response => {
        return response.json()
    }).then((users) => {
        const friends = document.getElementById('friends')
        for (const user of users) {
            friends.insertAdjacentHTML('beforeend', `
                                <div class="scroll-elem" onclick="openProfile(${user.user_id})">
                                    <div class="image-box" style="background-image: url(/static/avatars/${user.photo_of_profile}.png);"></div>
                                    <div class="content">
                                        <span>ФАМИЛИЯ: ${user.last_name}</span>
                                        <span>ИМЯ: ${user.first_name}</span>
                                    </div>
                                </div>`)
        }
    })
})

async function addFriends(userId) {
    await fetch(`/users/friend/add?friend_id=${userId}`, {method: 'post'})
}

async function openProfile(userId) {
    window.location.href = `/users/profile/${userId}`, {method: 'get'}
}