function clearList() {
    const error_text = document.querySelector('.book-list')
    error_text.innerHTML = ''

    var row = document.querySelector(".row");
    row.innerHTML = ''
}

function clearFields() {
    document.querySelector('#isbn').value = ''
    document.querySelector('#title').value = ''
    document.querySelector('#author').value = ''
    document.querySelector('#year').value = ''
}

function search_html() {
    const isbn = document.querySelector('#isbn').value
    const title = document.querySelector('#title').value
    const author = document.querySelector('#author').value
    const year = document.querySelector('#year').value
    let params = '?isbn='+isbn+'&title='+title+'&author='+author+'&year='+year
        
    const request = new XMLHttpRequest();

    request.open('POST', '/api/search'+params)
    request.send()

    // let response = ''
    request.onload = () => {
        const response = JSON.parse(request.responseText)
        console.log(response)
        const book_query = document.querySelector('.row')
        clearFields()
        if (response.status == 200) {
            clearList()

            const book_list = response.books
            book_list.map((book) => {

                let col = document.createElement('div')
                col.setAttribute('class', 'col-5')

                let card = document.createElement('div')
                card.setAttribute('class', 'card')

                let card_body = document.createElement('div')
                card_body.setAttribute('class', 'card-body')                    

                let card_title = document.createElement('h5')
                card_title.setAttribute('class', 'card-title')                    
                card_title.innerHTML = `Title: ${book.title}`

                let text_isbn = document.createElement('p')
                text_isbn.setAttribute('class', 'card-text')                    
                text_isbn.innerHTML = `ISBN: ${book.isbn}`

                let text_author = document.createElement('p')
                text_author.setAttribute('class', 'card-text')                    
                text_author.innerHTML = `Author: ${book.author}`

                let text_year = document.createElement('p')
                text_year.setAttribute('class', 'card-text')                    
                text_year.innerHTML = `Year: ${book.year}`

                let open_btn = document.createElement('button')
                open_btn.setAttribute('class', 'btn btn-primary')
                open_btn.setAttribute('data-value',`${book.isbn}`)
                open_btn.innerHTML = 'Open'

                card_body.appendChild(card_title)
                card_body.appendChild(text_isbn)
                card_body.appendChild(text_author)
                card_body.appendChild(text_year)
                card_body.appendChild(open_btn)

                card.appendChild(card_body)
                col.appendChild(card)
                book_query.appendChild(col)

                document.querySelectorAll('.btn-primary').forEach(button => {
                    
                    button.onclick = () => {
                        
                        console.log('something ' + button.dataset.value)
                        const num = button.dataset.value
                        clearList()
                        book_html(num)
                        return false
                    }
                })



            })
        } 
        else {
            clearList()

            let error = document.createElement('h4')
            error.setAttribute('class', 'text-center')
            error.innerHTML = "No books with given parameters"
            document.querySelector('#books_resp').appendChild(error)
        }
            
    }

    main()
}

function book_html(isbn){
    
    
}

function main() {
    console.log('main')
    document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.btn-secondary').onclick = function() {
        
        search_html()
        return false
    }
    });    
}


main()