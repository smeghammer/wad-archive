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
	loadFiles: function(pageNum){
		pNum = 0;
		if(pageNum){
			pNum = pageNum;
		}
		/** look for pagination flags */
		let pageSize = document.getElementById('body').getAttribute('data-page-size');
		console.log(pageSize);
		fetch('/app/files/'+pageSize + '/' + pNum)
		.then(function(response){
			/** NOTE: return the filecount as part of the pagination response data! */
			data = response.json();
			return(data);
		})
		.then(function(json_data){
			console.log(json_data);
			engine.buildFileLinks(json_data);
			engine.buildPaginator(json_data.page_num,json_data.page_size,json_data.item_count);
		})
	},
	
	//http://127.0.0.1:5000/app/files/20/0
	buildPaginator : function(currentPage, pageSize, recordCount){
		
		let num_pages = Math.ceil(recordCount/pageSize);
		let paginator = document.createElement('div');
		let prevtag = document.createElement('a');
		let nexttag = document.createElement('a');
		let summary_tag = document.createElement('span');
		summary_tag.appendChild(document.createTextNode('Page ' + currentPage + ' of '+num_pages))
		prevtag.setAttribute('class','paginator_prev');
		nexttag.setAttribute('class','paginator_next');
		prevtag.setAttribute('id','paginator_prev');
		nexttag.setAttribute('id','paginator_next');
		prevtag.appendChild(document.createTextNode(' < '));
		nexttag.appendChild(document.createTextNode(' > '));
		
		console.log(currentPage, pageSize,num_pages, recordCount);
		if(currentPage < num_pages){
			// make next link
		}
		if(currentPage > 0){
			// make prev link
		}
		//https://gomakethings.com/listening-for-click-events-with-vanilla-javascript/
		prevtag.addEventListener('click',function(){
			console.log('clicked prev')
			engine.loadFiles((parseInt(currentPage) - 1));
		});
		nexttag.addEventListener('click',function(){
			console.log('clicked next');
			engine.loadFiles((parseInt(currentPage) + 1));
		});
		
		paginator.appendChild(prevtag);
		paginator.appendChild(summary_tag);
		paginator.appendChild(nexttag);
		
		/** append click handlers */
		
		
		let elem = document.getElementById('paginator');
		elem.innerHTML = "";
		elem.appendChild(paginator);
	},
	
	buildFileLinks : function(fileData){
		/** empty the container */
		let elem = document.getElementById('filelist')
		elem.innerHTML = "";
		let _ul = document.createElement('ul');
		for(let counter = 0; counter<fileData.page_data.length;counter++){
			console.log(fileData.page_data[counter]);
			let test = document.createElement('li');
			test.appendChild(this.buildFileLink(fileData.page_data[counter]._id,fileData.page_data[counter]['filenames'][0]));
			_ul.appendChild(test);
		}
		elem.appendChild(_ul);
	},
	
	buildFileLink : function(fileguid, filename){
		let _linkelem = document.createElement('a');
		_linkelem.setAttribute('href','/app/file/' + fileguid);
		_linkelem.setAttribute('title','Download ' + filename);
		_linkelem.appendChild(document.createTextNode(filename));
		return(_linkelem);
	},
	
	buildPaginationLink : function(direction, currentPage, recordcount){
		let newpage = currentPage;
		switch(direction){
			case -1:	//back
				newpage--;
			break;
			case 1:		//forward
				newpage++;
			break;
		}
	}
	
}
console.log('script loaded');
engine.init();