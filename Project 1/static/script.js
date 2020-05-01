function addrev(id){ 
    const review_holder = document.createElement("div");
            review_holder.setAttribute('class', 'review_section')
            review_holder.innerHTML = `
                <hr>

                  <center id = "err"> </center> 
                  <br>
                  <h4>Add a Review to the book </h4>
                  <div class="form-row">
                    <div class="form-group col-md-6">
                      <label for="inputCity">Description</label>
                      <textarea name = "description"  class="form-control" > </textarea>
                    </div>
                    <div class="form-group col-md-2">
                      <label for="inputState">Rating</label>
                      <select name="rating" class="form-control">
                        <option selected>Choose...</option>
                        <option>1</option>
                        <option>2</option>
                        <option>3</option>
                        <option>4</option>
                        <option>5</option>
                      </select>
                    </div>
                </div>
                  <button type="submit" id ='review_button' class="btn btn-primary">Submit</button>
            `
    document.querySelector('#jscontent').appendChild(review_holder);
    document.querySelector("#review_button").onclick = ()=>{
        let d = document.querySelector('textarea[name = "description"]').value;
        let s = document.querySelector('select[name = "rating"]').value;
        review_book(id,d,s);
    }
}




function review_book(isbn,desc,star){

	const uname = document.querySelector("#username").textContent;
	// console.log(uname,id,d,s);
	const request = new XMLHttpRequest();
    let params = '?description='+desc+'&isbn='+id+'&mailid='+uname+'&stars='+star

    request.open('POST', '/api/submit_review' + params)
    request.send()
    request.onload = ()=>{
    	let data = JSON.parse(request.responseText);
    	if(data['status'] == 200)
    		book_html(id)
		else{
			const err = document.querySelector("#err")
			err.innerHTML =  `Error` + data['status'] 	
		}
    }
}
