let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

$.ajaxSetup({
    headers: {
        'X-CSRFToken': csrftoken
    }
});

let words_obj = 0;
$.ajax({
    url: '/english/api/r_e_words',
    method: 'GET',
    async: false,
    success: function (text) {

        words_obj = text;
    },
    error: function (text) {
        alert('"Не получен "');
    },
});
/*
Array(20) [ {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, … ]
0: Object { id: 16, english: "bride", russian: "невеста", … }

control: false
english: "bride"
heavy: false
id: 16
info: ""
irregular_verbs: false
learned: false
lesson: 1
phrasal_verbs: false
repeat_in_progress: true
repeat_learn: 3
russian: "невеста"

1: Object { id: 52, english: "paint", russian: "краска", … }
2: Object { id: 68, english: "stomachache", russian: "боль в животе", … }
3: Object { id: 83, english: "to bake", russian: "печь", … }
4: Object { id: 89, english: "camera", russian: "фотаппарат", … }
*/

let random_word = words_obj[Math.floor(Math.random() * words_obj.length)];

var dellete_word_button = document.getElementById('dellete_word'); // кнопка для удаления слова

var count_words = document.getElementById("count_is");    // счетчик слов
var submit_button = document.getElementById("submit_button");    // счетчик слов
var vvod = document.getElementById("vvod");    // счетчик слов
var learned = document.getElementById('learned'); // кнопка для выученого слова
var heavy = document.getElementById('heavy'); // кнопка для сложного слова
var important = document.getElementById('important'); // кнопка для important слова
count_words.innerHTML = words_obj.length;
var word_index_to_dell = false;
let answer = document.getElementById("result");             // правильный ответ
document.getElementById("word").innerHTML = random_word.russian;
let ok = document.getElementById("ok");
let err = document.getElementById("error");

let logo = document.getElementById("logo")
let control_state=true;
if (logo.style.backgroundColor){
    control_state = true
}
else{
    control_state = false
}

function start() {
    let inp = document.getElementById("vvod").value.trim();
    let to_del = random_word;
    random_word = words_obj[Math.floor(Math.random() * words_obj.length)];
    if (random_word == undefined) {
        alert("Слова закончились, отдохни!!!");
    }
    if (random_word.id==to_del.id){
        random_word = words_obj[Math.floor(Math.random() * words_obj.length)];
    }
    if (random_word.id==to_del.id){
        random_word = words_obj[Math.floor(Math.random() * words_obj.length)];
    }
    document.getElementById("word").innerHTML = random_word.russian;
    count_words.innerHTML = words_obj.length;
    heavy.classList.remove('btn-dark', 'btn-outline-dark')
    if (to_del.heavy){
        heavy.classList.add('btn-dark');
    }else{
        heavy.classList.add('btn-outline-dark');
    }
    learned.classList.remove('btn-success', 'btn-outline-success')
    if (to_del.learned){
        learned.classList.add('btn-success');
    }else{
        learned.classList.add('btn-outline-success');
    }
    important.classList.remove('btn-warning', 'btn-outline-warning')
    if (to_del.important){
        important.classList.add('btn-warning');
    }else{
        important.classList.add('btn-outline-warning');
    }
    let data = {}

    if (inp.toLowerCase() === to_del.english.toLowerCase()) { //right input

        answer.innerText = to_del.english + " - " + to_del.russian + "//" + to_del.repeat_learn + "//";
        if (control_state) {
            data.learned = true;
            data.control = true;
            to_del.learned = true;

            learned.classList.remove('btn-success', 'btn-outline-success')
            if (to_del.learned) {
                learned.classList.add('btn-success');
            } else {
                learned.classList.add('btn-outline-success');
            }
        }

        let word_index = words_obj.indexOf(to_del);
        if (word_index !== -1) {
            words_obj.splice(word_index, 1);
        }

        if (to_del.repeat_learn > 0) {
            data.repeat_learn = to_del.repeat_learn - 1
        } else {
            if (to_del.heavy){ //if word heavy
                to_del.heavy = false;
                data.heavy = false;
                data.repeat_learn = 3;
            }else {  //if word not heavy
                to_del.learned = true;
                data.learned = true;
                learned.classList.remove('btn-success', 'btn-outline-success')
                if (to_del.learned){
                    learned.classList.add('btn-success');
                    }else{
                    learned.classList.add('btn-outline-success');
                }
            }
        }
        count_words.innerHTML = words_obj.length;
        document.getElementById("vvod").value = '';
        ok.style.display = 'none';
        err.style.display = 'block';
        dellete_word_button.style.display = 'none';
        answer.style.display = 'block';

    } else {  //wrong input
        if (control_state) {
            data.control = true
            let word_index = words_obj.indexOf(to_del);
            if (word_index !== -1) {
                words_obj.splice(word_index, 1);
            }
        }else{
            if (to_del.repeat_learn<7){
                to_del.repeat_learn = to_del.repeat_learn + 1
                data.repeat_learn = to_del.repeat_learn;
            }
        }
        document.getElementById("vvod").value = '';
        answer.style.display = 'block'
        answer.innerText = to_del.english + " - " + to_del.russian + "//" + to_del.repeat_learn + "//";
        ok.style.display = 'block'
        ok.innerText = inp + " - не верно.";
        err.style.display = 'none';
        dellete_word_button.style.display = 'inline';
        count_words.innerHTML = words_obj.length;
    }
    $.ajax({
            url: '/english/api/word/' + to_del.id + "/",
            method: 'PATCH',
            data: data,
            success: function (text) {
                console.log('__ok__');
            },
            error: function (text) {
                console.log('__error__');
                console.log(text);
                alert('error');
            },
    });


    dellete_word_button.onclick = function () {
        dell_word();
        console.log('Хоть и не верно  - удаляю');
        word_index_to_dell = words_obj.indexOf(to_del);
        if (word_index_to_dell !== -1) {
            words_obj.splice(word_index_to_dell, 1);
        }
        dellete_word_button.style.display = 'none';
        count_words.innerHTML = words_obj.length;

    }
    heavy.onclick = function () {
        to_del.heavy = !to_del.heavy
        $.ajax({
            url: '/english/api/word/' + to_del.id + "/",
            method: 'PATCH',
            data: {'heavy': to_del.heavy},
            success: function (text) {
                console.log('__ok__');
            },
            error: function (text) {
                console.log('__error__');
                console.log(text);
                alert('error');
            },
        });

        heavy.classList.remove('btn-dark', 'btn-outline-dark')
        if (to_del.heavy){
            heavy.classList.add('btn-dark');
        }else{
            heavy.classList.add('btn-outline-dark');
        }
    }
    important.onclick = function () {
        to_del.important = !to_del.important
        $.ajax({
            url: '/english/api/word/' + to_del.id + "/",
            method: 'PATCH',
            data: {'important': to_del.important},
            success: function (text) {
                console.log('__ok__');
            },
            error: function (text) {
                console.log('__error__');
                console.log(text);
                alert('error');
            },
        });

        important.classList.remove('btn-warning', 'btn-outline-warning')
        if (to_del.important){
            important.classList.add('btn-warning');
        }else{
            important.classList.add('btn-outline-warning');
        }
    }
    learned.onclick = function () {
        learned_f()
    }


    function dell_word(){

        if (to_del.repeat_learn > 0) {
            $.ajax({
                url: '/english/api/word/' + to_del.id + "/",
                method: 'PATCH',
                data: {'repeat_learn': to_del.repeat_learn - 1},
                success: function (text) {
                    console.log(text)
                },
                error: function (text) {
                    console.log(text);
                    alert(text);
                },
            });
        } else {
            if (to_del.heavy){
                to_del.heavy = !to_del.heavy
                $.ajax({
                    url: '/english/api/word/' + to_del.id + "/",
                    method: 'PATCH',
                    data: {'heavy': to_del.heavy,
                            'repeat_learn': 3
                    },
                    success: function (text) {
                        console.log('__ok__');
                    },
                    error: function (text) {
                        console.log('__error__');
                        console.log(text);
                        alert('error');
                    },
                });
            }else {
                learned_f()
            }
        }
    }
    function learned_f(){
        console.log('learned: staart');
        console.log(to_del);

        to_del.learned = !to_del.learned;
        console.log('learned:' + to_del.learned);
        $.ajax({
            url: '/english/api/word/' + to_del.id + "/",
            method: 'PATCH',
            data: {'learned': to_del.learned},
            success: function (text) {
                console.log('__ok__ learned : true');
            },
            error: function (text) {
                console.log('__error__');
                console.log(text);
                alert('error');
            },
        });

        learned.classList.remove('btn-success', 'btn-outline-success')
        if (to_del.learned){
        learned.classList.add('btn-success');
    }else{
        learned.classList.add('btn-outline-success');
    }
    }
}

submit_button.onclick = function () {
    start();
};
vvod.onsubmit = function () {
    start();
};

// Make sure this code gets executed after the DOM is loaded.
document.querySelector("#vvod").addEventListener("keyup", event => {
    if (event.key !== "Enter") return; // Use `.key` instead.
    document.querySelector("#submit_button").click(); // Things you want to do.
    event.preventDefault(); // No need to `return false;`.
});

