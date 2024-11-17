async function get_users(e) {
    e.preventDefault()
    const search = document.getElementById('search').value
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
        for (user of users) {
            console.log(user)
            var div = document.createElement('div')
            users_div.appendChild(div)
            div.insertAdjacentElement('beforebegin', '<img src="" alt="">')
            div.insertAdjacentElement('beforebegin', `<p>ИМЯ: ${user.first_name}</p>`)
            div.insertAdjacentElement('beforebegin', `<p>ФАМИЛИЯ: ${user.last_name}</p>`)

        }
    })

}

document.getElementById('search_btn').addEventListener('click', get_users)