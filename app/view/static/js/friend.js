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
        for (const user of users) {
            const div = document.createElement('div')
            div.className = 'scroll-elem'
            div.innerHTML = `
                <img src="/static/avatars/${user.photo_of_profile}.png" alt="">
                <div>
                     <span>ФАМИЛИЯ: ${user.last_name}</span>
                    <span>ИМЯ: ${user.first_name}</span>
                    </div>
                    <button onclick="addFriends(${user.user_id})" style="width: 300px; height: 100px; z-index: 1;">Добавить в друзья</button>
            `
            users_div.appendChild(div)
        }
    })
}


document.getElementById('search-form').addEventListener('submit', get_users)

document.addEventListener('DOMContentLoaded',  async () => {
    await fetch('usr/friend/list').then(response => {
        return response.json()
    }).then((users) => {
        const friends = document.getElementById('friends')
        for (const user of users) {
            friends.insertAdjacentHTML('beforeend', `<div class="scroll-container" id="users">
                                <div class="scroll-elem">
                                    <div class="image-box"><img src="/static/avatars/${user.photo_of_profile}.png" alt=""></div>
                                    <div class="content">
                                        <span>ФАМИЛИЯ: ${user.last_name}</span>
                                        <span>ИМЯ: ${user.first_name}</span>
                                    </div>
                                </div>
                           </div>`)
        }
    })
})

async function addFriends(userId) {
    await fetch(`/users/friend/add?friend_id=${userId}`, {method: 'post'})
}