// GLOBAL FUNCTIONS //

var categoryNumber = 0; // INIT VALUE FOR SEARCH IN EVERY TABLE

// GET THE SEARCH VALUE FROM THE HTML
function ChosenCategory(index) {
  categoryNumber = index;
}

// SEARCH ACORDING TO THE USER CHOICE
function searchByCategoryFunc() {
  table = document.getElementById("chessboard");
  inactives = document.querySelectorAll("[id=inactive]").length;
  var num = categoryNumber;
  // Declare variables
  var input, filter, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  tr = table.getElementsByTagName("tr");
  // Loop through all table rows, and hide those who don't match the search query
  if (dpMode == 1) {
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[num];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  } else if (dpMode == 2) {
    for (i = 0; i < tr.length - inactives; i++) {
      td = tr[i].getElementsByTagName("td")[num];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  } else if (dpMode == 3) {
    for (i = tr.length - inactives; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[num];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }
}

// INIT DISPLAY MODE OF THE TABLES
var dpMode = 2;

// FILTERING THE TABLES ACORDING TO THE USER CHOICE OF THE DISPLAY MODE
function changeDisplayMode(index) {
  dpMode = index;
  table = document.getElementById("chessboard");
  // Declare variables
  var tr, i;
  tr = table.getElementsByTagName("tr");
  // Loop through all table rows, and hide those who don't match the search query
  if (dpMode === "1") {
    for (i = 1; i < tr.length; i++) {
      tr[i].style.display = "";
    }
  }
  if (dpMode === "2") {
    for (i = 1; i < tr.length; i++) {
      if (tr[i].attributes.id.value === "active") {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
  if (dpMode === "3") {
    for (i = 1; i < tr.length; i++) {
      if (tr[i].attributes.id.value === "inactive") {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
  if (dpMode === "4") {
    for (i = 1; i < tr.length; i++) {
      if (tr[i].attributes.id.value === "closed") {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
  if (dpMode === "5") {
    for (i = 1; i < tr.length; i++) {
      if (tr[i].attributes.id.value === "locked") {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

// DISABLE ALL EXPIERD ITEMS THAT ARE NOT FROM THE SAME SUPPLIER AFTER WE CHECK A CHECKBOX
function expiredOnCheck() {
  var btns = document.getElementById("expButtons");
  var countInput = document.querySelectorAll("#expCheckbox");
  var id = $("input").attr("id");
  var itemData = document.querySelectorAll("#itemData");
  var expItem = document.querySelectorAll("#expItem");
  isNotCheck = true;
  if (id == "expCheckbox") {
    for (i = 0; i < countInput.length; i++) {
      if (countInput[i].checked) {
        isNotCheck = false;
        itemData[i].style.color = "black";
        expItem[i].style.color = "black";
      }
    }
    if (isNotCheck) {
      for (i = 0; i < countInput.length; i++) {
        countInput[i].disabled = false;
        itemData[i].style.color = "black";
        expItem[i].style.color = "black";
      }
    }

    for (i = 0; i < countInput.length; i++) {
      if (countInput[i].checked) {
        btns.style.display = "";
        for (j = 0; j < countInput.length; j++) {
          if (countInput[j].name !== countInput[i].name) {
            countInput[j].disabled = true;
            itemData[j].style.color = "#e3e3e3";
            expItem[j].style.color = "#e3e3e3";
          }
        }
        return 1;
      } else {
        btns.style.display = "none";
      }
    }
  } else {
    return false;
  }
}

// DISABLE ALL OUT OF STOCK ITEMS THAT ARE NOT FROM THE SAME SUPPLIER AFTER WE CHECK A CHECKBOX
function outOfStockOnCheck() {
  var btns = document.getElementById("outOfStockButtons");
  var countInput = document.querySelectorAll("#outOfStockCheckbox");
  var id = document.getElementById("outOfStockCheckbox").id;
  var itemData = document.querySelectorAll("#oosItemData");
  var oosItem = document.querySelectorAll("#oosItem");
  isNotCheck = true;
  if (id == "outOfStockCheckbox") {
    for (i = 0; i < countInput.length; i++) {
      if (countInput[i].checked) {
        isNotCheck = false;
        itemData[i].style.color = "black";
        oosItem[i].style.color = "black";
      }
    }
    if (isNotCheck) {
      for (i = 0; i < countInput.length; i++) {
        countInput[i].disabled = false;
        itemData[i].style.color = "black";
        oosItem[i].style.color = "black";
      }
    }

    for (i = 0; i < countInput.length; i++) {
      if (countInput[i].checked) {
        btns.style.display = "";
        for (j = 0; j < countInput.length; j++) {
          if (countInput[j].name !== countInput[i].name) {
            countInput[j].disabled = true;
            itemData[j].style.color = "#e3e3e3";
            oosItem[j].style.color = "#e3e3e3";
          }
        }
        return 1;
      } else {
        btns.style.display = "none";
      }
    }
  } else {
    return false;
  }
}

// GETS A STRING AND CHECKS IF IT CONTAINS CHARS THAT ARE NOT VALID
function charsValidation(inputtxt) {
  var letters = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
  for (i = 0; i < inputtxt.length; i++) {
    if (letters.test(inputtxt[i])) {
      return true;
    }
  }
  return false;
}

// GETS A NUMBER AND CHECKS IF IT CONTAINS CHARS THAT ARE NOT VALID
function validateNumbers(inputtxt) {
  var letters = /-/;
  for (i = 0; i < inputtxt.length; i++) {
    if (letters.test(inputtxt[i])) {
      return true;
    }
  }
  return false;
}

// GETS A STRING AND ID AND CHECKS IF THE TABLE ALREADY CONTAINS THE THESE VALUES
function checkIfExsists(name, id) {
  table = document.getElementById("chessboard");
  var rows = table.rows;
  for (var i = 1; i < rows.length; i++) {
    var cols = rows[i].cells;
    for (var c = 0; c < cols.length; c++) {
      if (cols[c].innerText == name && cols[0].innerHTML != id) {
        return true;
      }
    }
  }
  return false;
}
