let engine = {

	fileCount : -1,
	init : function(){
		console.log('in init');
		/* which page are we loading? */
		let startup = document.getElementById('body').getAttribute('data-init-action');
		switch(startup){
			case 'list-files':
			
			/** append handler to search button: */
			let btn = document.getElementById('searchbtn');
			btn.addEventListener('click',function(){
				engine.loadFiles(0,document.getElementById('searchfield').value);
			});	
			this.loadFiles();
			break;
			default:
		}
	},
	
	/**
	 * https://stackoverflow.com/questions/50776445/vanilla-javascript-version-of-ajax
	 */
	loadFiles: function(pageNum,filter,num_pages){
		f=''
		if(filter)
		{
			f='?filter='+filter
		}
		console.log('loadfiles filter: ', filter)
		console.log('loadfiles num pages: ', num_pages)
		pNum = 0;
		if(pageNum && pageNum>0){
			pNum = pageNum;
		}
		else{
			console.log('neg pagenum! ',pageNum)
		}
		
		if(pageNum >= num_pages){
			pNum = num_pages-1;
		}
		/** look for pagination flags */;
		let pageSize = document.getElementById('body').getAttribute('data-page-size');
		console.log(pageSize);
		fetch('/app/files/'+pageSize + '/' + pNum + f)
		.then(function(response){
			/** NOTE: return the filecount as part of the pagination response data! */
			data = response.json();
			return(data);
		})
		.then(function(json_data){
			console.log(json_data);
			engine.buildFileLinks(json_data);
			engine.buildPaginator(json_data.page_num,json_data.page_size,json_data.item_count);
		});
	},
	
	//http://127.0.0.1:5000/app/files/20/0 - todo: refactor to remove redundant pageSixe arg
	buildPaginator : function(currentPage, pageSize, recordCount){
		
		let num_pages = Math.ceil(recordCount/pageSize);
		let paginator = document.createElement('div');
		let prevtag = document.createElement('a');
		let nexttag = document.createElement('a');
		
		let prevtag2 = document.createElement('a');
		let nexttag2 = document.createElement('a');
		
		let summary_tag = document.createElement('span');
		
		let filecount = document.getElementById('filecount');
		summary_tag.appendChild(document.createTextNode('Page ' + (currentPage+1) + ' of ' + num_pages))
		prevtag.setAttribute('class','paginator_prev');
		nexttag.setAttribute('class','paginator_next');
		prevtag.setAttribute('title','Go back a page');
		nexttag.setAttribute('title','Go forward a page');
		prevtag.setAttribute('id','paginator_prev');
		nexttag.setAttribute('id','paginator_next');
		prevtag.appendChild(document.createTextNode(' < '));
		nexttag.appendChild(document.createTextNode(' > '));
		
		prevtag2.setAttribute('class','paginator_prev');
		nexttag2.setAttribute('class','paginator_next');
		prevtag2.setAttribute('title','Jump back 50 pages');
		nexttag2.setAttribute('title','Jump forward 50 pages');
		prevtag2.setAttribute('id','paginator_prev2');
		nexttag2.setAttribute('id','paginator_next2');
		prevtag2.appendChild(document.createTextNode(' << '));
		nexttag2.appendChild(document.createTextNode(' >> '));
		filecount.innerHTML = '';
		filecount.appendChild(document.createTextNode(recordCount + ' files'));
		console.log(currentPage, pageSize,num_pages, recordCount);
/*		if(currentPage < num_pages){
			// make next link
		}
		if(currentPage > 0){
			// make prev link
		}*/
		//https://gomakethings.com/listening-for-click-events-with-vanilla-javascript/
		prevtag.addEventListener('click',function(){
			engine.loadFiles((parseInt(currentPage) - 1),document.getElementById('searchfield').value, num_pages);
		});
		prevtag2.addEventListener('click',function(){
			engine.loadFiles((parseInt(currentPage) - 50),document.getElementById('searchfield').value, num_pages);
		});		
		
		nexttag.addEventListener('click',function(){
			engine.loadFiles((parseInt(currentPage) + 1),document.getElementById('searchfield').value, num_pages);
		});
		nexttag2.addEventListener('click',function(){
			engine.loadFiles((parseInt(currentPage) + 50),document.getElementById('searchfield').value, num_pages);
		});
		
		paginator.appendChild(prevtag2);
		paginator.appendChild(prevtag);
		paginator.appendChild(summary_tag);
		paginator.appendChild(nexttag);
		paginator.appendChild(nexttag2);

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
			let test = document.createElement('li');
			test.appendChild(this.buildFileLink(fileData.page_data[counter]._id,fileData.page_data[counter]['filenames'][0]));
			_ul.appendChild(test);
		}
		elem.appendChild(_ul);
	},
	
	buildFileLink : function(fileguid, filename,isDownloadLink){
		let _linkelem = document.createElement('a');
		_linkelem.setAttribute('data-fileguid',fileguid);
		if(isDownloadLink){
			_linkelem.setAttribute('href','/app/file/' + fileguid);
			_linkelem.setAttribute('title','Download ' + filename);
		}
		else{
			_linkelem.setAttribute('href','#');
			_linkelem.setAttribute('title','Details for ' + filename);
			_linkelem.addEventListener('click',function(){
				engine.buildFileDetails(this.getAttribute('data-fileguid'));
			});
		}

		_linkelem.appendChild(document.createTextNode(filename));
		return(_linkelem);
	},
	
	buildFileDetails : function(fileguid){
		console.log('get details by this: ',fileguid);
		fetch('/app/file/details/' + fileguid)
		.then(function(response){
			/** NOTE: return the filecount as part of the pagination response data! */
			data = response.json();
			console.log(data)
			return(data);
		})
		.then(function(json_data){
			console.log(json_data);
			/** empty the containers */
			document.getElementById('detail_name').innerHTML = '';
			document.getElementById('detail_readme').innerHTML = '';
			document.getElementById('detail_download').innerHTML = '';
			document.getElementById('detail_maps').innerHTML = '';
			document.getElementById('detail_screenshots').innerHTML = '';
			document.getElementById('detail_graphics').innerHTML = '';
			
			document.getElementById('detail_name').appendChild(document.createTextNode(json_data['record_filename']));
			let linkElem = engine.buildFileLink(json_data['record_identifier'],json_data['record_filename'],true);
			document.getElementById('detail_download').appendChild(linkElem);
			//https://developer.mozilla.org/en-US/docs/Web/CSS/white-space
			document.getElementById('detail_readme').appendChild(document.createTextNode(json_data['record_readme']));
			
			//this.buildFileLink(fileData.page_data[counter]._id,fileData.page_data[counter]['filenames'][0])
		});
		/** get the heading block and pushin the filename (trimmed) */
	},

	buildPaginationLink : function(direction, currentPage, filecount){
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