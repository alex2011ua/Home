let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

$.ajaxSetup({
    headers: {
        'X-CSRFToken': csrftoken
    }
});

let words_obj = 0;
$.ajax({
    url: '',
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
        alert('"Не получен список слов с сервера"');
    },
});
console.log(words_obj)


//
// let control_state = words_obj['control_state'];
// delete words_obj['control_state'];
// let words_list = Object.keys(words_obj);


let gerund = document.getElementById('gerund_button');
let infinitive = document.getElementById('infinitive_button');
let all_of_them = document.getElementById("all_of_them");
let to_button = document.getElementById('to_button');
let for_button = document.getElementById("for_button");
let make_button = document.getElementById('make_button');
let do_button = document.getElementById('do_button')
let countable_button = document.getElementById('countable_button');
let uncountable_button = document.getElementById('uncountable_button')

let count_words = document.getElementById("count_is");    // счетчик слов

let count_true = 0;
let count_false = 0;
let c_true = document.getElementById('count_true');
let c_false = document.getElementById('count_false');

let answer = document.getElementById("result");             // правильный ответ
document.getElementById("word").innerHTML = word.english;
let ok = document.getElementById("ok");
let err = document.getElementById("error");

let uptate_scrieen = function () {
    ind = Math.floor(Math.random() * words_obj.length);
    word = words_obj[ind];
    c_true.innerHTML = count_true;
    c_false.innerHTML = count_false;
    document.getElementById("word").innerHTML = word.word;
    count_words.innerHTML = words_obj.length;

    if (word.buttons.includes('gerund')) {
        gerund.style.display = 'inline';
    } else {
        gerund.style.display = 'none';
    }
    if (word.buttons.includes('infinitive')) {
        infinitive.style.display = 'inline';
    } else {
        infinitive.style.display = 'none';
    }
    if (word.buttons.includes('all')) {
        all_of_them.style.display = 'inline';
    } else {
        all_of_them.style.display = 'none';
    }
    if (word.buttons.includes('to')) {
        to_button.style.display = 'inline';
    } else {
        to_button.style.display = 'none';
    }
    if (word.buttons.includes('for')) {
        for_button.style.display = 'inline';
    } else {
        for_button.style.display = 'none';
    }
    if (word.buttons.includes('make')) {
        make_button.style.display = 'inline';
    } else {
        make_button.style.display = 'none';
    }
    if (word.buttons.includes('do')) {
        do_button.style.display = 'inline';
    } else {
        do_button.style.display = 'none';
    }
    if (word.buttons.includes('count')) {
        countable_button.style.display = 'inline';
    } else {
        countable_button.style.display = 'none';
    }
    if (word.buttons.includes('uncount')) {
        uncountable_button.style.display = 'inline';
    } else {
        uncountable_button.style.display = 'none';
    }
}
uptate_scrieen();

function start(button_pressed) {
    let inp = button_pressed;

    if (inp.toLowerCase() === word.answer) {
        console.log('верно - удаляю');
        answer.innerText = word.word + " - " + word.answer + ' ' + word.russian;
        count_true++;
        words_obj.splice(ind, 1)
        ok.style.display = 'block';
        err.style.display = 'none';
        answer.style.display = 'block';
    } else {
        count_false++;
        answer.style.display = 'block'
        answer.innerText = word.word + " - " + word.answer + ' ' + word.russian;
        ok.style.display = 'none';
        err.innerText = inp + " - не верно.";
        err.style.display = 'block';
        words_obj.splice(ind, 1)
    }

    uptate_scrieen();
}

gerund.onclick = function () {
    start('gerund');
};
infinitive.onclick = function () {
    start('infinitive');
};
all_of_them.onclick = function () {
    start('all');
};
to_button.onclick = function () {
    start('to');
};
for_button.onclick = function () {
    start('for');
};
make_button.onclick = function () {
    start('make');
};
do_button.onclick = function () {
    start('do');
};
countable_button.onclick = function () {
    start('count');
};
uncountable_button.onclick = function () {
    start('uncount');
};

