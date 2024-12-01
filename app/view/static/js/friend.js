async function get_users(e) {
    e.preventDefault()
    const search = document.getElementById('input_str').value
    if (search === ''){
        return
    }
    await fetch(`/users/search?search_str=${search}`).then(response => {
            return response.json()
        }
    ).then((users) => {
        var users_div = document.getElementById('users')
        users.innerHTML = ''
        console.log(users)
        for (const user of users) {
            var div = document.createElement('div')
            div.innerHTML = `
                <div>
                    <img src="/static/avatars/${user.photo_of_profile}.png" alt="">
                    <div>
                        <span>ФАМИЛИЯ: ${user.last_name}</span>
                        <span>ИМЯ: ${user.first_name}</span>
                    </div>
                    <button onclick="addFriends(${user.user_id})">Добавить в друзья</button>
                </div>
            `
            users_div.appendChild(div)
            
        }
    })

}

document.getElementById('search-form').addEventListener('submit', get_users)



async function addFriends(userId) {
    
} 