function showModal(table, data) {
  let row = table.getSelection()[0].row;
    let trueChecked = Boolean(data.getValue(row,8))? 'checked="checked"' : '';
    let falseChecked = !Boolean(data.getValue(row,8))? 'checked="checked"' : '';
    let formHtml = `
    <form action="update" method="post">
      <div class="form-group">
        <label for="id">Id: </label>
        <input class="form-control" type="text" id="id" name="id" value="${data.getValue(row,0)}" readonly>
      </div>
      <div class="form-group">
        <label for="date">Date: </label>
        <input class="form-control" type="text" id="date" name="date" value="${data.getValue(row,1)}">
      </div>

      <div class="form-group">
        <label for="month">Month: </label>
        <input class="form-control" type="text" id="month" name="month" value="${data.getValue(row,2)}">
      </div>

      <div class="form-group">
        <label for="store">Store: </label>
        <input class="form-control" type="text" id="store" name="store" value="${data.getValue(row,3)}">
      </div>

      <div class="form-group">
        <label for="amount">Amount: </label>
        <input class="form-control" type="number" step="0.01" id="amount" name="amount" value="${data.getValue(row,4)}">
      </div>

      <div class="form-group">
        <label for="category">Category: </label>
        <input class="form-control" type="text" id="category" name="category" value="${data.getValue(row,5)}">
      </div>

      <div class="form-group">
        <label for="bank">Bank: </label>
        <input class="form-control" type="text" id="bank" name="bank" value="${data.getValue(row,6)}">
      </div>

      <div class="form-group">
        <label for="notes">Notes: </label>
        <input class="form-control" type="text" id="notes" name="notes" value="${data.getValue(row,7)}">
      </div>

      <div class="form-check">
          <label class="form-check-label">Excluded: </label>
          <label class="form-check-label"><input type="radio" name="radio" value="True" ${trueChecked} > True </label>
          <label class="form-check-label"><input type="radio" name="radio" value="False" ${falseChecked}> False </label>
      </div>
      <div class="container text-right">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button onclick="deleteButtonCall(${data.getValue(row,0)})" class="btn btn-danger">Delete</a> 
        <button type="submit" class="btn btn-info">Edit</button>
      </div>
    </form>`;
    $("#modal-body").html(formHtml); 
    $('#myModal').modal('show');
}


function deleteButtonCall(id){
  let confirmValue = confirm(`Do u want to delete the record with the Id ${id}` );
  if (confirmValue === true){
    //TODO: handle the error if the month page no longer exist
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", `/deleteRecord/${id}`, false);
    xhttp.send();
  }
}

const FULL_TABLE_COLUMNS = [ 
  {type: "number", label: "id"}, 
  {type: "string", label: "Date"}, 
  {type: "string", label: "Month"}, 
  {type: "string", label: "Store"},
  {type: "number", label: "Amount"},
  {type: "string", label: "Category"},
  {type: "string", label: "Bank"},
  {type: "string", label: "Notes"},
  {type: "number", label: "Excluded"}];

const STORE_AMOUNT_COLUMNS = [
  {type:'string', label:'Store'},
  {type:'number', label:'Amount'}
];

function drawTable(
  rowsData, 
  tableHtmlId, 
  showEditModal = true,
  columnLables = FULL_TABLE_COLUMNS) {
  let data = new google.visualization.DataTable();

  columnLables.forEach(({type, label}) => data.addColumn(type, label));

  data.addRows(rowsData);
  
  let table = new google.visualization.Table(document.getElementById(tableHtmlId));
  table.draw(data, {showRowNumber: true, width: '100%', height: '100%'});

  if (showEditModal){
    google.visualization.events.addListener(table, 'select', () => showModal(table, data));
  }
}    

const PIE_CHART_COLUMNS = [
  {type:'string', label: 'Category'}, 
  {type: 'number', label: 'Total'}];

function drawPieChart(
  rowsData, 
  chartHtmlId,
  title, 
  columnLables=PIE_CHART_COLUMNS){

  let dataTable = new google.visualization.DataTable();

  columnLables.forEach(({type, label}) => dataTable.addColumn(type, label));
  dataTable.addRows(rowsData);

  let options = {'title':title, 'width':550, 'height':400};

  let chart = new google.visualization.PieChart(document.getElementById(chartHtmlId));
  chart.draw(dataTable, options);
}
  