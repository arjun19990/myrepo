var qbd = qbd || {};
qbd.actionsteps = function () {

//Create task to selected Action step 

function createTask(){
debugger;
//first comment

//Get an array of entity references for all selected rows in the subgrid
var selectedEntityReferences = [];
var selectedRows = Xrm.Page.getControl("Action_Steps").getGrid().getSelectedRows();

 
selectedRows.forEach(function (selectedRow, i) {
 selectedEntityReferences.push(selectedRow.getData().getEntity().getEntityReference());
});
// var attributes = selectedRows.getData().getEntity().getAttributes().getAll();
var id = selectedEntityReferences;


  var req = new XMLHttpRequest();
  var url ="https://prod-56.westus.logic.azure.com:443/workflows/2cd1f211f01e4067875c76fb03e9fa6f/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=7b0RdLjMtOURJEJbFcCsgBCCC75G4MGqrOCqXmsjWPA";
  req.open("POST", url, true);
  req.setRequestHeader('Content-Type', 'application/json');
  req.send(JSON.stringify({
    "stepId": selectedEntityReferences
  }));
 
Xrm.Utility.showProgressIndicator("Submitting....");
    setTimeout(function(){ 
	closeProgress();
	
	},5000);
}
function closeProgress(){
Xrm.Utility.closeProgressIndicator();
}

function setExecutionStatus()
{
debugger;
var entityName = Xrm.Page.data.entity.getEntityName();
if (entityName == "qbd_capa")
 Xrm.Page.getAttribute("qbd_executionstatus").setValue(0);	
else if (entityName == "qbd_changecontrol")
	Xrm.Page.getAttribute("qbd_overallactionstepstatus").setValue(0);	
}
 
 function enableSubmitBtn()
 {
 debugger;

// var flag = Xrm.Page.getAttribute("qbd_issubmitted").getValue();

//Get an array of entity references for all selected rows in the subgrid
var getGridRows = [];
var flag = Xrm.Page.getControl("Action_Steps").getGrid().getSelectedRows();

 
flag.forEach(function (selectedRow, i) {
 getGridRows.push(selectedRow.getData().getEntity().getAttributes().getAll());
});
// var attributes = selectedRows.getData().getEntity().getAttributes().getAll();
	if (flag == 0 || flag == null)
	{
		return true;
	} 
else{
		return false;
	}
 }
 


return {
        'createTask': createTask,
		'setExecutionStatus': setExecutionStatus,
        'enableSubmitBtn' : enableSubmitBtn
       };
}();