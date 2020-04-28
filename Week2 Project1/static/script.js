
document.addEventListener('DOMContentLoaded',function(){
	document.querySelector('.error').style.visibility = 'hidden';
	document.querySelector(".btn").onclick = ()=>{ 	
		const mailElement  = document.querySelector('input[name="mailid"]');
		if(mailElement != null){
			var mailid = mailElement.value;
		}
		const passElement  = document.querySelector('input[name="password"]');
		if(passElement != null){
			var password = passElement.value;
		}
		if(!(checkMail(mailid) && checkPassword(password))){
			document.querySelector('.error').style.visibility = 'visible';
			mailElement.value = "";
			passElement.value = "";
			return false;
		}

	};

});



function checkMail(mailid){
	if(mailid == null || !mailid.includes('@'))
		return false;
	return mailid.match(/\S+@\S+\.\S+/) != null;
}


function checkPassword(password){
	if(password == null)
		return false;
	// console.log(password.match(/((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{6,20})/));
	return password.match(/((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{6,20})/) != null ;
}

