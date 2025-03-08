let button = document.getElementById('generator');
let long = document.getElementById('long-cb');
let complex = document.getElementById('complex-cb');
let passwordDisplay = document.getElementById('password-display');

button.addEventListener('click', function() {
    document.body.style.backgroundColor = "red"; // Just for fun!
    let length = long.checked ? 16 : 8;
    let charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    if (complex.checked) {
        charset += "!@#$%^&*()_+~`|}{[]:;?><,./-=";
    }
    passwordDisplay.textContent = generatePassword(length, charset);
});

function generatePassword(length, charset) {
    let password = "";
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * charset.length);
        password += charset[randomIndex];
    }
    return password;
}
