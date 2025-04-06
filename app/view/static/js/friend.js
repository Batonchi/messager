const current_user_id = document.getElementById('current_user_id').value
const ws = new WebSocket(`/users/friend/add/${current_user_id}`)
ws.onmessage = async function(event) {
    if (event.data == current_user_id) {
        await fetch(`/users/notification/list-other-requests`).then(response => {
            return response.json()
        }).then((users) => {
            const users_div = document.getElementById('in-your')
            users_div.innerHTML = ''
            console.log(users)
            for (const user of users) {
                users_div.insertAdjacentHTML('beforeend', `
                    <div class="scroll-elem" onclick="showProfile(${user.user_id})">
                        <div class="image-box" style="background-image: url('/static/avatars/${user.photo_of_profile}.png'); width: 100px; height: 100px" onclick=""></div>
                        <div class="content">
                            <span>ФАМИЛИЯ: ${user.last_name}</span>
                            <span>ИМЯ: ${user.first_name}</span>
                        </div>
                        <button class="" onclick="addFriend(${user.user_id})">Принять</button>
                    </div>`)
            }
        })
    }
}

async function addFriend(friend_id){
    await fetch(`/users/friend/accept?friend_id=${friend_id}`)
    location.reload()
} 


async function get_users(e) {
    e.preventDefault()
    const search = document.getElementById('input_str').value
    if (search === '') {
        return
    }
    await fetch(`/users/search?search_str=${search}`).then(response => {
            return response.json()
        }).then((users) => {
        const users_div = document.getElementById('users')
        users_div.innerHTML = ''
        console.log(users)
        for (const user of users) {
            users_div.insertAdjacentHTML('beforeend', `
                <div class="scroll-elem" onclick="showProfile(${user.user_id})">
                    <div class="image-box" style="background-image: url('/static/avatars/${user.photo_of_profile}.png'); width: 100px; height: 100px" onclick=""></div>
                    <div class="content">
                        <span>ФАМИЛИЯ: ${user.last_name}</span>
                        <span>ИМЯ: ${user.first_name}</span>
                    </div>
                </div>`)
        }
    })
}

function showProfile(user_id) {
    window.location.href = `/users/profile/${user_id}`
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
                                    <div class="image-box" style="background-image: url('/static/avatars/${user.photo_of_profile}.png');"></div>
                                    <div class="content">
                                        <span>ФАМИЛИЯ: ${user.last_name}</span>
                                        <span>ИМЯ: ${user.first_name}</span>
                                    </div>
                                </div>`)
        }
    })

    await fetch(`/users/notification/list-your-requests`).then(response => {
        return response.json()
    }).then((users) => {
        const users_div = document.getElementById('from-your')
        users_div.innerHTML = ''
        console.log(users)
        for (const user of users) {
            users_div.insertAdjacentHTML('beforeend', `
                <div class="scroll-elem" onclick="showProfile(${user.user_id})">
                    <div class="image-box" style="background-image: url('/static/avatars/${user.photo_of_profile}.png'); width: 100px; height: 100px" onclick=""></div>
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


