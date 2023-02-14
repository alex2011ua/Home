let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

$.ajaxSetup({
    headers: {
        'X-CSRFToken': csrftoken
    }
});

let words_obj = 0;
$.ajax({
    url: '/english/api/r_e_words',
    method: 'POST',
    data: 'data',
    async: false,
    success: function (text) {
        console.log('__ok__');
        words_obj = text;
    },
    error: function (text) {
        console.log('__error__');
        console.log(text);
        alert('"Не получен "');
    },
});

let control_state = words_obj['control_state'];
delete words_obj['control_state'];
let words_list = Object.keys(words_obj);
let ind = Math.floor(Math.random() * words_list.length);
let word = words_list[ind];
let translate = words_obj[words_list[ind]];
var dellete_word_button = document.getElementById('dellete_word'); // кнопка для удаления слова
var learned = document.getElementById('learned'); // кнопка для выученого слова
var heavy = document.getElementById('heavy'); // кнопка для сложного слова
var not_heavy = document.getElementById('not_heavy'); // кнопка для сложного слова
var count_words = document.getElementById("count_is");    // счетчик слов
var submit_button = document.getElementById("submit_button");    // счетчик слов
var vvod = document.getElementById("vvod");    // счетчик слов
count_words.innerHTML = words_list.length;
console.log(words_obj[words_list[ind]], words_list[ind]);
let answer = document.getElementById("result");             // правильный ответ
document.getElementById("word").innerHTML = words_list[ind];
let ok = document.getElementById("ok");
let err = document.getElementById("error");

function start() {
    let inp = document.getElementById("vvod").value.trim();
    let to_del = word;
    if (inp.toLowerCase() === translate.toLowerCase()) {
        console.log('верно - удаляю');
        answer.innerText = translate + " - " + word;
        delete words_obj[word];
        words_list = Object.keys(words_obj);
        document.getElementById("vvod").value = '';
        ok.style.display = 'none';
        err.style.display = 'block';
        dellete_word_button.style.display = 'none';
        answer.style.display = 'block';
        if (control_state === true) {
            learnedFunc();
        }
        ;
    } else {
        document.getElementById("vvod").value = '';
        console.log("не верно");
        answer.style.display = 'block'
        answer.innerText = translate + " - " + word;
        ok.style.display = 'block'
        ok.innerText = inp + " - не верно.";
        err.style.display = 'none';

        dellete_word_button.style.display = 'inline';
        if (control_state === true) {
            delete words_obj[to_del];
            words_list = Object.keys(words_obj);
            console.log('Хоть и не верно  - удаляю');
            dellete_word_button.style.display = 'none';
            control();
        }
    }

    dellete_word_button.onclick = function () {
        delete words_obj[to_del];
        words_list = Object.keys(words_obj);

        console.log('Хоть и не верно  - удаляю');
        dellete_word_button.style.display = 'none';

    }



    function control() {
        console.log(to_del);
        $.ajax({
            url: 'mod/',
            method: 'GET',
            data: {'control': to_del},
            success: function (text) {
                console.log('control ok' + to_del)
            },
            error: function (text) {
                console.log(text);
                alert(text);
            },
        });
    }

    function learnedFunc() {
        console.log("sdf")
    }

    learned.onclick = learnedFunc;

    heavy.onclick = function () {
        console.log(to_del);
        $.ajax({
            url: 'mod/',
            method: 'GET',
            data: {'heavy': true},
            success: function (text) {
                console.log('__ok__');
            },
            error: function (text) {
                console.log('__error__');
                console.log(text);
                alert('error');
            },
        });
    }
        not_heavy.onclick = function () {
        console.log(to_del);
        $.ajax({
            url: 'mod/',
            method: 'GET',
            data: {'heavy': false},
            success: function (text) {
                console.log('__ok__');
            },
            error: function (text) {
                console.log('__error__');
                console.log(text);
                alert('error');
            },
        });
    }


    ind = Math.floor(Math.random() * words_list.length);
    word = words_list[ind];
    translate = words_obj[words_list[ind]];
    console.log(words_obj[words_list[ind]], words_list[ind]);
    document.getElementById("word").innerHTML = words_list[ind];
    count_words.innerHTML = words_list.length;
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

