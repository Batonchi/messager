const current_user_id = document.getElementById('current_user_id').value
const ws = new WebSocket(`/users/friend/add/${current_user_id}`)
ws.onmessage = async function(event) {
    if (event.data == current_user_id) {
        await fetch(`/users/notification/list-other-requests`).then(response => {
            return response.json()
        }).then((users) => {
            show_info_cells('in-your', users)
        })
    }
}

function show_info_cells (place_id, list_of_placed_info) {
    const users_div = document.getElementById(place_id)
            users_div.innerHTML = ''
            console.log(list_of_placed_info)
            for (const user of list_of_placed_info) {
                const button = '<button className="" onClick="addFriend(${user.user_id})">Принять</button>'
                users_div.insertAdjacentHTML('beforeend', `
                    <div class="scroll-elem" onclick="showProfile(${user.user_id})">
                        <div class="image-box" style="background-image: url('/static/avatars/${user.photo_of_profile}.png');
                         width: 100px; height: 100px" onclick=""></div>
                        <div class="content">
                            <span>ФАМИЛИЯ: ${user.last_name}</span>
                            <span>ИМЯ: ${user.first_name}</span>
                        </div>
                        ${String(place_id) === 'in-your' ? button : ''}
                    </div>`)
            }
}

async function addFriend(friend_id){
    await fetch(`/users/friend/accept?friend_id=${friend_id}`, {'method': 'POST'})
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
            show_info_cells('users', users)
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
        show_info_cells('friends', users)
    })

    await fetch(`/users/notification/list-your-requests`).then(response => {
        return response.json()
    }).then((users) => {
        show_info_cells('from-your', users)
    })

    await fetch(`/users/notification/list-other-requests`).then(response => {
            return response.json()
        }).then((users) => {
            show_info_cells('in-your', users)
        })
})

async function addFriends(userId) {
    await fetch(`/users/friend/add?friend_id=${userId}`, {method: 'post'})
}

async function openProfile(userId) {
    window.location.href = `/users/profile/${userId}`, {method: 'get'}
}


