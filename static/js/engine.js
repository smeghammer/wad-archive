let engine = {

	fileCount : -1,

	init : function(){
		console.log('in init');
		/* which page are we loading? */
		let startup = document.getElementById('body').getAttribute('data-init-action');
		console.log(startup);
		
		switch(startup){
			case 'list-files':
				this.loadFiles();
			break;
			default:
				
		}
	},
	
	/**
	fetch('http://example.com/movies.json')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    console.log(myJson);
    
    
    https://stackoverflow.com/questions/50776445/vanilla-javascript-version-of-ajax
  });
	 */
	loadFiles: function(){
		
		/** may need to load this asynchronously */
		//this.getFileCount();
		
		/** look for pagination flags */
		let pageSize = document.getElementById('body').getAttribute('data-page-size');
		console.log(pageSize);
		fetch('/app/files/'+pageSize + '/0')
		.then(function(response){
			/** NOTE: return the filecount as part of the pagination response data! */
			data = response.json();
			return(data);
		})
		.then(function(json_data){
			//console.log(json_data);
			engine.buildFileLinks(json_data)
			/** and load the filecount */
			 //return( engine.getFileCount() );
		})
		//.then(function(filecount){
		//	engine.fileCount =  filecount;
		//	console.log(engine.fileCount);
		//})
	},
	
//	getFileCount : function(){
//		fetch('/app/count')
//		.then(function(response){
//			data = response.text();
//			return(data);
//		})
//		.then(function(count_data){
//			console.log(count_data);
//			return(count_data);
//		})
//	},
	
	buildPaginator : function(currentPage, pageSize, recordCount){
		
	},
	
	buildFileLinks : function(fileData){
		//console.log(fileData)
		/** empty the container */
		let elem = document.getElementById('filelist')
		elem.innerHTML = "";
		let _ul = document.createElement('ul');
		for(let counter = 0; counter<fileData.page_data.length;counter++){
			console.log(fileData.page_data[counter]);
			let test = document.createElement('li');
			test.appendChild(this.buildFileLink(fileData.page_data[counter]._id,fileData.page_data[counter]['filenames'][0]));
			test.appendChild(document.createTextNode(fileData.page_data[counter]['filenames'][0]));
			_ul.appendChild(test);
		}
		elem.appendChild(_ul);
	},
	
	buildFileLink : function(fileguid, filename){
		let _linkelem = document.createElement('a');
		_linkelem.setAttribute('href','/app/file/' + fileguid);
		_linkelem.setAttribute('title','Download' + filename);
		_linkelem.appendChild(document.createTextNode(filename));
		return(_linkelem);
	}
	
}
console.log('script loaded');
engine.init();