function submitCode() {

        const code = document.getElementById('userCode').value
        const display = document.getElementById('responseMessage');

        display.innerText = "Code Entered: " + code;

        display.style.color = "green";

}

function openModal() {
    document.getElementById("myModal").style.display = "block";
}

function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

var slideIndex = 1;

function plusSlides(n) {
    showSlides(slideIndex += n)
}

function currentSlide(n) {
    showSlides(slideIndex = n)
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");

    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    slides[slideIndex-1].style.display = "block"
}

window.onclick = function(event) {
    var modal = this.document.getElementById("myModal");
    if (event.target == modal) {
        closeModal();
    }
}