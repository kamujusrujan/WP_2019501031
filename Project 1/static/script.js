function book_html(id) {
	clearList();
    const request = new XMLHttpRequest();
    request.open("POST", "/api/book_details?isbn=" + id)
    request.send()
    request.onload = () => {
        const response = JSON.parse(request.responseText)
        console.log(response)

        if (response["status"] == 200) {
            const reviews = response.reviews
            // let row = document.querySelector(".row");
            const row = document.createElement("div")
            row.setAttribute("class", "row");


            let col_book = document.createElement("div")
            col_book.setAttribute("class", "col-md-4 col-md-4")

            let card = document.createElement("div")
            card.setAttribute("class", "card")

            let card_overlay = document.createElement("div")
            card_overlay.setAttribute("class", "card-body")

            let title = document.createElement("h5")
            title.setAttribute("class", "card-title")
            title.innerHTML = `Title: ${response.title}`

            let author = document.createElement("p")
            author.setAttribute("class", "card-text")
            author.innerHTML = `Author: ${response.author}`

            let isbn = document.createElement("p")
            isbn.setAttribute("class", "card-text")
            isbn.innerHTML = `ISBN: ${response.isbn}`

            let year = document.createElement("p")
            year.setAttribute("class", "card-text")
            year.innerHTML = `Year: ${response.year}`

            card_overlay.appendChild(title)
            card_overlay.appendChild(author)
            card_overlay.appendChild(isbn)
            card_overlay.appendChild(year)

            card.appendChild(card_overlay)
            col_book.appendChild(card)
            row.appendChild(col_book)

            let review_col = document.createElement("div")
            review_col.setAttribute("class", "col-md-6 col-md-6")

            let heading = document.createElement("h2")
            heading.innerHTML = `Reviews: `


            let tp = document.createElement("p")
            tp.innerHTML = `You can give your review in the review section below.`

            console.log(reviews)

            if (reviews == null) {
                let tp1 = document.createElement("p")
                tp1.innerHTML = `No reviews yet`
                row.appendChild(tp1)

            } else {
                reviews.map((review) => {
                    let display_rev = document.createElement("div")
                    display_rev.setAttribute("class", "test")

                    let rev_name = document.createElement("p")
                    rev_name.innerHTML = `User Name: ${review.name}`

                    let rev_rating = document.createElement("p")
                    rev_rating.innerHTML = `Rating: ${review.rating}`

                    let rev_desc = document.createElement("p")
                    rev_desc.innerHTML = `description: ${review.description}`

                    display_rev.appendChild(rev_name)
                    display_rev.appendChild(rev_rating)
                    display_rev.appendChild(rev_desc)
                    review_col.appendChild(display_rev)
                    row.appendChild(review_col)
                })
            }
            document.querySelector('#jscontent').appendChild(row);

            addrev(id)
			
        } else {
            return "Invalid isbn"
        }
    }
}
