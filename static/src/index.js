import {
    io
} from 'socket.io-client'
const socket = io('https://flask-chatapp1.herokuapp.com/')
socket.on('receive-message', (data) => {
    sender(data['msg'], data['user'])
})

// socket.on('connect',() => {
//     socket.emit('send_message',{'message':'hello','name':'Abdelrahman'})
//     console.log('connected')
// }); 
// socket.on('receive-message',(data) => {      
//     sender(data['msg'],data['user'])
//     })
window.sender = function sender(txt, name) {
    let box = document.querySelector('.box-content');
    let message_box = document.createElement('div');
    message_box.classList.add('message');
    message_box.classList.add('left');
    let text = document.createElement('div');
    text.classList.add('text')
    let username = document.createElement('h3');
    username.textContent = name;
    let img = document.createElement('img');
    img.setAttribute('src', '../static/images/comment.svg');
    let m = document.createElement('p');
    m.textContent = txt;
    box.appendChild(message_box);
    message_box.appendChild(img);
    message_box.appendChild(text);
    text.appendChild(username);
    text.appendChild(username);
    text.appendChild(m);
    start_bottom();
}
window.get_message = function get_message() {
    fetch('/message')
        .then(res => {
            return res.json()
        })
        .then(messages => {
            if (messages === []) {
                return
            }
            for (let i = 0; i < messages.length; i++) {
                let name = messages[i]['username']
                sender(messages[i]['message'], name)
            }
            start_bottom();
        })
}

function start_bottom() {
    let box = document.querySelector('.box-content');
    box.scrollTop = box.scrollHeight;
}
if (document.URL.includes("/chat_room")) {
    get_message();
}

window.send_message = function send_message() {
    let message = new FormData(document.querySelector('.message-form'))
    let name = null
    let m = null
    fetch('/message', {
            method: 'post',
            body: message
        })
        .then(res => {
            return res.json()
        })
        .then(txt => {
            if ('username' in txt) {
                name = txt['username'];
                m = txt['message']
                const temp_socket = io('https://flask-chatapp1.herokuapp.com/')
                temp_socket.on('connect', () => {
                    temp_socket.emit('send_message', {
                        'message': m,
                        'name': name
                    })
                    console.log('connected')
                });
                let input = document.querySelector('.enter');
                input.value = ''
            }
        });
    return false
}

window.login_to_chat = function login_to_chat() {
    let data = document.querySelector('.login-form')
    let form = new FormData(data);
    fetch('/log', {
            method: 'post',
            body: form
        })
        .then(res => {
            return res.json()
        })
        .then(txt => {
            if ('msg' in txt) {
                let h3 = document.createElement('h3');
                h3.classList.add('msg')
                h3.textContent = txt['msg'];
                if (!data.contains(h3)) {
                    data.appendChild(h3)
                } else {
                    let del = document.querySelector('.msg');
                    del.remove()
                    data.appendChild(h3)
                }
            } else {
                user = txt['user'];
                window.location.href = '/chat_room';
            }
        })
    return false
}

window.register = function register() {
    let data = document.querySelector('.login-form')
    let form = new FormData(data)
    fetch('/register_api', {
            method: 'post',
            body: form
        })
        .then(res => {
            return res.json()
        })
        .then(txt => {
            if ('msg' in txt) {
                let h3 = document.createElement('h3');
                h3.classList.add('msg')
                h3.textContent = txt['msg'];
                if (data.contains(h3)) {
                    let del = document.querySelector('.msg');
                    del.remove()
                    data.appendChild(h3)
                } else {
                    data.appendChild(h3)
                }

            } else {
                window.location.href = '/chat_room'
            }
        })
    return false
}