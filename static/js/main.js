// making pagination works with search querys adding the 
// page number as an input value inside de search form
let searchform = document.getElementById('searchform')
let pageLinks = document.getElementsByClassName('page-link')
if (searchform) {
    for (let i=0; pageLinks.length > i; i++) {
        pageLinks[i].addEventListener('click', function (event) {
            event.preventDefault()
            // Getting the data attribute from pagination buttons
            let page_number = this.dataset.page
            // Putting the page number value inside search form
            searchform.innerHTML += `<input value=${page_number} name="page" hidden/>`
            searchform.submit()
        })
    }
}