



function deepEqual(obj1,obj2){
	const keys1 = Object.keys(obj1), keys2 = Object.keys(obj2)
	if(keys1.length != keys2.length)
		return false
	for (var i = 0; i < keys1.length; i++) {
		const k = keys1[i]
		if( typeof obj1[k] == "object" && typeof obj2[k] == "object" ){
			if (!deepEqual(obj1[k],obj2[k]))
				return false
		}
		else if(obj1[k] === obj2[k])
			continue
		else{
			return false
		}
	}
	return true
}


const student = {
	name:'srujan',
	grade : 'b',
	circle : {
		f:3
	} 
}




const student2 = {
	name:'srujan',
	circle : {
		f:3
	} ,
	grade : 'b'
	}




const student3 = {
	name:'kiran',
	grade : 'a+',
	circle : {
		f:2
	} 
}


const student4 = {
	name:'sourabh',
	grade : 'a+',
	circle : {
		f:2
	} 
}



console.log(deepEqual(student,student2));
console.log(deepEqual(student,student3));
console.log(deepEqual(student4,student4));
